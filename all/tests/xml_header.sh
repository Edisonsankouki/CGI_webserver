cd ..
python3 webserv.py config.cfg &
PID=$!
sleep 1
cd -
str=$(curl -I 127.0.0.1:8070/note.xml 2> /dev/null | grep '200 OK' | diff -w - xml_header.out) 
if [[ "$str" == "" ]];then
    echo test_xml_header passed
else
    echo test_xml_header failed
fi

kill $PID