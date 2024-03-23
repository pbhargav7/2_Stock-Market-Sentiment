# db_connection.py

import psycopg2

db_params = {
    'dbname': 'postgres',
    'user': 'postgres',
    'password': 'postgres',
    'host': 'localhost',
    'port': 5432
}

def create_db_connection():
    try:
        connection = psycopg2.connect(**db_params)
        return connection
    except Exception as e:
        print(f"Error connecting to the database: {str(e)}")
        return None

def close_db_connection(connection):
    if connection:
        connection.close()