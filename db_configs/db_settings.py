import psycopg2
from db_configs.config import DB_CONFIG

class DBSettings:
    """Context manager for database operations."""
    def __enter__(self):
        self.conn = psycopg2.connect(**DB_CONFIG)
        self.cursor = self.conn.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self.conn.rollback()
        else:
            self.conn.commit()

        self.cursor.close()
        self.conn.close()

    def execute(self, query, params=None):
        """Executes a data modification query."""
        self.cursor.execute(query, params)

    def fetchall(self, query, params=None):
        """Returns all rows matching the query."""
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def fetchone(self, query, params=None):
        """Returns one row matching the query."""
        self.cursor.execute(query, params)
        return self.cursor.fetchone()

def execute_query(query, params=None):
    """Executes a data modification query."""
    with DBSettings() as db:
        db.execute(query, params)

def fetchall(query, params=None):
    """Returns all rows matching the query."""
    with DBSettings() as db:
        return db.fetchall(query, params)

def fetchone(query, params=None):
    """Returns one row matching the query."""
    with DBSettings() as db:
        return db.fetchone(query, params)
