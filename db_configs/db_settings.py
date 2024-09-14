import psycopg2
from .config import DB_CONFIG

class Database:
    def __init__(self):
        self.connection = psycopg2.connect(
            dbname=DB_CONFIG.get('database'),
            user=DB_CONFIG.get('user'),
            password=DB_CONFIG.get('password'),
            host=DB_CONFIG.get('host'),
            port=DB_CONFIG.get('port')
        )
        self.cursor = self.connection.cursor()

    def execute(self, query, params=None):
        if params is None:
            params = ()
        self.cursor.execute(query, params)
        self.connection.commit()

    def fetchall(self, query, params=None):
        if params is None:
            params = ()
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    @staticmethod
    def fetchone(query, params=None):
        if params is None:
            params = ()
        db.cursor.execute(query, params)
        return db.cursor.fetchone()


db = Database()

def execute_query(query, params=None):
    db.execute(query, params)

def fetchall(query, params=None):
    return db.fetchall(query, params)

def fetchone(query, params=None):
    return db.fetchone(query, params)
