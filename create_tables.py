import sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()
# create_table = "CREATE TABLE IF NOT EXISTS users(username text,password text,consent Integer)"
# cursor.execute(create_table)

insert_query = "INSERT INTO users values(?,?,?)"
cursor.execute(insert_query, ("nitesh", "qwerty", None))

connection.commit()
connection.close()
