cd ..
python3 webserv.py config.cfg &
PID=$!
cd -
sleep 1
str=$(curl localhost:8070/greetings.html | diff - greetings_expected.out)
if [[ "$str" == "" ]];then
    echo test_greetings passed
else
    echo test_greetings failed
fi 
kill $PID
