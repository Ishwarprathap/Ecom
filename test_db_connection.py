from db_config import get_connection

# Test database connection
try:
    conn = get_connection()
    if conn.is_connected():
        print("Database connected successfully!")
    else:
        print("Connection failed!")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    if 'conn' in locals() and conn.is_connected():
        conn.close()
        print("Database connection closed.")
