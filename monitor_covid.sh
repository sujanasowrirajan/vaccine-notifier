PID=`pgrep -f '/usr/local/opt/python-3.9.0/bin/python3.9 /home/pi/Desktop/covid.py'`
echo $PID
if [ -z $PID ]; then /home/pi/Desktop/start_cowin.sh; fi