cd ..
python3 webserv.py config.cfg &
PID=$!
sleep 1
cd -
str=$(curl -I 127.0.0.1:8070/missing.html 2> /dev/null | grep '404' | diff - 404_status_expected.out )
if [[ "$str" == "" ]];then
    echo test_404 passed
else
    echo test_404 failed
fi

kill $PID
