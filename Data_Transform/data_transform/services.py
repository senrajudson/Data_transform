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
import pandas

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
            self._db_arquive = f"CACHE_DADOS/{file_path}"
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
        conn = sqlite3.connect(f"{self._data_csv_file}.db")
        conn.close()
        self.move_csv_file()
    
    def conn_and_cursor(self, db_file):
        self._conn = sqlite3.connect(db_file)
        self._cursor = self._conn.cursor()
        return self._conn

    def close_conn_and_cursor(self):
        self._cursor.close()
        self._conn.commit()
        self._conn.close()

    def open_csv_file(self):

        with open(f"{self._data_csv_file}.csv", 'r', newline = '', encoding = 'latin-1') as file:
            csv_reader = csv.reader(file)
            colunas = next(csv_reader)
            self.sql_create_table_and_insert_data(self.sql_create_table(colunas), self.sql_insert_data(colunas), 
                                                csv_reader, self.sql_create_table(colunas), self.sql_insert_data(colunas))
            
            print("encode_type = 'latin-1'")

    def move_csv_file(self):
        # Se a pasta de destino não existir, crie-a
        if not os.path.exists("CACHE_DADOS"):
            os.makedirs("CACHE_DADOS")

        # Move o arquivo para a pasta de destino
        shutil.move(f"{self._data_csv_file}.db", "CACHE_DADOS")

        self._db_arquive = f"CACHE_DADOS/{self._data_csv_file}.db"

    def sql_create_table(self, colunas):
        # sql para criar tabela
        sql_create_table = f'''
        CREATE TABLE IF NOT EXISTS {self._tabela} (
        {', '.join([f"{coluna} TEXT" for coluna in colunas])}
        )
        '''

        return sql_create_table
    
    def sql_insert_data(self, colunas):
        # sql para inserir dados
        sql_insert_data = f'''
        INSERT INTO {self._tabela} (
        {', '.join(colunas)}
        ) VALUES (
        {', '.join(['?'] * len(colunas))}
        )
        '''

        return sql_insert_data
    
    # função para criar tabela e inserir dados
    def sql_create_table_and_insert_data(self, create_table, insert_data, csv_reader, log_sql_create_table, log_sql_insert_data):

        self.conn_and_cursor(self._db_arquive)

        logging.debug(f'{log_sql_create_table}')
        self._cursor.execute(create_table)
        logging.debug(f'{log_sql_insert_data}')
        self._cursor.executemany(insert_data, csv_reader)

        self.close_conn_and_cursor()
    
    # detectar o tipo de encode do arquivo
    def detect_encoding(self, file_path):
        with open(file_path, 'rb') as f:
            raw_data = f.read()
            result = chardet.detect(raw_data)
            self._encoding = result['encoding']
            confidence = result['confidence']

        print(f"Os dados são do tipo {self._encoding} condidence {confidence}")

        return self._encoding
    
    # converter o encode dos dados
    def convert_encoding(self, input_file, output_file, input_encoding, output_encoding):
        with codecs.open(input_file, 'r', encoding=input_encoding, errors='ignore') as f_input:
            content = f_input.read()

        with codecs.open(output_file, 'w', encoding=output_encoding, errors='ignore') as f_output:
            f_output.write(content)
    
    def contar_tipos_de_dados(self):

        self.conn_and_cursor(self._db_arquive)

        self._cursor.execute(f'''
        PRAGMA table_info('{self._tabela}')
        ''')

        resultados = self._cursor.fetchall()

        print("""Tipos de dados na coluna:
              
              """)

        for row in resultados:
            print(row)

        self.close_conn_and_cursor()

    def converter_column_value(self):

        self.conn_and_cursor(self._db_arquive)

        # Obtenha os nomes de todas as colunas, exceto a coluna de interesse
        self._cursor.execute(f'''
            SELECT name FROM pragma_table_info('{self._tabela}')
        ''')

        colunas = [row[0] for row in self._cursor.fetchall()]

        print("Convertendo colunas:")
        with tqdm(total=len(colunas)) as pbar:

            for coluna in colunas:
                self._cursor.execute(f'''
                ALTER TABLE {self._tabela} ADD COLUMN Nova_coluna REAL
                ''')

                self._cursor.execute(f'''
                UPDATE {self._tabela} SET Nova_coluna = CASE
                                WHEN {coluna} LIKE '%[a-zA-Z]%' THEN NULL
                                ELSE CAST({coluna} AS REAL)
                                END
                ''')

                self._cursor.execute(f'''
                ALTER TABLE {self._tabela} DROP COLUMN {coluna}
                ''')

                self._cursor.execute(f'''
                ALTER TABLE {self._tabela} RENAME COLUMN Nova_coluna TO {coluna}
                ''')

                self._cursor.execute(f'''
                DELETE FROM {self._tabela} WHERE {coluna} = 0.0
                ''')

                pbar.update(1)

        self.close_conn_and_cursor()

    def converter_uma_coluna(self, column=None):
        
        self.conn_and_cursor(self._db_arquive)

        print("Convertendo coluna:")

        self._cursor.execute(f'''
        ALTER TABLE {self._tabela} ADD COLUMN Nova_coluna REAL
        ''')

        self._cursor.execute(f'''
        UPDATE {self._tabela} SET Nova_coluna = CASE
                    WHEN {column} LIKE '%[a-zA-Z]%' THEN NULL
                    ELSE CAST({column} AS REAL)
                    END
        ''')

        self._cursor.execute(f'''
        ALTER TABLE {self._tabela} DROP COLUMN {column}
        ''')

        self._cursor.execute(f'''
        ALTER TABLE {self._tabela} RENAME COLUMN Nova_coluna TO {column}
        ''')

        self._cursor.execute(f'''
        DELETE FROM {self._tabela} WHERE {column} = 0.0
        ''')

        self.close_conn_and_cursor()
        
    def plot_correlation_heatmap(self, coluna_interesse=None):
        
        self.conn_and_cursor(self._db_arquive)

        # Obtenha os nomes de todas as colunas, exceto a coluna de interesse
        if coluna_interesse != None:
            self._cursor.execute(f'''
                SELECT name FROM pragma_table_info('{self._tabela}')
                WHERE name != '{coluna_interesse}'
            ''')
            colunas = [coluna_interesse] + [row[0] for row in self._cursor.fetchall()]  

        if coluna_interesse == None:
            self._cursor.execute(f'''
                SELECT name FROM pragma_table_info('{self._tabela}')
            ''')
            colunas = [row[0] for row in self._cursor.fetchall()]  

        # Execute uma consulta para obter os dados das colunas
        self._cursor.execute(f'''
            SELECT {', '.join(colunas)} FROM {self._tabela}
        ''')
        dados = self._cursor.fetchall()

        # Crie uma matriz numpy com os dados
        matriz_dados = np.array(dados)

        # Calcule a matriz de correlação
        matriz_correlacao = np.corrcoef(matriz_dados, rowvar=False)

        # Crie um mapa de calor usando seaborn
        plt.figure(figsize=(10, 8))
        sns.heatmap(matriz_correlacao, annot=True, xticklabels=colunas, yticklabels=colunas, cmap='coolwarm')
        plt.title("Mapa de Correlação")
        plt.show()

        self.close_conn_and_cursor()

    def remover_coluna(self, columns_name=None):

        self.conn_and_cursor(self._db_arquive)

        self._cursor.execute(f'''
        ALTER TABLE {self._tabela} DROP COLUMN {columns_name}
        ''')

        self.close_conn_and_cursor()

    def remover_colunas(self, columns_name=None):

        self.conn_and_cursor(self._db_arquive)

        for coluna in columns_name:

            self._cursor.execute(f'''
            ALTER TABLE {self._tabela} DROP COLUMN {coluna}
            ''')
            
        self.close_conn_and_cursor()

        ############## ainda não foi testado ################

    def imprimir_primeiras_linhas_do_db(self, num_linhas=10):

        # Executar o SELECT para buscar as primeiras linhas
        query = f"SELECT * FROM {self._tabela} LIMIT {num_linhas}"
        df = pandas.read_sql_query(query, self.conn_and_cursor(self._db_arquive))

        self.close_conn_and_cursor()

        # Imprimir as linhas no formato "pretty"
        print(df.to_string(index=False))
            
    def sql_renomear_coluna(self, coluna, rename):
        self.conn_and_cursor(self._db_arquive)

        self._cursor.execute(f"""
                             ALTER TABLE {self._tabela}
                             RENAME COLUMN {coluna} TO {rename};
        """)

        self.close_conn_and_cursor()

