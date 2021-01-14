import os, psutil, pickle
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
	