import pickle
import os
db_loc = 'db.p'

def size():
	print(os.stat(db_loc).st_size / 1024, 'KB | ', len(l_db()), 'keys')

def clear():
	pickle.dump({}, open(db_loc, 'wb'))
	return {}
def l_db():
	db = pickle.load(open(db_loc, 'rb'))
	return db
def u_db(db):
	pickle.dump(db, open(db_loc, 'wb'))