import pandas
import seaborn as sns
import matplotlib.pyplot as plt
########################################################################################################################

class DataTransformServices:
    def __init__(self):
        self._data_csv_file = None
        self._column_name = None

    @property
    def data_csv_file(self):
        return self._data_csv_file
    
    @data_csv_file.setter
    def data_csv_file(self, file_path):
        self._data_csv_file = file_path
        self._df = pandas.read_csv(self.data_csv_file)

    @property
    def column_name(self):
        return self._column_name
    
    @column_name.setter
    def column_name(self, name):
        self._column_name = name
    
    def contar_tipos_de_dados(self):
    
        # Verificar o tipo de cada valor na coluna específica
        tipos_de_dados = self._df[self._column_name].apply(lambda x: 'String' if isinstance(x, str) else 'Tipo {}'.format(type(x).__name__))
        
        # Contar quantos são strings e quantos são números
        contagem = tipos_de_dados.value_counts()
        print("Contagem de tipos de dados na coluna '{}':".format(self._column_name))
        print(contagem)
    
    def converter_column_value(self):

        # Definir uma função para converter os valores da coluna Salário
        def converter_valores(valor):
            try:
                return float(valor)
            except ValueError:
                return valor
            
        self._df[self._column_name] = self._df[self._column_name].apply(converter_valores)
        return self._df
    
    def remover_strings(self):

        def tem_string(val):
            return isinstance(val, str)
        
        self._df = self._df[~self._df[self._column_name].apply(tem_string)]
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
