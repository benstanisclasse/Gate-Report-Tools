import mysql.connector
from mysql.connector import Error

def test_mysql_connection(host, database, user, password):
    conn = None  # Initialize the connection variable
    try:
        # Establish the connection
        conn = mysql.connector.connect(
            host=host,
            database=database,
            user=user,
            password=password
        )

        # Check if the connection was successful
        if conn.is_connected():
            print("Connection to MySQL server was successful.")
        else:
            print("Connection failed.")

    except Error as e:
        print(f"Error: {e}")
    
    finally:
        # Close the connection if it was established
        if conn is not None and conn.is_connected():
            conn.close()
            print("Connection closed.")

# Connection details
host = '192.168.1.65'
database = 'hospital'
user = 'root'
password = 'Pa55w.rd'

# Test the connection
test_mysql_connection(host, database, user, password)
