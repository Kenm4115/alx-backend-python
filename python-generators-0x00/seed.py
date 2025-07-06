
import mysql.connector
import csv
import uuid
from decimal import Decimal

# --- Prototypes ---

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="kenm",
        password="1234"
    )

def create_database(connection):
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
    connection.commit()

def connect_to_prodev():
    return mysql.connector.connect(
        host="localhost",
        user="kenm",
        password="1234",
        database="ALX_prodev"
    )

def create_table(connection):
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_data (
            user_id CHAR(36) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age DECIMAL(5,2) NOT NULL,
            INDEX(user_id)
        )
    """)
    connection.commit()

def insert_data(connection, data):
    cursor = connection.cursor()
    query = """
        INSERT INTO user_data (user_id, name, email, age)
        VALUES (%s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE name=VALUES(name), email=VALUES(email), age=VALUES(age)
    """
    cursor.executemany(query, data)
    connection.commit()

def read_csv_data(file_path):
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            yield (
                str(uuid.uuid4()),       # user_id as UUID
                row['name'],
                row['email'],
                Decimal(row['age'])      # Ensure age is Decimal
            )

def stream_users(connection):
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data")
    for row in cursor:
        yield row

# --- Main process ---

if __name__ == "__main__":
    # Step 1: Connect and create database
    conn = connect_db()
    create_database(conn)
    conn.close()

    # Step 2: Connect to ALX_prodev
    conn_prodev = connect_to_prodev()

    # Step 3: Create user_data table
    create_table(conn_prodev)

    # Step 4: Insert CSV data
    csv_data = list(read_csv_data("user_data.csv"))
    insert_data(conn_prodev, csv_data)

    # Step 5: Stream and print users one by one
    print("Streaming rows:")
    for user in stream_users(conn_prodev):
        print(user)

    conn_prodev.close()
