cd ..
python3 webserv.py config.cfg &
PID=$!
cd -
sleep 1
str=$(curl localhost:8070/example.css | diff -w - css_test.out)
if [[ "$str" == "" ]];then
    echo test_css passed
else
    echo test_css failed
fi 
kill $PID