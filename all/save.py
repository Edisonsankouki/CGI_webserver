import sys
import socket
import os
import gzip

def main():
	#TODO: configuration rendered.
	try:
		conf = open(sys.argv[1])
	except Exception:
		print("Missing Configuration Argument")
		sys.exit(0)
	
	lines_0 = conf.readlines()
	conf.close()
	lines = []
	for i in lines_0:
		lines.append(i.strip("\n"))
	path = []
	for i in lines:
		a = i.split("=")[1]
		path.append(a)
	try:
		FILE = path[0]
		CGIBIN = path[1]
		EXEC = path[3]
	except IndexError:
		print("Missing Field From Configuration File")
		sys.exit(0)


	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
	s.bind(("127.0.0.1", int(path[2])))
	s.listen(100)


	
	
	while True:
		c, addr = s.accept()
		request = c.recv(1024).decode('utf-8')
		content = request.split(' ')[1]
		the_headers = request.split('\r\n')

		os.environ["SERVER_ADDR"] = "127.0.0.1"

		os.environ["SERVER_PORT"] = path[2]

		os.environ["REQUEST_METHOD"] = request.split(' ')[0]

		os.environ["REQUEST_URI"] = content


		url_message = the_headers[0]


		if(len(url_message.split('?'))==1):
			pass
		else:
			os.environ['QUERY_STRING'] =url_message.split("?")[1].split(" ")[0]
	

		for i in the_headers:
			if i == "":
				continue
			if i[0:5]=='Host':
				os.environ["HTTP_HOST"] = i
			if i[0:11]=='User-Agent':
				os.environ["USER-AGENT"] = i
			if i[0:15]=="Accept-Encoding":
				os.environ["HTTP_ACCEPT_ENCODING"] = i
			if i[0:7] == "Accept:":
				os.environ["HTTP_ACCEPT"] = i
			if i[0:14] == "Remote-Address":
				os.environ["REMODE_ADDRESS"] = i
			if i[0:12] == "Content-Type":
				os.environ["CONTENT_TYPE"] = i
			if i[0:14] == "Content-Length":
				os.environ["CONTENT_LENGTH"] = i
			if i[0:12] == "Remote-port":
				os.environ["REMOTE_PORT "]= i
		
			
		path1 = content.split('?')[0][1:]


		if "files" in path1:
			send_back = handle_static(path1,FILE)
		if "cgibin" in path1:
			send_back = handle_cgi(path1,EXEC,CGIBIN)
		if "py" in path1 or ".sh" in path1:
			send_back = handle_cgi(path1,EXEC,CGIBIN)
			
		else:
			send_back = handle_static(path1,FILE)
		
		try:
			O = os.environ["HTTP_ACCEPT_ENCODING"]
			if "gzip" in O:
				send_back = gzip.compress(send_back)
			c.send(send_back)
			c.close()
		except KeyError:
			c.send(send_back)
			c.close()
		






			
			
		

def read_the_static(filepath,FILE):
	filename = filepath.split("/")
	if(len(filename)==2):
		filename = filename[1]
	if(len(filename)==1):
		filename = filename[0]
	else:
		raise FileNotFoundError
	if ('jpg' in filename) or ('png' in filename) or ('jpeg' in filename):
		file = open(FILE + "/" + filename,'rb')
		index = file.read()
		file.close()
		return index
	file = open(FILE + "/" + filename,'r')
	index = file.read()
	file.close()
	return index

def handle_static(path,FILE):
	html_content = '''HTTP/1.1 200 OK
Content-Type: text/html\n
'''
	txt_content = '''HTTP/1.1 200 OK
Content-Type: text/plain\n
'''
	js_content = '''HTTP/1.1 200 OK
Content-Type: application/javascript\n
'''
	css_content = '''HTTP/1.1 200 OK
Content-Type: text/css\n
'''
	png_content = '''HTTP/1.1 200 OK
Content-Type: image/png\n
'''
	jpg_content = '''HTTP/1.1 200 OK
Content-Type: image/jpeg\n
'''
	xml_content = '''HTTP/1.1 200 OK
Content-Type: text/xml\n
'''
	error_header = '''HTTP/1.1 404 File not found
Content-Type: text/html\n
'''
	error_html_content = '''<html>
<head>
\t<title>404 Not Found</title>
</head>
<body bgcolor="white">
<center>
\t<h1>404 Not Found</h1>
</center>
</body>
</html>
'''
  
	try:

		if ".html" in path:
			return (html_content + read_the_static(path,FILE)).encode('utf-8')
		if ".txt" in path:
			return (txt_content + read_the_static(path,FILE)).encode('utf-8')
		if ".js" in path:
			return (js_content + read_the_static(path,FILE)).encode('utf-8')
		if ".css" in path:
			return (css_content + read_the_static(path,FILE)).encode('utf-8')
		if ".png" in path:
			return png_content.encode('utf-8') + read_the_static(path,FILE)
		if ".jpg" in path:
			return jpg_content.encode('utf-8') + read_the_static(path,FILE)
		if ".jpeg" in path:
			return jpg_content.encode('utf-8') + read_the_static(path,FILE)
		if ".xml" in path:
			return (xml_content + read_the_static(path,FILE)).encode('utf-8')
		else:
			return (html_content + '''<html>
<head>
\t<title>Hello!</title>
</head>
<body>
<h1>Hello World!</h1>
</body>
</html>
''').encode('utf-8')
		
		
	except FileNotFoundError:
		return (error_header+error_html_content).encode('utf-8')



def handle_cgi(path,EXEC,CGIBIN):
	parameter = path.split("/")
	if(len(parameter)==2):
		parameter = parameter[1]
	if(len(parameter)==1):
		parameter = parameter[0]
	r,w = os.pipe()
	original_pid = os.getpid()
	pid = os.fork()
	if pid == 0:
		os.close(r)
		os.dup2(w,1)
		os.dup2(w,2)
		try:
			os.execve(EXEC, (EXEC, CGIBIN+"/"+parameter), os.environ)
		except Exception:
			sys.exit(2)
	if pid <0 :
		cgi_header = '''HTTP/1.1 500 Internal Server Error
'''
		content = "<h1>500 internal error</h1>"

		return (cgi_header+content).encode('utf-8')
	else:
		os.close(w)
		r = os.fdopen(r)
	
		check_succeed = os.waitpid(pid,0)


		if(check_succeed[1]==256 or check_succeed[1] == 512):
			cgi_header = '''HTTP/1.1 500 Internal Server Error\n
'''
			content = "<h1>500 internal error</h1>"

			return (cgi_header+content).encode('utf-8')


		content = r.read()
		cgi_header = '''HTTP/1.1 200 OK
Content-Type: text/html\n
'''
		if "Content" in content or "HTTP" in content:
			content = content.split("\n")
			new_conntent = ""
			for x in content:
				if "Content" in x:
					continue
				if "HTTP" in x:
					new_conntent+=x+"\n\n"
					continue
				new_conntent += x
			new_conntent+="\n"
			if "HTTP" in new_conntent:
				return new_conntent.encode('utf-8')
			return (cgi_header + new_conntent).encode('utf-8')
		if '303' in content:
			cgi_header = '''HTTP/1.1 303 Custom Status\n
'''
		
		

		return (cgi_header+content).encode('utf-8')





if __name__ == '__main__':
	main()