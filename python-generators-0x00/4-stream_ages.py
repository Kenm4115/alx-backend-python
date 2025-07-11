
"""
Objective: to use a generator to compute a memory-efficient aggregate function i.e average age for a large dataset

Instruction:

Implement a generator stream_user_ages() that yields user ages one by one.

Use the generator in a different function to calculate the average age without loading the entire dataset into memory

Your script should print Average age of users: average age

You must use no more than two loops in your script

You are not allowed to use the SQL AVERAGE
"""

import mysql.connector

def stream_user_ages():
    connection = mysql.connector.connect(
        host="localhost",
        user="kenm",
        password="1234",
        database="ALX_prodev"
    )
    cursor = connection.cursor()
    cursor.execute("SELECT age FROM user_data")

    for (age,) in cursor:
        yield float(age)

    cursor.close()
    connection.close()


def compute_average_age():
    total_age = 0
    count = 0

    for age in stream_user_ages():
        total_age += age
        count += 1

    if count == 0:
        print("No users in the database.")
    else:
        average_age = total_age / count
        print(f"Average age of users: {average_age:.2f}")


# Run the computation
if __name__ == "__main__":
    compute_average_age()
