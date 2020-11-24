cd ..
python3 webserv.py config.cfg &
PID=$!
cd -
sleep 1
curl localhost:8070/ins.png --output - 
if [[ "$str" == "" ]];then
    echo test_png passed
else
    echo test_png failed
fi 
kill $PID
