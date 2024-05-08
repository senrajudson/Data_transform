from services import DataTransformServices

services = DataTransformServices()

# definir arquivo para dataframe
def dataframe_csv(csv_file):
    services.data_csv_file = csv_file

# definir coluna que será alterada
def dataframe_coluna(column):
    services.column_name = column

# Definir uma função para converter os valores da coluna Salário
def converter_valores():
    services.converter_column_value()

# Função para printar tipos dos dados 
def printar_tipos_de_dados():
    services.contar_tipos_de_dados()

# Função para remover coluna de dataframe
def remover_coluna():
    services.remover_coluna()

# Função para remover strings
def remover_strings():
    services.remover_strings()

# Função para plotar mapa de correlação
def plotar_mapa_de_correlacao():
    services.plot_correlation_heatmap()


