import sys
import os
import signal
import app.el_meu_util as mu
from datetime import datetime
from flask import request, send_from_directory, render_template, jsonify
from app import app, db
from sqlalchemy.sql import text



#import sqlalchemy as db
#engine = db.create_engine('postgresql+pg8000://jmsansco_postgre:aralep69&U@localhost/jmsansco_bram')
#"dbname='bonior' user='postgres' host='localhost' password='superpass'"
#connection = engine.connect()
#metadata = db.MetaData()
#taula = db.Table('exemple', metadata, autoload=True, autoload_with=engine)
#resultat = '' #+ ', '.join(taula.columns.keys())

engine = db.engine


@app.route('/')
@app.route('/index')
def index():
	nom = request.args.get("nom")
	user = {'username': nom}
	entorn = app.config["ENTORN"]
	return render_template('index.html.j2', title='Entorn: '+entorn, user=user)	

@app.route('/ara')
def the_time():
	cur_time = str(datetime.now())
	connection = engine.connect()
	#result = connection.execute("SELECT nom FROM exemple WHERE id=3")
	result = connection.execute("SELECT current_user as nom")
	for row in result:
		resultat = row['nom']

	connection.close()
	return cur_time + " es l'hora actual!  ...Yuppy Yeahhh! " + resultat

@app.route('/esborra')
def esborra():
	cur_time = str(datetime.now())
	connection = engine.connect()
	cmd = "DELETE FROM mondecubs WHERE usuari = :usuari"
	usuari = 'josep'
	result = connection.execute(text(cmd),usuari = usuari)
	connection.close()
	return cur_time + " un nou mon!"


@app.route('/prou')
def prou():
	pid = int(os.getpid())
	print ('Adeu')

	os.kill(pid, signal.SIGTERM)
	#os.kill(pid, signal.SIGKILL)
	
@app.route('/r')
def pr():
	llista_pr = mu.running_process()
	return 'Processos:<br/>' + llista_pr
	
@app.route('/render')
def render():
	nom = request.args.get("nom")
	user = {'username': nom}
	return render_template('babylon.html.j2', title=nom, user=user)

@app.route('/minim')
def minimcraft():
	nom = request.args.get("nom")
	user = {'username': nom}
	return render_template('minimcraft.html.j2', title=nom, user=user)

@app.route('/desa',methods=['POST'] )
def desaCubs():
	data = request.json
	#print (data[0]["colorHex"])
	connection = engine.connect()

	cmd = "INSERT INTO mondecubs (x,y,z,colorhex,usuari) values (:x,:y,:z,:color,:usuari)"

	try:
		for unCub in data:
			x = unCub["x"]
			y = unCub["y"]
			z = unCub["z"]
			color = unCub["colorHex"]
			usuari = 'josep'
			connection.execute(text(cmd), x = x, y = y, z = z, color = color, usuari = usuari)
	except Exception as e:
		data = e
	connection.close()
	return 'Resultat:' + str(data)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),'favicon.ico', mimetype='image/vnd.microsoft.icon')	

@app.route('/textures/<path:path>')
def send_js(path):
    return send_from_directory('static/textures', path)