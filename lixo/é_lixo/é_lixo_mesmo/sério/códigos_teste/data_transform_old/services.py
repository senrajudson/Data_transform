import pandas

class DataTransfromServices:
    def __init__(self):
        self._data_csv_file = None
        self._column_name = None

    @property
    def data_csv_file(self):
        return self._data_csv_file
    
    @data_csv_file.setter
    def data_csv_file(self, file_path):
        self._data_csv_file = file_path

    @property
    def column_name(self):
        return self._column_name
    
    @column_name.setter
    def column_name(self, name):
        self._column_name = name

    # Definir uma função para converter os valores da coluna Salário
    def converter_salario(valor):
        try:
            return float(valor)
        except ValueError:
            return valor
    
    def contar_tipos_de_dados(self):
    
        # Verificar o tipo de cada valor na coluna específica
        tipos_de_dados = df[self.column_name].apply(lambda x: 'String' if isinstance(x, str) else 'Número {}'.format(type(x).__name__))
        
        # Contar quantos são strings e quantos são números
        contagem = tipos_de_dados.value_counts()
        print("Contagem de tipos de dados na coluna '{}' antes da transformação:".format(self.column_name))
        print(contagem)
        
        # Retornar a contagem
        # return contagem
    

    
    def converter_column_value(self):
        df = pandas.read_csv(self.data_csv_file, converters={"{}".format(self.column_name): self.converter_salario})
        return df

    def open_csv_file(self):
        df = pandas.read_csv(self.data_csv_file)
        # df_depois = pandas.read_csv(data_csv_file, converters={"Salário": self.converter_salario})
        # Chamar a função e imprimir o resultado
        # resultado = self.contar_tipos_de_dados(df, column_name)
        # print("Contagem de tipos de dados na coluna '{}' antes da transformação:".format(column_name))
        # print(resultado)

        # # Chamar a função e imprimir o resultado
        # resultado = self.contar_tipos_de_dados(df_depois, column_name)
        # print("Contagem de tipos de dados na coluna '{}' depois da transformação:".format(column_name))
        # print(resultado)
        return df
    
        # def contar_tipos_de_dados(df):
    #     contagem_total = {}
        
    #     # Iterar sobre cada coluna do DataFrame
    #     for column_name in df.columns:
    #         # Verificar o tipo de cada valor na coluna específica
    #         tipos_de_dados = df[column_name].apply(lambda x: 'String' if isinstance(x, str) else 'Número {}'.format(type(x).__name__))
            
    #         # Contar quantos são strings e quantos são números
    #         contagem = tipos_de_dados.value_counts()
            
    #         # Adicionar a contagem ao dicionário total
    #         contagem_total[column_name] = contagem
        
    #     # Retornar o dicionário de contagens
    #     return contagem_total