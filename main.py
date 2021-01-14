#from replit import db
from db import *
from datetime import datetime
t = datetime.today().strftime('%Y-%m-%d-%H-%M-%S')
from urllib.parse import unquote
#import hashlib

from flask import Flask, send_from_directory, request
from flask_mobility import Mobility
import codecs
import os

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

def cacheWorkaround(file):
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

@app.route('/')
def main():
	#index.html
	return cacheWorkaround(codecs.open('web/index.html', 'r', 'utf-8'))

def circle(size, big='', color=''):
	return '<div class="dark '+big+' '+color+' c100 pPSIZE center"><span>PSIZE%</span><div class="slice"><div class="bar"></div><div class="fill"></div></div></div>'.replace('PSIZE', str(size)[:5])

@app.route('/stats')
def stats():
	#index.html
	s = codecs.open('web/stats_header.html', 'r', 'utf-8').read()
	if request.MOBILE:
		response = s + '<center><br><br><table style=" width:75%;margin-top:10%;"><tr>RAM</tr><tr>'+circle(ram_usage_p()*100)+'</tr><br><tr>DISK</tr><tr>'+circle(disk_usage_p()*100, 'green')+'</tr><br><tr>DB: '+str(len(l_db())) + ' keys'+'</tr><tr>'+circle(db_disk_p()*100, 'orange')+'</tr></table></center>'
	else:
		response = s + '<center><table style=" width:75%;margin-top:10%;"><tr><th>RAM</th><th>DISK</th><th>DB: '+str(len(l_db())) + ' keys'+'</th></tr><tr><td>'+circle(ram_usage_p()*100, big='big')+'</td><td>'+circle(disk_usage_p()*100, big='big', color='green')+'</td><td>'+circle(db_disk_p()*100, big='big', color='orange')+'</td></tr></table></center>'

	return response

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


@app.route('/update_usr/<usr>/<pas>/<new_usr>')
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

@app.route('/favicon.ico')
def favicon():
	return send_from_directory(os.path.join(app.root_path, 'static'),'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == '__main__':
	#Run server forever
	keep_alive()
