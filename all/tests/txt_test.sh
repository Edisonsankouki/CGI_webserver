cd ..
python3 webserv.py config.cfg &
PID=$!
cd -
str=$(curl localhost:8070/test.txt | diff -w - txt_test.out)
if [[ "$str" == "" ]];then
    echo test_txt passed
else
    echo test_txt failed
fi 
kill $PID
