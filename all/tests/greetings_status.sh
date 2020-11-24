cd ..
python3 webserv.py config.cfg &
PID=$!
cd -
sleep 1
str=$(curl -I 127.0.0.1:8070/greetings.html 2> /dev/null | grep '200 OK' | diff - greetings_status_expected.out) 
if [[ "$str" == "" ]];then
    echo test_greeting_status passed
else
    echo test_greeting_status failed
fi
kill $PID
