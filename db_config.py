import mysql.connector
from mysql.connector import Error

def get_connection():
    try:
        conn = mysql.connector.connect(
            host="127.0.0.1",
            user="root",  # Replace with your MySQL username
            password="Aimrkoi$295",  # Replace with your MySQL password
            database="ecommerce"
        )
        if conn.is_connected():
            print("Connected to the database")
            return conn
        else:
            return None
    except Error as e:
        print(f"Error: {e}")
        return None
