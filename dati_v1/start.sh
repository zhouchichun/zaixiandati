sh kill.sh $1
echo "old process killed"
nohup python3 FLASK_dati.py  --port $1 &
echo "new started at port $1"
