cd ..
python3 webserv.py config.cfg &
PID=$!
cd -
sleep 1
str=$(curl -I localhost:8070/hello_1.py | diff - custom_header.out)

if [[ "$str" == "" ]];then
    echo test_custom passed
else
    echo test_custom passed
fi 
kill $PID