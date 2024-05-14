import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import sqlite3
import csv
import pandas
########################################################################################################################

class DataTransformServices:
    def __init__(self):
        self._db_arquive = None
        self._data_csv_file = None
        self._column_name = None

    @property
    def db_arquive(self):
        return self._db_arquive
    
    @db_arquive.setter
    def db_arquive(self, file_path):
        try:
            self._db_arquive = file_path
            conn = sqlite3.connect(f"{self._db_arquive}")
            conn.close()
        except ValueError:
            raise ValueError("Não foi possível conectar com o banco de dados, aquivo inválido.")


    @property
    def data_csv_file(self):
        return self._data_csv_file
    
    @data_csv_file.setter
    def data_csv_file(self, file_path):
        self._data_csv_file = file_path
        self._df = "pandas.read_csv(self.data_csv_file)"

    @property
    def column_name(self):
        return self._column_name
    
    @column_name.setter
    def column_name(self, name):
        self._column_name = name
    
    def contar_tipos_de_dados(self, column=None):

        if column is not None:
            array_data = {}
            for chunk in pandas.read_csv(self._data_csv_file, chunksize = 1000000):
                tipos_de_dados = chunk[column].apply(lambda x: 'String' if isinstance(x, str) else 'Tipo {}'.format(type(x).__name__))
                array_data[column] = array_data.get(column, pandas.Series()).add(tipos_de_dados.value_counts(), fill_value=0)
                
        if column==None:
            array_data = {}
            for chunk in pandas.read_csv(self._data_csv_file, chunksize = 1000000):
                for column in chunk:
                    tipos_de_dados = chunk[column].apply(lambda x: 'String' if isinstance(x, str) else 'Tipo {}'.format(type(x).__name__))
                    array_data[column] = array_data.get(column, pandas.Series()).add(tipos_de_dados.value_counts(), fill_value=0)

        if array_data:
            contagem = pandas.concat(array_data, ignore_index=False)

        print("Contagem de tipos de dados na coluna:")
        print(contagem)

    
    def converter_column_value(self, column=None):
        conn = sqlite3.connect(self._db_arquive)
        cursor = conn.cursor()

        if column != None:
          cursor.execute('''
          ALTER TABLE dados_fake ADD COLUMN Nova_coluna REAL
          ''')

          cursor.execute(f'''
          UPDATE dados_fake SET Nova_coluna = CASE
                        WHEN {column} LIKE '%[a-zA-Z]%' THEN NULL
                        ELSE CAST({column} AS REAL)
                        END
          ''')

          cursor.execute(f'''
          ALTER TABLE {self._db_arquive} DROP COLUMN {column}
          ''')

          cursor.execute(f'''
          ALTER TABLE {self._db_arquive} RENAME COLUMN Nova_coluna TO {column}
          ''')

          cursor.execute(f'''
          DELETE FROM {self._db_arquive} WHERE {column} = 0.0
          ''')

        # Obtenha os nomes de todas as colunas, exceto a coluna de interesse
        cursor.execute(f'''
            SELECT name FROM pragma_table_info('dados_fake')
        ''')

        colunas = [row[0] for row in cursor.fetchall()]

        for coluna in colunas:
          cursor.execute('''
          ALTER TABLE dados_fake ADD COLUMN Nova_coluna REAL
          ''')

          cursor.execute(f'''
          UPDATE dados_fake SET Nova_coluna = CASE
                        WHEN {coluna} LIKE '%[a-zA-Z]%' THEN NULL
                        ELSE CAST({coluna} AS REAL)
                        END
          ''')

          cursor.execute(f'''
          ALTER TABLE {self._db_arquive} DROP COLUMN {coluna}
          ''')

          cursor.execute(f'''
          ALTER TABLE {self._db_arquive} RENAME COLUMN Nova_coluna TO {coluna}
          ''')

          cursor.execute(f'''
          DELETE FROM {self._db_arquive} WHERE {coluna} = 0.0
          ''')

        conn.commit()
        conn.close()
    
    def remover_strings(self, column):

        def tem_string(val):
            return isinstance(val, str)
        
        self._df = self._df[~self._df[column].apply(tem_string)]
        # print(self._df)
        return self._df
        
    def plot_correlation_heatmap(self):
        try:
            # Calcula a matriz de correlação
            correlacao = self._df.corr()

            # Cria o gráfico de heatmap
            plt.figure(figsize=(10, 8))
            sns.heatmap(correlacao, annot=True, cmap='coolwarm', fmt=".2f")
            plt.title("Heatmap de Correlação")
            plt.show()
        except ValueError as error:
            return error
    
    def remover_coluna(self, column_name):
        # Verifica se a coluna está presente no DataFrame
        if column_name not in self._df.columns:
            for coluna in self._df.columns:
                print(coluna)
            print(f"A coluna '{column_name}' não está presente no DataFrame.")

        # Remove a coluna especificada
        self._df = self._df.drop(column_name, axis=1)
        return self._df
