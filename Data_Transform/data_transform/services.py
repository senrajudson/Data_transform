import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import sqlite3
import csv
import re
import shutil
import os
import chardet
import codecs
from tqdm import tqdm

import logging
logging.basicConfig(level=logging.DEBUG)
########################################################################################################################

class DataTransformServices:
    def __init__(self):
        self._db_arquive = None
        self._data_csv_file = None
        self._tabela = "dados_analise"

    @property
    def db_arquive(self):
        return self._db_arquive
    
    @db_arquive.setter
    def db_arquive(self, file_path):
        try:
            self._db_arquive = file_path
            conn = sqlite3.connect(self._db_arquive)
            conn.close()
        except ValueError:
            raise ValueError("Não foi possível conectar com o banco de dados, aquivo inválido.")

    @property
    def data_csv_file(self):
        return self._data_csv_file
    
    @data_csv_file.setter
    def data_csv_file(self, file_path):

        self._data_csv_file = re.sub(r'\.\w+$', '', file_path)

        # detectar o tipo de encode do arquivo
        def detect_encoding(file_path):
            with open(file_path, 'rb') as f:
                raw_data = f.read()
                result = chardet.detect(raw_data)
                encoding = result['encoding']
                confidence = result['confidence']

            print(f"Os dados são do tipo {encoding} condidence {confidence}")
            return encoding
        
        def convert_encoding(input_file, output_file, input_encoding, output_encoding):
            with codecs.open(input_file, 'r', encoding=input_encoding, errors='ignore') as f_input:
                content = f_input.read()

            with codecs.open(output_file, 'w', encoding=output_encoding) as f_output:
                f_output.write(content)
            
        # # converter o tipo de encode do arquivo
        # def convert_encoding(input_file, output_file, input_encoding, output_encoding):
        #     with open(input_file, 'r', encoding=input_encoding) as file:
        #         content = file.read()

        #     with open(output_file, 'w', encoding=output_encoding) as file:
        #         file.write(content)

        conn = sqlite3.connect(f"{self._data_csv_file}.db")
        cursor = conn.cursor()

        with open(file_path, 'r', newline = '', encoding = 'latin-1') as file:
            csv_reader = csv.reader(file)
            colunas = next(csv_reader)

            sql_create_table = f'''
            CREATE TABLE IF NOT EXISTS {self._tabela} (
            {', '.join([f"{coluna} TEXT" for coluna in colunas])}
            )
            '''

            sql_insert_data = f'''
            INSERT INTO {self._tabela} (
            {', '.join(colunas)}
            ) VALUES (
            {', '.join(['?'] * len(colunas))}
            )
            '''
        
            try:
                cursor.execute(sql_create_table)
                cursor.executemany(sql_insert_data, csv_reader)
                print("encode_type = 'utf-8'")
                
            except:
                print("Os dados não estavam no tipo utf-8")
                encode_type = detect_encoding(file_path)

                if encode_type != 'utf-8':
                    print("encode_type != 'utf-8'")
                    convert_encoding(file_path, file_path, encode_type, 'utf-8')

                # Renomear colunas inválidas
                for i in range(len(colunas)):
                    if not colunas[i].isidentifier():
                        colunas[i] = f'{colunas[i]}{i+1}'

                logging.debug(f'{sql_create_table}')
                cursor.execute(sql_create_table)

                logging.debug(f'{sql_insert_data}')
                cursor.executemany(sql_insert_data, csv_reader)                

        cursor.close()
        conn.commit()
        conn.close()

        # Se a pasta de destino não existir, crie-a
        if not os.path.exists("CACHE_DADOS"):
            os.makedirs("CACHE_DADOS")

        # Move o arquivo para a pasta de destino
        shutil.move(f"{self._data_csv_file}.db", "CACHE_DADOS")

        self._db_arquive = f"CACHE_DADOS/{self._data_csv_file}.db"
        
    
    def contar_tipos_de_dados(self):

        conn = sqlite3.connect(self._db_arquive)
        cursor = conn.cursor()

        cursor.execute(f'''
        PRAGMA table_info('{self._tabela}')
        ''')

        resultados = cursor.fetchall()

        print("""Tipos de dados na coluna:
              
              """)

        for row in resultados:
            print(row)

        cursor.close()
        conn.close()

    def converter_column_value(self, column=None):
        conn = sqlite3.connect(self._db_arquive)
        cursor = conn.cursor()

        if column != None:
          print("Convertendo coluna:")

          cursor.execute(f'''
          ALTER TABLE {self._tabela} ADD COLUMN Nova_coluna REAL
          ''')

          cursor.execute(f'''
          UPDATE {self._tabela} SET Nova_coluna = CASE
                        WHEN {column} LIKE '%[a-zA-Z]%' THEN NULL
                        ELSE CAST({column} AS REAL)
                        END
          ''')

          cursor.execute(f'''
          ALTER TABLE {self._tabela} DROP COLUMN {column}
          ''')

          cursor.execute(f'''
          ALTER TABLE {self._tabela} RENAME COLUMN Nova_coluna TO {column}
          ''')

          cursor.execute(f'''
          DELETE FROM {self._tabela} WHERE {column} = 0.0
          ''')

        # Obtenha os nomes de todas as colunas, exceto a coluna de interesse
        cursor.execute(f'''
            SELECT name FROM pragma_table_info('{self._tabela}')
        ''')

        colunas = [row[0] for row in cursor.fetchall()]

        print("Convertendo colunas:")
        with tqdm(total=len(colunas)) as pbar:

            for coluna in colunas:
                cursor.execute(f'''
                ALTER TABLE {self._tabela} ADD COLUMN Nova_coluna REAL
                ''')

                cursor.execute(f'''
                UPDATE {self._tabela} SET Nova_coluna = CASE
                                WHEN {coluna} LIKE '%[a-zA-Z]%' THEN NULL
                                ELSE CAST({coluna} AS REAL)
                                END
                ''')

                cursor.execute(f'''
                ALTER TABLE {self._tabela} DROP COLUMN {coluna}
                ''')

                cursor.execute(f'''
                ALTER TABLE {self._tabela} RENAME COLUMN Nova_coluna TO {coluna}
                ''')

                cursor.execute(f'''
                DELETE FROM {self._tabela} WHERE {coluna} = 0.0
                ''')

                pbar.update(1)

        cursor.close()
        conn.commit()
        conn.close()
        
    def plot_correlation_heatmap(self, coluna_interesse=None):
        # Conecte-se ao banco de dados
        conn = sqlite3.connect(self._db_arquive)
        cursor = conn.cursor()

        # Obtenha os nomes de todas as colunas, exceto a coluna de interesse
        if coluna_interesse != None:
            cursor.execute(f'''
                SELECT name FROM pragma_table_info('{self._tabela}')
                WHERE name != '{coluna_interesse}'
            ''')
            colunas = [coluna_interesse] + [row[0] for row in cursor.fetchall()]  

        if coluna_interesse == None:
            cursor.execute(f'''
                SELECT name FROM pragma_table_info('{self._tabela}')
            ''')
            colunas = [row[0] for row in cursor.fetchall()]  

        # Execute uma consulta para obter os dados das colunas
        cursor.execute(f'''
            SELECT {', '.join(colunas)} FROM {self._tabela}
        ''')
        dados = cursor.fetchall()

        # Crie uma matriz numpy com os dados
        matriz_dados = np.array(dados)

        # Calcule a matriz de correlação
        matriz_correlacao = np.corrcoef(matriz_dados, rowvar=False)

        # Crie um mapa de calor usando seaborn
        plt.figure(figsize=(10, 8))
        sns.heatmap(matriz_correlacao, annot=True, xticklabels=colunas, yticklabels=colunas, cmap='coolwarm')
        plt.title("Mapa de Correlação")
        plt.show()

        cursor.close()
        conn.close()
    
    def remover_coluna(self, columns_name=None):

        if type(columns_name) == list:
            conn = sqlite3.connect(self._db_arquive)
            cursor = conn.cursor()
            
            for coluna in columns_name:

                cursor.execute(f'''
                ALTER TABLE {self._tabela} DROP COLUMN {coluna}
                ''')

            cursor.close()
            conn.commit()
            conn.close()
            return
            
        if columns_name != None:
            conn = sqlite3.connect(self._db_arquive)
            cursor = conn.cursor()
            cursor.execute(f'''
            ALTER TABLE {self._tabela} DROP COLUMN {columns_name}
            ''')

            cursor.close()
            conn.commit()
            conn.close()
            

