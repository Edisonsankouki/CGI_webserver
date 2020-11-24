cd ..
python3 webserv.py config.cfg &
PID=$!
cd -
sleep 1
str=$(curl localhost:8070/ | diff - index_expected.out)
if [[ "$str" == "" ]];then
    echo test_index_html passed
else
    echo test_index_html failed
fi 
kill $PID
