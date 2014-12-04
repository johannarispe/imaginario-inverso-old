import serial
import time
import datetime
import json

port = serial.Serial('/dev/ttyAMA0')

while True:
	data = port.readline()
	if data: 
		fo = open("/static/test.json","wb")
		now = datetime.datetime.now()
		timeString = now.strftime("%Y-%m-%d %H:%M")
		mensajeTX = {	
			'mensaje' : mensaje,
		        'time': timeString
		}
		fo.write(json.dumps(mensajeTX))
