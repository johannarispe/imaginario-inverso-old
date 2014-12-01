#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import datetime
import feedparser
import serial 
import time
from flask import Flask, jsonify, request, session, g, redirect, url_for, abort, render_template, flash

# initialize app
app = Flask(__name__)

app.config.update(dict(
    DEBUG=True,
    SECRET_KEY='developmentkey',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

port = serial.Serial('/dev/ttyAMA0')
if (port.isOpen() == False):
    portort.open()

port.flushInput()
port.flushOutput()

#feed = feedparser.parse('http://www.eluniversal.com.mx/rss/mexico.xml')

#dict = {u'Peña':u'Peña=>-43', u'México': u'México-revolucionario', 'Detenidos': u'Heróicos-militantes-detenidos','detenidos':u'Heróicos-militantes-detenidos', 'normalistas': u'Heroes-normalistas'}

#for post in feed.entries:
#	for k, v in dict.items():
#		post.title = post.title.replace(k,v)

@app.route('/')
def iniciar():
	now = datetime.datetime.now()
	timeString = now.strftime("%Y-%m-%d %H:%M")
	templateData = {	
		'title' : 'HELLO!',
		'time': timeString
      }
#	return render_template('index.html',**feed)
	return render_template('index.html')

@app.route('/_conversar')
def mandarMensaje():
	now = datetime.datetime.now()
        timeString = now.strftime("%Y-%m-%d %H:%M")
	mensaje = request.args.get('mensaje')
	port.write(mensaje.encode('UTF-8'))
	time.sleep(0.05)
        mensajeTX = {
                'mensaje' : mensaje,
                'time': timeString
      	}
	return jsonify(mensajeTX)	

@app.route('/_recibir')
def recibirMensaje():
	now = datetime.datetime.now()
        timeString = now.strftime("%Y-%m-%d %H:%M")
	while True:
		mensaje = port.readline()
		if mensaje:
			mensajeRX = {
				'mensaje' : mensaje,
				'time' : timeString
			}
		else :
			mensajeRX = {
                                'mensaje' : '0000',
                                'time' : timeString
                        }
		time.sleep(0.05)
	return jsonify(time=timeString)

@app.route('/_add_numbers')
def add_numbers():
	a = request.args.get('a', 0, type=int)
	b = request.args.get('b', 0, type=int)
	return jsonify(result=a + b)


# Fire up server
if __name__ == "__main__":
        app.run(host='0.0.0.0')
        app.port = 80
        app.run()	
