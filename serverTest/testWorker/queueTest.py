from __future__ import absolute_import
from os import path, environ
import json
from flask import Flask, Blueprint, abort, jsonify, request, session
import settings
from celery import Celery
import serial

app = Flask(__name__)
app.config.from_object(settings)

#app = Celery('tasks', broker='redis://localhost')

def make_celery(app):
	celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'])
    	celery.conf.update(app.config)
    	TaskBase = celery.Task
    	class ContextTask(TaskBase):
        	abstract = True
        	def __call__(self, *args, **kwargs):
            		with app.app_context():
                		return TaskBase.__call__(self, *args, **kwargs)
    	celery.Task = ContextTask
	return celery

celery = make_celery(app)

port = serial.Serial("/dev/ttyAMA0", baudrate=4800, timeout=1.0)

@celery.task
def readSerial():
	while True:
		data = port.readline()
	        if data:
			print ("\nreceived:\n"+data[:-1])
		        sleep(0.1)

@app.route("/test")
def startReading():
	res = readSerial.apply_async()
	retval = readSerial.AsyncResult(task_id).get(timeout=1.0)
	context = {"id": res.task_id}
    	result = "{}".format(context['id'],retval)
	#result = "add((x){}, (y){})".format(context['x'], context['y'])
    	goto = "{}".format(context['id'])
	return jsonify(result=result)

@app.route("/test/result/<task_id>")
def show_result(task_id):
	retval = readSerial.AsyncResult(task_id).get(timeout=1.0)
    	return repr(retval)

if __name__ == "__main__":
	port = int(environ.get("PORT", 5000))
	app.run(host='0.0.0.0', port = port, debug = True)
