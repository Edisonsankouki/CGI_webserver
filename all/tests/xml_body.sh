cd ..
python3 webserv.py config.cfg &
PID=$!
cd -
sleep 1
str=$(curl localhost:8070/note.xml | diff -w - xml_body.out)
if [[ "$str" == "" ]];then
    echo test_xml_body passed
else
    echo test_xml_body failed
fi 
kill $PID
