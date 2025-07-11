
"""
Objective: Create a generator to fetch and process data in batches from the users database

Instructions:

Write a function stream_users_in_batches(batch_size) that fetches rows in batches

Write a function batch_processing() that processes each batch to filter users over the age of25`

You must use no more than 3 loops in your code. Your script must use the yield generator

Prototypes:

def stream_users_in_batches(batch_size)
def batch_processing(batch_size)
"""

import mysql.connector

def stream_users_in_batches(batch_size):
    connection = mysql.connector.connect(
        host="localhost",
        user="kenm",
        password="1234",
        database="ALX_prodev"
    )
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data")

    all_batches = []
    while True:
        batch = cursor.fetchmany(batch_size)
        if not batch:
            break
        yield batch

    cursor.close()
    connection.close()
    return all_batches


def batch_processing(batch_size):
    for batch in stream_users_in_batches(batch_size):
        filtered_batch = [user for user in batch if float(user['age']) > 25]
        yield filtered_batch
