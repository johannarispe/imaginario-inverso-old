#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import path, environ
import datetime
import serial 
import time
from flask import Flask, jsonify, request, session, g, redirect, url_for, abort, render_template, flash
from redis import StrictRedis
from celery import Celery

from assets import assets
import configuracion

# inicializando app
app = Flask(__name__)
app.config.from_object(configuracion)
assets.init_app(app)

# levantando servicio redis
redis = StrictRedis(host='localhost')

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

#levantando servicio celery
celery = make_celery(app)

# configurndo para escuchar puerta UART
port = serial.Serial('/dev/ttyAMA0',baudrate=4800, timeout=1.0)
if (port.isOpen() == False):
    port.open()

port.flushInput()
port.flushOutput()

@app.route('/', methods=['GET', 'POST'])
def index():
	if redis.llen(app.config['REDIS_MENSAJES']):
		flash('Task is already running at'+ app.config['REDIS_MENSAJES'], 'error')
	else:
		readSerial.delay()
		flash('Task started at '+app.config['REDIS_MENSAJES'], 'info')
	return render_template('index.html')

#Creando task para leer serial
@celery.task(name="tasks.readSerial")
def readSerial():
	now = datetime.datetime.now()
	horaRecepcion = now.strftime("%Y-%m-%d %H:%M")
	while True:
		data = port.readline()
		if data: 
			msg = {
				'time' : horaRecepcion,
				'mensaje' : data[:-1]
				}
			redis.rpush(app.config['REDIS_MENSAJES'],msg)
			time.sleep(0.1)

#Creando ruta para enviar mensajes
@app.route('/_conversar')
def enviarMensaje():
	now = datetime.datetime.now()
        timeString = now.strftime("%Y-%m-%d %H:%M")
	mensaje = request.args.get('mensaje')
	mensaje = mensaje+'\n'
	port.write(mensaje)
        mensajeTX = {
                'mensaje' : mensaje,
                'time': timeString
      	}
	return jsonify(mensajeTX)	

#Creando ruta para leer la cola de mensajes
@app.route("/_mensajes")
def leerCola():
	res = readSerial.apply_async()
	tails = redis.lrange(app.config['REDIS_MENSAJES'],0,-1)
	jsonDeMensajes = {"id": res.task_id, "mensajes" : tails}
	return jsonify(result = jsonDeMensajes)

# Correr el server
if __name__ == "__main__":
        port = int(environ.get("PORT", 5000))
	app.run(host='0.0.0.0', port = port, debug = True)
