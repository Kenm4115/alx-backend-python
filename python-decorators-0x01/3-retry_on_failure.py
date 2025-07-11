
"""
Objective: create a decorator that manages database transactions by automatically committing or rolling back changes

Instructions:

Complete the script below by writing a decorator transactional(func) that ensures a function running a database operation is wrapped inside a transaction.If the function raises an error, rollback; otherwise commit the transaction.

Copy the with_db_connection created in the previous task into the script
"""

import time
import sqlite3 
import functools

# Decorator to manage DB connection
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper

# Decorator to retry function on failure
def retry_on_failure(retries=3, delay=2):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(1, retries + 1):
                try:
                    print(f"[TRY {attempt}] Attempting to execute {func.__name__}...")
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"[ERROR] Attempt {attempt} failed: {e}")
                    last_exception = e
                    if attempt < retries:
                        time.sleep(delay)
            print(f"[FAILED] All {retries} retries failed.")
            raise last_exception
        return wrapper
    return decorator

@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

# Attempt to fetch users with automatic retry on failure
users = fetch_users_with_retry()
print(users)
