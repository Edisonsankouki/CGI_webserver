cd ..
python3 webserv.py config.cfg &
PID=$!
sleep 1
cd -
str=$(curl 127.0.0.1:8070/error.py | diff - 500_error.out )
if [[ "$str" == "" ]];then
    echo test_query passed
else
    echo test_query failed
fi

kill $PID