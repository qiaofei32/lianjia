import os
import sys
import json
import MySQLdb
from warnings import filterwarnings
filterwarnings('ignore', category = MySQLdb.Warning)
# resetwarnings()
import MySQLdb.cursors as cursors


class MySQL_API(object):
	"""
	mysql api of mine
	"""
	def __init__(self, conf_file="DataBase.conf", connect_info={}, cursorclass_name=None):
		"""
		init and connect to mysql
		"""
		self.bCrateDb = False	
		conf_file_list = []
		conf_file_list.append(conf_file)
		conf_file_list.append("DataBase.conf")
		conf_file_list.append("./conf/DataBase.conf")
		conf_file_list.append("../conf/DataBase.conf")
		conf_file_list.append("../../conf/DataBase.conf")
		conf_file_list = list(set(conf_file_list))
		
		for conf_file in conf_file_list:
			if not connect_info and os.path.exists(conf_file):
				fileHandler = open(conf_file,"r")
				data = fileHandler.read()
				fileHandler.close()
				connect_info = json.loads(data)
		if not connect_info:
			print "connect info error!"
			return None
			
		host   = connect_info.get("host", "127.0.0.1")
		port   = connect_info.get("port", 3306)
		user   = connect_info.get("user", "root")
		passwd = connect_info.get("passwd", "root")
		db	   = connect_info.get("db", "mysql")
		# cursorclass_name = connect_info.get("cursorclass","DictCursor")
		# cursorclass_name = connect_info.get("cursorclass","Cursor") # ago
		cursorclass_name = cursorclass_name if cursorclass_name else connect_info.get("cursorclass", "Cursor")
		
		cursorclass = getattr(cursors, cursorclass_name)
		
		try:
			self.conn = MySQLdb.connect(host=host, port=port, user=user, passwd=passwd, db=db, cursorclass=cursorclass)
		except Exception,e:
			if "Unknown database" in str(e):
				try:
					self.conn = MySQLdb.connect(host=host, port=port, user=user, passwd=passwd, cursorclass=cursorclass)
					self.bCrateDb = True
				except:
					self.conn = None
		if not self.conn:
			print "Failed To Connect To MySQL,Quit..."
			# sys.exit(1)
			return None
		# print "Connect To MySQL Done..."
		self.cursor = self.conn.cursor() 	
		self.cursor.execute("set names utf8") 
		
		if self.bCrateDb and db:
			print "create db:%s" %db
			self.cursor.execute("CREATE DATABASE `%s` /*!40100 COLLATE 'utf8_general_ci' */;" %db) 
			self.conn.select_db(db)
	
	def write_items(self, sql, param=None, auto_commit=True, print_error=False):
		ret = [True,None]
		try:
			if not param:
				ret[1] = self.cursor.execute(sql) 
			else:
				if type(param)==type((1,)) or type(param)==type([1]):
					# param = (("bbb",int(time.time())), ("ccc",33), ("ddd",44) )  
					ret[1] = self.cursor.executemany(sql,param) 
		except Exception,e:
			if print_error:
				print "=" * 60
				print e
				print sql
				print param
				ret[0] = False
				ret[1] = param
		if auto_commit:
			self.conn.commit()
		return ret
		
	def query(self, sql, print_error=False):
		ret = None
		try:
			n = self.cursor.execute(sql) 
			ret = self.cursor.fetchall()
		except Exception,e:
			if print_error:
				print e
				ret = sql		
		return ret
	
	def create_database(self, db_name):
		sql = "CREATE DATABASE IF NOT EXISTS %s COLLATE='utf8_general_ci' " %db_name
		self.query(sql)
		self.commit()
		self.conn.select_db(db_name)
		
	def commit(self):
		self.conn.commit()
		
	def close(self):
		if self.cursor:self.cursor.close()
		if self.conn:self.conn.close()
		
	def __del__(self):
		if self.cursor:self.cursor.close()
		if self.conn:self.conn.close()
		
if __name__=="__main__":
	
	print "TODO"
	# api = Write2MySQL()
