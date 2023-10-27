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

    def create_table(self):
        connection = self._get_thread_connection()
        cursor = connection.cursor()
        query = """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                email TEXT,
                password TEXT,
                created_at TIMESTAMP,
                updated_at TIMESTAMP
            )
        """
        cursor.execute(query)
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

    def close_db(self):
        connection = self._get_thread_connection()
        connection.close()
        delattr(threading.current_thread(), "db_connection")
