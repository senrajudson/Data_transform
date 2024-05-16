import csv
import sqlite3

conn = sqlite3.connect('db_dados_fake.db')
cursor = conn.cursor()

with open('dados_fake.csv', 'r', newline = '', encoding = 'utf-8') as file:
  csv_reader = csv.reader(file)
  colunas = next(csv_reader)

tabela = "dados_fake"

cursor.execute(f'''
CREATE TABLE IF NOT EXISTS {tabela} (
{', ' .join([f"{coluna} TEXT" for coluna in colunas])}
)

''')

with open ('dados_fake.csv', 'r', newline = '', encoding = 'utf-8') as file:
  csv_reader = csv.reader(file)
  next(csv_reader)
  cursor.executemany(f'''
  INSERT INTO {tabela} (
  {', ' .join(colunas)}
  ) VALUES (
  {', ' .join(['?'] * len(colunas))}
  )

  ''', csv_reader)
  
conn.commit()
conn.close()