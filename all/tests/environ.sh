cd ..
python3 webserv.py config.cfg &
PID=$!
cd -
sleep 1
str=$(curl localhost:8070/environ.py | diff -w - environ.out)
if [[ "$str" == "" ]];then
    echo test_environ passed
else
    echo test_environ failed
fi 
kill $PID