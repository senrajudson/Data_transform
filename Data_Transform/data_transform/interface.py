from Data_transform.data_transform.services import DataTransformServices

services = DataTransformServices()

# definir arquivo banco de dados
def db_arquive(db_arquive):
    services.db_arquive = db_arquive

# definir arquivo csv
def data_csv_file(data_csv_file):
    services.data_csv_file = data_csv_file

    try:
        # abrir o csv em latin-1
        services.open_csv_file()
    except:
        # o encode não estava em latin-1, converter para latin-1
        services.detect_encoding(f"{services._data_csv_file}.csv")
        services.convert_encoding(f"{services._data_csv_file}.csv", f"{services._data_csv_file}.csv", services._encoding, 'latin-1')
    finally:
        # abrir o csv em latin-1
        services.open_csv_file()

# Definir uma função para converter os valores de uma coluna
def converter_valores(column=None):
    # column = uma coluna
    if column != None:
        services.converter_uma_coluna()

        return
    # todas as colunas
    services.converter_column_value()

# Função para printar tipos dos dados 
def printar_tipos_de_dados():
    services.contar_tipos_de_dados()

# Função para remover coluna de dataframe
def remover_coluna(name):
    # remover = uma lista
    if type(name) == list:
        services.remover_colunas(name)

        return
    # remover = uma coluna
    services.remover_coluna(name)

# Função para plotar mapa de correlação
def plotar_mapa_de_correlacao(coluna=None):
    services.plot_correlation_heatmap(coluna)

######## possíveis new features (ainda não testadas) ##########
def printar_primeiras_linhas(num_linhas):
    services.imprimir_primeiras_linhas_do_db(num_linhas)

def remover_linhas_arquivo_original():
    return

def renomear_coluna(coluna, rename):
    services.sql_renomear_coluna(coluna, rename)