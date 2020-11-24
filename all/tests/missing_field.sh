cd ..
python3 webserv.py config.cfg &
PID=$!
cd -
sleep 1
str=$(python3 ../webserv.py broken_cfg.cfg | diff - missing_field.out)
if [[ "$str" == "" ]];then
    echo test_missing_field passed
else
    echo test_missing_field failed
fi
kill $PID
