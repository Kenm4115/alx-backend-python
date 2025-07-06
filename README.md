# MySQL User Data Seeder & Stream Processor

This project demonstrates efficient data handling from a MySQL database using Python. It includes generators, batching, pagination, and memory-efficient aggregate computations to work with large datasets.

---

## 📚 Objectives

### 1. Seed the Database from CSV (`seed.py`)

- ✅ Connect to the MySQL server.
- ✅ Create database `ALX_prodev` if it doesn't exist.
- ✅ Create table `user_data` with the following schema:
  - `user_id` (UUID, Primary Key, Indexed)
  - `name` (VARCHAR, NOT NULL)
  - `email` (VARCHAR, NOT NULL)
  - `age` (DECIMAL, NOT NULL)
- ✅ Read user data from `user_data.csv`.
- ✅ Insert users into the table.

**Prototype Functions:**

```python
def connect_db()
def create_database(connection)
def connect_to_prodev()
def create_table(connection)
def insert_data(connection, data)

2. Stream Users One by One (0-stream_users.py)
✅ Use a generator to fetch user rows one at a time from the database.

✅ Only one loop allowed.

✅ Uses yield.

Prototype:
python
def stream_users()

3. Batch Processing (1-batch_processing.py)
✅ Stream rows in batches using stream_users_in_batches(batch_size).

✅ Use batch_processing(batch_size) to filter users older than 25.

✅ Uses no more than 3 loops total.

✅ Two versions supported:

Generator version using yield

Return-based version using return (non-generator)

Prototypes:
python
def stream_users_in_batches(batch_size)
def batch_processing(batch_size)

4. Lazy Pagination (2-lazy_paginate.py)
✅ Implement paginate_users(page_size, offset) to fetch paged rows.

✅ Use lazy_paginate(page_size) generator to fetch only when needed.

✅ Only one loop allowed.

✅ Uses yield.

Prototypes:
python
def paginate_users(page_size, offset)
def lazy_paginate(page_size)

5. Memory-Efficient Average (3-average_age.py)
✅ Implement stream_user_ages() generator to stream one age at a time.

✅ Use it in compute_average_age() to calculate average without loading full dataset.

✅ No SQL AVG allowed.

✅ Uses no more than two loops.

✅ Uses yield.

Prototypes:
python
def stream_user_ages()
def compute_average_age()
