
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
