
"""
Objective: create a generator that streams rows from an SQL database one by one.

Instructions:

In 0-stream_users.py write a function that uses a generator to fetch rows one by one from the user_data table. You must use the Yield python generator

Prototype: def stream_users()
Your function should have no more than 1 loop
"""

import mysql.connector

def stream_users():
    connection = mysql.connector.connect(
        host="localhost",
        user="kenm",
        password="1234",
        database="ALX_prodev"
    )

    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data")

    for row in cursor:
        yield row

    cursor.close()
    connection.close()
