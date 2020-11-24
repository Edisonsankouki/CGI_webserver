cd ..
python3 webserv.py config.cfg &
PID=$!
sleep 1
cd -
str=$(curl 127.0.0.1:8070/error.py | diff - 500_error.out )
if [[ "$str" == "" ]];then
    echo test_500 passed
else
    echo test_500 failed
fi

kill $PID