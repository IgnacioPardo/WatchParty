#from replit import db
from db import *
from datetime import datetime
from urllib.parse import unquote
#import hashlib

from flask import Flask, send_from_directory, request
from flask_mobility import Mobility
import codecs, os, zipfile

#Threading
from threading import Thread

#WSGIServer
from gevent.pywsgi import WSGIServer

#Disable Warnings
import warnings
#warnings.filterwarnings('ignore')

#Logging
import logging

#Logging configuration set to debug on debug.log file

"""logging.basicConfig(filename='debug.log',level=logging.DEBUG)
logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

#Disable unneeded dependencies logging
werkzeugLog = logging.getLogger('werkzeug')
werkzeugLog.disabled = True
requestsLog = logging.getLogger('urllib3.connectionpool')
requestsLog.disabled = True"""

db = l_db()

def getDLink(r):
	if r:
		return 'https://www.icloud.com/shortcuts/5e4a1b6ff02c4f2ab15bf90addf28bfd'
	return '/download'

def cacheWorkaround(file):
    t = datetime.today().strftime('%Y-%m-%d-%H-%M-%S')
    return file.read().replace('REPLACE', t)

def validate(usr, pas):
	if usr not in db.keys():
		return False
	return db[usr]['pas'] == pas

def run():
	#WSGIServer
	WSGIServer(('', 8081), app).serve_forever()

#Thread
def keep_alive():
	t = Thread(target=run)
	t.start()

app = Flask(__name__)
Mobility(app)


@app.route('/dark')
@app.route('/dark_redirect_signin')
def gray():
	#index.html
	site = cacheWorkaround(codecs.open('web/index.html', 'r', 'utf-8'))
	site = site.replace('download_link', getDLink(request.MOBILE))
	return site

@app.route('/')
@app.route('/redirect_signin')
@app.route('/black')
@app.route('/black_redirect_signin')
def main():
	#index.html
	site = cacheWorkaround(codecs.open('web/index.html', 'r', 'utf-8'))
	site = site.replace('download_link', getDLink(request.MOBILE))
	return site.replace('#222222', 'black').replace('#282828', '#0e0e0e').replace('icon-196', 'icon-196-black').replace('icon-152', 'icon-152-black')

@app.route('/white')
@app.route('/white_redirect_signin')
def white():
	#index.html
	site = cacheWorkaround(codecs.open('web/index.html', 'r', 'utf-8'))
	site = site.replace('download_link', getDLink(request.MOBILE))
	return site.replace('white', 'black').replace('#222222', 'white').replace('#282828', '#f0f0f0').replace('sign_out.svg', 'sign_out_red.svg')

@app.route('/stats')
def stats():
	return html_stats(request.MOBILE)

@app.route('/validate/')
@app.route('/validate/<usr>')
@app.route('/validate/<usr>/<pas>')
def check_valid(usr=None, pas=None):
	if usr == 'null':
		usr = None
	if pas == 'null':
		pas = None
	if usr and pas:
		print({'response' : validate(usr, pas), 'description':(not validate(usr, pas))*'in'+'valid user'})
		return {'response' : validate(usr, pas), 'description':(not validate(usr, pas))*'in'+'valid user', 'data' : {'friends': db[usr]['friends'], 'np' : db[usr]['np'], 'history' : db[usr]['history']}}
	return {'response' : False, 'description':'invalid sign in'}


@app.route('/get_usr_by_id/<usr>/<pas>/<o_usr>')
def get_usr_by_id(usr, pas, o_usr):
	if validate(usr, pas):
		if o_usr in db[usr]['friends']:
			return db[o_usr]['now']
		return 'id not in user friend list'
	return {'response' : validate(usr, pas), 'description':(not validate(usr, pas))*'in'+'valid user'}

@app.route('/get_friends_np/<usr>/<pas>')
def get_friends_np(usr, pas):
	if validate(usr, pas):
		res = {}
		for f in db[usr]['friends']:
			res[f] = db[f]['np']
		return {'response' : True, 'description': 'friends now playing', 'data' : res}
	return {'response' : validate(usr, pas), 'description':(not validate(usr, pas))*'in'+'valid user'}

@app.route('/add/<usr>/<pas>/<o_usr>')
def add(usr, pas, o_usr):
	if validate(usr, pas):
		if o_usr not in db[usr]['friends']:
			if o_usr in db.keys():
				db[usr]['friends'] += [o_usr]
				u_db(db)
				return {'response' : True, 'description': o_usr+' added as friend', 'data':{'friends': db[usr]['friends'], 'np' : db[usr]['np'], 'history' : db[usr]['history']}}
			return {'response' : False, 'description':'invalid friend id'}
		return {'response' : False, 'description':'friend allready in friend list'}
	return {'response' : validate(usr, pas), 'description':(not validate(usr, pas))*'in'+'valid user'}

@app.route('/remove/<usr>/<pas>/<o_usr>')
def remove(usr, pas, o_usr):
	if validate(usr, pas):
		if o_usr in db[usr]['friends']:
			if o_usr in db.keys():
				db[usr]['friends'].remove(o_usr)
				u_db(db)
				return {'response' : True, 'description': o_usr+' removed from friends', 'data':{'friends': db[usr]['friends'], 'np' : db[usr]['np'], 'history' : db[usr]['history']}}
			return {'response' : False, 'description':'invalid friend id'}
		return {'response' : False, 'description':'friend not in friend list'}
	return {'response' : validate(usr, pas), 'description':(not validate(usr, pas))*'in'+'valid user'}


@app.route('/test')
@app.route('/test/<url>')
def test(url='Dou|a'):
	print(url)
	url = url.replace('|', '/')
	print(url)
	return {'url':url}


@app.route('/update_np/<usr>/<pas>/<title>')
@app.route('/update_np/<usr>/<pas>/<title>/<url>/<platform>')
def update_np(usr, pas, title, url=None, platform=None):

	url = unquote(url)
	url = url.replace('|', '/').replace(';', ':')
	platform = unquote(platform)
	title = unquote(title)

	print(usr, title, url, platform)

	if validate(usr, pas):
		db[usr]['np'] = {'url' : url, 'title' : title, 'platform' : platform, 'timestamp' : t}
		db[usr]['history'][t] = db[usr]['np']
		del db[usr]['history'][t]['timestamp']
		u_db(db)
		return {'url' : url, 'title' : title, 'platform' : platform, 'timestamp' : t}
	return {'response' : validate(usr, pas), 'description':(not validate(usr, pas))*'in'+'valid user'}

@app.route('/update_np_ios/<usr>/<pas>/<title>/<url>/<platform>')
def update_np_ios(usr, pas, title, url=None, platform=None):
	url = unquote(url)
	url = url.replace('|', '/').replace(';', ':')
	platform = unquote(platform)
	title = unquote(title)
	print(usr, title, url, platform)
	if validate(usr, pas):
		db[usr]['np'] = {'url' : url, 'title' : title, 'platform' : platform, 'timestamp' : t}
		db[usr]['history'][t] = db[usr]['np']
		del db[usr]['history'][t]['timestamp']
		u_db(db)
		return 'Done'
	return 'Error'

@app.route('/retrieve_np/<usr>/<pas>')
def retrieve_np(usr, pas):
	if validate(usr, pas):
		return db[usr]['np']
	return {'response' : validate(usr, pas), 'description':(not validate(usr, pas))*'in'+'valid user'}

"""
@app.route('/set_np/<usr>/<pas>/<title>')
def set_np(usr, pas, title):
	if validate(usr, pas):
		db[usr]['np']['title'] = title
		u_db(db)
		return db[usr]['np']
	return 'invalid username and password'
"""

@app.route('/clear_h/<usr>/<pas>')
def clear_h(usr, pas):
	if validate(usr, pas):
		db[usr]['np'] = {'url' : '', 'title' : '', 'platform' : '', 'timestamp' : ''}
		db[usr]['history'] = {}
		u_db(db)
		return db[usr]
	return {'response' : validate(usr, pas), 'description':(not validate(usr, pas))*'in'+'valid user'}


@app.route('/change_username/<usr>/<pas>/<new_usr>')
def update_usr(usr, pas, new_usr):
	if validate(usr, pas):
		db[new_usr] = db.pop(usr)
		u_db(db)
		return 'Done'
	return {'response' : validate(usr, pas), 'description':(not validate(usr, pas))*'in'+'valid user'}

@app.route('/new/<usr>/<pas>')
def new_usr(usr, pas):
	if usr not in db.keys():
		db[usr] = {
					'pas' : pas, 
					'friends' : [],
					'np' : {'url' : '', 'title' : '', 'platform' : '', 'timestamp' : ''},
					'history' : {}
				}
		u_db(db)
		return {'response':True, 'description' : usr + ' created', 'np': db[usr]['np'], 'friends': db[usr]['friends'], 'history': db[usr]['history']}
	return {'response':False, 'description': 'username allready in use'}

@app.route('/da')
def delete_all():
	db = clear()
	return 'Done'

@app.route('/list_db')
def list_db():
	returnDB = db
	for n in returnDB.keys():
		if "'" in returnDB[n]['np']['title']:
			returnDB[n]['np']['title'] = returnDB[n]['np']['title'].replace("'", '')
		for t in returnDB[n]['history']:
			if "'" in returnDB[n]['history'][t]['title']:
				returnDB[n]['history'][t]['title'] = returnDB[n]['history'][t]['title'].replace("'", '')

	return '<body>'+str(returnDB).replace("'", '"').replace('None', 'null')+'<script>console.log(document.body.innerText);\nmyObj =JSON.parse(document.body.innerText);\ntxt = "<table border=\'1\'>";\nfor (x in myObj) {\ntxt += "<tr><td>" + JSON.stringify(myObj[x]) + "</td></tr>";\n}\ntxt += "</table>";\ndocument.body.innerHTML = txt;</script></body>'

@app.route('/download')
def zipExtension():
	zf = zipfile.ZipFile("static/WatchParty-Chrome.zip", "w")
	for dirname, subdirs, files in os.walk("extension"):
		zf.write(dirname)
		for filename in files:
			zf.write(os.path.join(dirname, filename))
	zf.close()
	return send_from_directory(os.path.join(app.root_path, 'static'),'WatchParty-Chrome.zip')

@app.route('/favicon.ico')
def favicon():
	return send_from_directory(os.path.join(app.root_path, 'static'),'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == '__main__':
	#Run server forever
	keep_alive()
