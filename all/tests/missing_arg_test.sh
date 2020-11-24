cd ..
python3 webserv.py config.cfg &
PID=$!
cd -
sleep 1
str=$(python3 ../webserv.py | diff - missing_arg.out)
if [[ "$str" == "" ]];then
    echo test_missing_arg passed
else
    echo test_missing_arg failed
fi
kill $PID
