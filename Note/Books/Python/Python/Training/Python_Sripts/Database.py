




import pymysql 

db = pymysql.connect("10.0.0.9","root","root","northwind")

cursor = db.cursor()

cursor.execute("DROP TABLE IF EXISTS PythonFirst")

sql = "CREATE TABLE PythonFirst (FIRST_NAME  CHAR(20) NOT NULL,LAST_NAME  CHAR(20),AGE INT)"

cursor.execute(sql)

db.close()
