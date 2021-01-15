import os, psutil, pickle, codecs
db_loc = os.getenv("db_loc")

def to_str():
	return str(os.stat(db_loc).st_size / 1024) + ' KB | ' + str(len(l_db())) + ' keys'

def db_size():
	return os.stat(db_loc).st_size / 1024

def keys_size():
	return len(l_db())

def clear():
	pickle.dump({}, open(db_loc, 'wb'))
	return {}
def l_db():
	db = pickle.load(open(db_loc, 'rb'))
	return db
def u_db(db):
	pickle.dump(db, open(db_loc, 'wb'))

ram_size = 500 * 1024
disk_size = 500 * 1024

def ram_usage():
	process = psutil.Process(os.getpid())
	return process.memory_info().rss / 1024

def disk_usage():
	disk = 0
	start_path = '.'
	for path, dirs, files in os.walk(start_path):
		for f in files:
			fp = os.path.join(path, f)
			disk += os.path.getsize(fp)
	return disk / 1024

def ram_usage_p():
	return ram_usage() / ram_size

def disk_usage_p():
	return disk_usage() / disk_size

def db_disk_p():
	return db_size() / disk_size
	

def circle(size, big='', color=''):
	return '<div class="dark '+big+' '+color+' c100 pPSIZE center"><span>PSIZE%</span><div class="slice"><div class="bar"></div><div class="fill"></div></div></div>'.replace('PSIZE', str(size)[:5])

def html_stats(mobile):
	s = codecs.open('web/stats_header.html', 'r', 'utf-8').read()
	if mobile:
		return s + '<center><br><br><table style=" width:75%;margin-top:10%;"><tr>RAM</tr><tr>'+circle(ram_usage_p()*100)+'</tr><br><tr>DISK</tr><tr>'+circle(disk_usage_p()*100, 'green')+'</tr><br><tr>DB: '+str(len(l_db())) + ' keys'+'</tr><tr>'+circle(db_disk_p()*100, 'orange')+'</tr></table></center>'
	else:
		return s + '<center><table style=" width:75%;margin-top:10%;"><tr><th>RAM</th><th>DISK</th><th>DB: '+str(len(l_db())) + ' keys'+'</th></tr><tr><td>'+circle(ram_usage_p()*100, big='big')+'</td><td>'+circle(disk_usage_p()*100, big='big', color='green')+'</td><td>'+circle(db_disk_p()*100, big='big', color='orange')+'</td></tr></table></center>'
