import sqlite3

conn = sqlite3.connect("db_dados_fake.db")
cursor = conn.cursor()

cursor.execute('''
ALTER TABLE dados_fake DROP COLUMN Nova_coluna
''')

cursor.execute('''
ALTER TABLE dados_fake ADD COLUMN Nova_coluna REAL
''')

cursor.execute('''
UPDATE dados_fake SET Nova_coluna = CASE
               WHEN Salário LIKE '%[a-zA-Z]%' THEN 'str'
               ELSE CAST(Salário AS REAL)
               END
''')

cursor.execute('''
ALTER TABLE dados_fake DROP COLUMN Salário
''')

cursor.execute('''
ALTER TABLE dados_fake RENAME COLUMN Nova_coluna TO Salário
''')

conn.commit()

cursor.execute('''
PRAGMA table_info(dados_fake)
''')

resultados = cursor.fetchall()

for row in resultados:
  print(row)

cursor.execute('''
SELECT * FROM dados_fake WHERE Salário IS NULL
''')

resultados = cursor.fetchall()

for row in resultados:
  print(row)

conn.close()