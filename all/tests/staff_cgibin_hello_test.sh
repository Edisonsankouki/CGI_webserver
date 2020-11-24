cd ..
python3 webserv.py config.cfg &
PID=$!
cd -
sleep 1
str=$(curl localhost:8070/hello.py | diff - hello_expected.out)
if [[ "$str" == "" ]];then
    echo test_cgi_hello passed
else
    echo test_cgi_hello failed
fi
kill $PID
