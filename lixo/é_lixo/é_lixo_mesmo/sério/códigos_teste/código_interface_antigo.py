from Data_transform.data_transform.services import DataTransformServices

services = DataTransformServices()

# definir arquivo banco de dados
def db_arquive(db_arquive):
    services.db_arquive = db_arquive

# definir arquivo csv
def data_csv_file(data_csv_file):
    services.data_csv_file = data_csv_file

# Definir uma função para converter os valores de uma coluna
def converter_valores(column=None):
    services.converter_column_value(column)

# Função para printar tipos dos dados 
def printar_tipos_de_dados():
    services.contar_tipos_de_dados()

# Função para remover coluna de dataframe
def remover_coluna(name):
    services.remover_coluna(name)

# Função para plotar mapa de correlação
def plotar_mapa_de_correlacao(coluna=None):
    services.plot_correlation_heatmap(coluna)

def printar_primeiras_linhas():
    return

def remover_linhas_arquivo_original():
    return

def renomear_coluna():
    return