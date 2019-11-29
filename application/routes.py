import sys
import os
import signal
from flask import request, send_from_directory, render_template, jsonify, make_response
from datetime import datetime
from flask import current_app as app
#import app.el_meu_util as mu
from .models import db, Mondecubs, Gent

@app.route('/')
@app.route('/index')
def index():
	nom = request.args.get("nom")
	user = {'username': nom}
	entorn = app.config["ENTORN"]
	return render_template('index.html.j2', title='Entorn: '+entorn, user=user)

@app.route('/nou')
def nou_cub():
	usuari = 'mariona'
	colorhex = '#000000'
	x=0
	y=5
	z=10
	nou_mon = Mondecubs(usuari=usuari, x=x, y=y, z=z, colorhex=colorhex)
	db.session.add(nou_mon)
	db.session.commit()
	rows = db.session.query(Mondecubs).count()
	#mon = Mondecubs.query.filter(Mondecubs.usuari == usuari).order_by(Mondecubs.id.desc()).first()
	#return 'Ultim id: ' + str(mon.id)
	return 'El mon, ara te ' + str(rows) + ' cubs...'

@app.route('/render')
def render():
	nom = request.args.get("nom")
	user = {'username': nom}
	return render_template('babylon.html.j2', title=nom, user=user)

@app.route('/prou')
def prou():
	pid = int(os.getpid())
	print ('Adeu')
	os.kill(pid, signal.SIGTERM)

@app.route('/minim')
def minimcraft():
	nom = request.args.get("nom")
	user = {'username': nom}
	js_urls = []

	if app.config["JS_CDN"]:
		origen = "_CDN"
	else:
		origen = ""

	js_urls.append(app.config["JS"+origen+"_BABYLON"])
	js_urls.append(app.config["JS"+origen+"_BABYLON_GUI"])
	js_urls.append(app.config["JS"+origen+"_JQUERY"])

	return render_template('minimcraft.html.j2', title=nom, user=user, js_urls=js_urls)

@app.route('/desar',methods=['POST'] )
def desaCubs():
	data = request.json
	camara =  data["camara"]
	cubs = data["cubs"]
	print (data["camara"])
	try:
		for unCub in cubs:
			x = unCub["x"]
			y = unCub["y"]
			z = unCub["z"]
			colorhex = unCub["colorHex"]
			usuari = 'josep'

			#Preparem esborrat del cub si ja existia:
			db.session.query(Mondecubs).filter(Mondecubs.usuari == usuari,
												Mondecubs.x == x,
												Mondecubs.y == y,
												Mondecubs.z == z, ).delete()
			#Preparem el desat del cub:
			nou_mon = Mondecubs(usuari = usuari, x = x, y = y, z = z, colorhex = colorhex)
			if colorhex:
				#desem el cub si es de color
				db.session.add(nou_mon)
		#Tot el que s'havia preparat s'executa:
		db.session.commit()

	except Exception as e:
		data = e
	return str(data)
	
#Recupera els cubs de la base de dades, el javascript els recrea
@app.route('/rebre',methods=['POST'] )
def rebreCubs():
	#dades_rebudes = request.json
	#req = request.get_json()
	req =  request.json
	print (req) #per exemple posició de camera, o id per saber que falta...
	try:
		# aquí hauria d'anar a buscar els cubs...
		usuari = 'josep'
		cubs_llegits = db.session.query(Mondecubs).filter(Mondecubs.usuari == usuari).all()
		cols = ['id', 'x', 'y', 'z','colorhex']
		data = cubs_llegits
		response_body = [{col: getattr(d, col) for col in cols} for d in data]
		dades_enviar = jsonify(response_body)
	except Exception as e:
		dades_enviar = str(e)
	return dades_enviar

@app.route('/esborra')
def esborra():
	cur_time = str(datetime.now())
	usuari = 'josep'
	db.session.query(Mondecubs).filter(Mondecubs.usuari == usuari).delete()
	#models.User.query().delete()
	db.session.commit()
	return cur_time + " un nou mon!"

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/textures/<path:path>')
def send_js(path):
    return send_from_directory('static/textures', path)

@app.route('/js/<path:path>')
def static_js(path):
	#print(path)
	return send_from_directory('static/js', path)
