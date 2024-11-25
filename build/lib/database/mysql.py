import mysql.connector
from mysql.connector import Error

class MySQLConnection:
    _instance = None  # To store the singleton instance

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(MySQLConnection, cls).__new__(cls)
        return cls._instance

    def __init__(self, host="localhost", user="root", password="", database="book40"):
        if not hasattr(self, "_connection"):
            try:
                self._connection = mysql.connector.connect(
                    host=host,
                    user=user,
                    password=password,
                    database=database,
                    autocommit=True,
                    consume_results=True
                )
                if self._connection.is_connected():
                    self._cursor = self._connection.cursor()
                    print("Connected to MySQL database")
            except Error as e:
                self._connection = None
                self._cursor = None
                print(f"Error while connecting to MySQL: {e}")

    def get_connection(self):
        return self._connection

    def get_cursor(self):
        return self._cursor

    def close_connection(self):
        if self._connection and self._connection.is_connected():
            self._cursor.close()
            self._connection.close()
            print("MySQL connection closed")
            self._connection = None
            self._cursor = None
