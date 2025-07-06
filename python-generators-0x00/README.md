
# MySQL Seeder for ALX_prodev Database

This script sets up and populates a MySQL database named `ALX_prodev` with user data from a CSV file. It also includes a generator to stream database rows one by one.

---

## 📁 Project Structure

.
├── seed.py # Main script to set up and seed the database
├── user_data.csv # CSV file containing sample user data
└── README.md # This documentation file

yaml
Copy
Edit

---

## ⚙️ Features

- Creates MySQL database `ALX_prodev` if it doesn't exist.
- Creates a `user_data` table with the following fields:
  - `user_id` (UUID, Primary Key, Indexed)
  - `name` (VARCHAR, NOT NULL)
  - `email` (VARCHAR, NOT NULL)
  - `age` (DECIMAL, NOT NULL)
- Populates the table using `user_data.csv`.
- Includes a generator that streams rows one by one from the database.

---

## 🐍 Requirements

- Python 3.x
- MySQL server
- Python packages:
  - `mysql-connector-python`

Install the required package:

```bash
pip install mysql-connector-python