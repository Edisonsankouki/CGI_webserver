cd ..
python3 webserv.py config.cfg &
PID=$!
cd -
str=$(curl localhost:8070/home.js | diff - js_expected.out)
if [[ "$str" == "" ]];then
    echo test_js passed
else
    echo test_js failed
fi 
kill $PID
