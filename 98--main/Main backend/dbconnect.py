import MySQLdb

def connection():
	conn = MySQLdb.connect(host="localhost",
		                           user="root1",
		                           passwd="Arsh2308@",
		                           db="databasename",
		                         )
	c = conn.cursor()
	return c,conn

  #auth_plugin='mysql_native_password'