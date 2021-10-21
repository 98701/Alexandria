import sqlite3

# CREATE CONNECTION / DATABASE
# connection = sqlite3.connect("users.db")
# cursor = connection.cursor()
connection2 = sqlite3.connect("users2.db")

# CREATE TABLE
# cursor.execute('CREATE TABLE IF NOT EXISTS users(name TEXT, password TEXT, age INTEGER)')

# ADD DATA
# cursor.execute('INSERT INTO users VALUES("Daniel", "1234", 30)')
# cursor.execute('INSERT INTO users VALUES("Katha", "5678", 27)')
# connection.commit()

# READ
# cursor.execute('SELECT * FROM users')
# result = cursor.fetchall()
# print(result)

# UPDATE
# cursor.execute('UPDATE users SET age = 100')
# connection.commit()

# DELETE
# cursor.execute('DELETE FROM users WHERE name = "Katha"')
# connection.commit()

# cursor.execute('SELECT * FROM users')
# result = cursor.fetchall()
# print(result)

connection2.close()