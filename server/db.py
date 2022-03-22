import mysql.connector

class Database:
    def __init__(self):
       self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            database="spider",
            passwd="Msdian-77",
            auth_plugin='mysql_native_password'
        )

    
    def execute(self,query):
        cur = self.mydb.cursor()
        cur.execute(query)
        rows = cur.fetchall()
        return rows
    
    def get_columns(self,table):
        cur = self.mydb.cursor()
        try:
            cur.execute("SHOW columns FROM " + table)
            return [column[0] for column in cur.fetchall()]
        except:
            return []
    
    def get_tables(self):
        cur = self.mydb.cursor()
        cur.execute("SELECT table_name FROM information_schema.tables;")
        return [x[0] for x in cur.fetchall()]