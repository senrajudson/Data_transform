import sqlite3

conn = sqlite3.connect('db_csv_file.db')

cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS usuarios (
               id INTEGER PRIMARY KEY,
               nome TEXT NOT NULL,
               idade INTEGER
               )''')

cursor.execute('''
               INSERT INTO usuarios (nome, idade) VALUES (?, ?)''', ('João', 30))

cursor.execute('''
               INSERT INTO usuarios (nome, idade) VALUES (?, ?)''', ('Maria', 25))

conn.commit()

cursor.execute('''SELECT * FROM usuarios''')

resultados = cursor.fetchall()

print('View do db:')
for row in resultados:
  print(row)

conn.close()

