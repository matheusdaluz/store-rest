import sqlite3

conn = sqlite3.connect('data.db')

cursor = conn.cursor()

create_table = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)"
cursor.execute(create_table)

create_table = "CREATE TABLE IF NOT EXISTS items (name text, price text)"
cursor.execute(create_table)

cursor.execute("INSERT INTO items values ('cadeira', '34.56')")
conn.commit()
conn.close()