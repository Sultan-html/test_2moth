import sqlite3

class DatabaseManager:
    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = None

    def open_connection(self):
        if self.connection is None:
            self.connection = sqlite3.connect(self.db_name)

    def close_connection(self):
        if self.connection:
            self.connection.close()
            self.connection = None

    def search_user(self, username):
        self.open_connection()
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        self.close_connection()
        return user

    def execute_transaction(self, operations):
        self.open_connection()
        cursor = self.connection.cursor()
        try:
            for op in operations:
                cursor.execute(*op)
            self.connection.commit()
        except Exception:
            self.connection.rollback()
        finally:
            self.close_connection()

