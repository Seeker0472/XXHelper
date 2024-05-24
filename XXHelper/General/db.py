import sqlite3


def get_connection():
    conn = sqlite3.connect("./main.sqlite")
    return conn.cursor(),conn


def close_connection(cursor):
    cursor.close()
