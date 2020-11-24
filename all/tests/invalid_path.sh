cd ..
python3 webserv.py config.cfg &
PID=$!
cd -
sleep 1
str=$(python3 ../webserv.py invalid | diff - invalid_path.out)
if [[ "$str" == "" ]];then
    echo test_invalid_path passed
else
    echo test_invalid_path failed
fi
kill $PID
