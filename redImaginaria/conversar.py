#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import datetime
import feedparser
import serial 
import time
from flask import Flask, jsonify, request, session, g, redirect, url_for, abort, render_template, flash

app = Flask(__name__)

# modulos y config para uploader

import os.path

from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.storage import get_default_storage_class
from flask.ext.uploads import delete, init, save, Upload
from werkzeug import secure_filename


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.config['DEFAULT_FILE_STORAGE'] = 'filesystem'
app.config['UPLOADED_FILES_ALLOW'] = 'jpg'
app.config['UPLOADED_FILES_DENY'] = 'png'
app.config['UPLOADS_FOLDER'] = os.path.realpath('.') + '/static/'
app.config['FILE_SYSTEM_STORAGE_FILE_VIEW'] = 'static'
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024
db = SQLAlchemy(app)

Storage = get_default_storage_class(app)

init(db, Storage)

db.create_all()

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

# termina modulos y config uploader

# initialize app


app.config.update(dict(
    DEBUG=True,
    SECRET_KEY='developmentkey',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

# port = serial.Serial('/dev/ttyAMA0')
# if (port.isOpen() == False):
#     port.open()

# port.flushInput()
# port.flushOutput()

#feed = feedparser.parse('http://www.eluniversal.com.mx/rss/mexico.xml')

#dict = {u'Peña':u'Peña=>-43', u'México': u'México-revolucionario', 'Detenidos': u'Heróicos-militantes-detenidos','detenidos':u'Heróicos-militantes-detenidos', 'normalistas': u'Heroes-normalistas'}

#for post in feed.entries:
#	for k, v in dict.items():
#		post.title = post.title.replace(k,v)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method == 'POST':
        print 'saving'

        file = request.files['upload']

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            save(request.files['upload'])

        return redirect(url_for('index'))

    uploads = reversed(Upload.query.all())
    return render_template('index.html', uploads=uploads)



# @app.route('/')
# def iniciar():
# #	return render_template('index.html',**feed)
# 	return render_template('index.html')

@app.route('/_conversar')
def mandarMensaje():
	now = datetime.datetime.now()
        timeString = now.strftime("%Y-%m-%d %H:%M")
	mensaje = request.args.get('mensaje')
	mensaje = mensaje+'\n'
	# port.write(mensaje.encode('UTF-8'))
	#time.sleep(0.05)
        mensajeTX = {
                'mensaje' : mensaje,
                'time': timeString
      	}
	return jsonify(mensajeTX)	

def leerMensajes():
	bufferDeMensajes = ''
	while True: 
		mensaje = port.readline()
		if mensaje:
			print(mensaje)
			bufferDeMensajes = bufferDeMensajes + mensaje
		time.sleep(0.05)
	return bufferDeMensajes	



@app.route('/_recibir')
def recibirMensaje():
	now = datetime.datetime.now()
        timeString = now.strftime("%Y-%m-%d %H:%M")
	mensaje = 'NaN'
	if leerMensajes() != '':
		mensaje = bufferDeMensajes.decode('UTF-8')
		bufferDeMensajes = ''	
	#while True:
	#	mensaje = port.readline()
	#	if mensaje:
	#		mensajeRX = {
	#			'mensaje' : mensaje,
	#			'time' : timeString
	#		}
	#	else :
	#		mensajeRX = {
         #                       'mensaje' : '0000',
          #                      'time' : timeString
           #             }
	#	time.sleep(0.05)
	return jsonify(mensaje=mensaje)
# Fire up server




# endpoints pa uploader



@app.route('/delete/<int:id>', methods=['POST'])
def remove(id):
    upload = Upload.query.get_or_404(id)
    delete(upload)
    return redirect(url_for('index'))




# terminan endpoints pa uploader	


if __name__ == "__main__":
        app.run(host='0.0.0.0')
        app.port = 80
        app.run()	
