import sqlite3

class Database:
    def __init__(self,db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
    
    def execute(self,query):
        self.cur.execute(query)
        rows = self.cur.fetchall()
        return rows
