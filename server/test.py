import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  database="spider",
  passwd="Msdian-77",
  auth_plugin='mysql_native_password'
)

mycursor = mydb.cursor()

mycursor.execute("SELECT table_name FROM information_schema.tables;")
 
myresult = mycursor.fetchall()
 
for x in myresult:
  print(x)