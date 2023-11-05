import sqlite3
import threading
from app.models.user import User


class DB:
    def __init__(self, db_file: str):
        self.db_file = db_file

    def _get_thread_connection(self):
        if not hasattr(threading.current_thread(), "db_connection"):
            setattr(threading.current_thread(), "db_connection",
                    sqlite3.connect(self.db_file))
        return getattr(threading.current_thread(), "db_connection")

    def create_tables(self):
        connection = self._get_thread_connection()
        cursor = connection.cursor()
        users_table_query = """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                email TEXT,
                password TEXT,
                created_at TIMESTAMP,
                updated_at TIMESTAMP
            )
        """
        transactions_table_query = """
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                type TEXT,
                amount REAL,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        """
        cursor.execute(users_table_query)
        cursor.execute(transactions_table_query)
        connection.commit()

    def insert_user(self, user: User):
        connection = self._get_thread_connection()
        cursor = connection.cursor()
        query = """
            INSERT INTO users (username, email, password, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?)
        """
        values = (user.username, user.email, user.password,
                  user.created_at, user.updated_at)
        cursor.execute(query, values)
        connection.commit()

    def update_user(self, user_id: int, user: User):
        connection = self._get_thread_connection()
        cursor = connection.cursor()
        query = """
            UPDATE users
            SET username = ?, email = ?, password = ?, updated_at = ?
            WHERE id = ?
        """
        values = (user.username, user.email,
                  user.password, user.updated_at, user_id)
        cursor.execute(query, values)
        connection.commit()

    def delete_user(self, user_id: int):
        connection = self._get_thread_connection()
        cursor = connection.cursor()
        query = "DELETE FROM users WHERE id = ?"
        cursor.execute(query, (user_id,))
        connection.commit()

    def get_users(self):
        connection = self._get_thread_connection()
        cursor = connection.cursor()
        query = """
            SELECT id, username, email, created_at, updated_at
            FROM users
        """
        cursor.execute(query)
        users = [User(*row) for row in cursor.fetchall()]
        return users

    def add_transaction(self, user_id: int, transaction_type: str, amount: float):
        connection = self._get_thread_connection()
        cursor = connection.cursor()
        query = "INSERT INTO transactions (user_id, type, amount) VALUES (?, ?, ?)"
        values = (user_id, transaction_type, amount)
        cursor.execute(query, values)
        connection.commit()

    def get_total_transactions(self, user_id: int):
        connection = self._get_thread_connection()
        cursor = connection.cursor()
        query = "SELECT type, SUM(amount) FROM transactions WHERE user_id = ? GROUP BY type"
        cursor.execute(query, (user_id,))
        result = cursor.fetchall()
        return {"user_id": user_id, "total": dict(result)}

    def delete_transaction(self, user_id: int):
        connection = self._get_thread_connection()
        cursor = connection.cursor()
        query = "DELETE FROM transactions WHERE id = ?"
        cursor.execute(query, (user_id,))
        connection.commit()

    def close_db(self):
        connection = self._get_thread_connection()
        connection.close()
        delattr(threading.current_thread(), "db_connection")
