from Data_transform.data_transform.services import DataTransformServices

services = DataTransformServices()

# definir arquivo banco de dados
def db_arquive(db_arquive):
    services.db_arquive = db_arquive

# definir arquivo csv
def data_csv_file(data_csv_file):
    
    try:
        services.data_csv_file = data_csv_file
        services.open_csv_file()

    except:
        services.detect_encoding(f"{services._data_csv_file}.csv")
        services.convert_encoding(f"{services._data_csv_file}.csv", f"{services._data_csv_file}.csv", services._encoding, 'latin-1')
        services.open_csv_file()

    services.move_csv_file()

# Definir uma função para converter os valores de uma coluna
def converter_valores(column=None):
    if column != None:
        services.converter_uma_coluna()

        return
    
    services.converter_column_value()

# Função para printar tipos dos dados 
def printar_tipos_de_dados():
    services.contar_tipos_de_dados()

# Função para remover coluna de dataframe
def remover_coluna(name):
    services.remover_coluna(name)

# Função para plotar mapa de correlação
def plotar_mapa_de_correlacao(coluna=None):
    services.plot_correlation_heatmap(coluna)


### possíveis new features
def printar_primeiras_linhas():
    return

def remover_linhas_arquivo_original():
    return

def renomear_coluna():
    return