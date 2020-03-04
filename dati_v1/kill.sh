ps -ef | grep FLASK_dati|grep $1 |grep -v 'grep' | awk '{print $2}' | xargs kill -9
echo "old process killed"
#python manage.py runserver $1 &
#echo "new started"
