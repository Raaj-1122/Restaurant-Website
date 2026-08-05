import sqlite3

conn = sqlite3.connect("restaurant.db")
cursor = conn.cursor()

# Reservations

cursor.execute("""
CREATE TABLE IF NOT EXISTS reservations(
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT,
email TEXT,
phone TEXT,
date TEXT,
time TEXT
)
""")

# Food Items

cursor.execute("""
CREATE TABLE IF NOT EXISTS food_items(
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT,
category TEXT,
price REAL
)
""")

# Orders

cursor.execute("""
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    food_name TEXT NOT NULL,
    customer_name TEXT NOT NULL,
    phone TEXT NOT NULL
)
""")

conn.commit()
conn.close()

print("Database Created Successfully")
