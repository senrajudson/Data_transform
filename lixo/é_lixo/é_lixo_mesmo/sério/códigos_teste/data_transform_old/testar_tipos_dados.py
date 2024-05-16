import pandas as pd

def contar_tipos_de_dados(df, column_name):
    
    # Verificar o tipo de cada valor na coluna específica
    tipos_de_dados = df[column_name].apply(lambda x: 'String' if isinstance(x, str) else 'Número {}'.format(type(x).__name__))
    
    # Contar quantos são strings e quantos são números
    contagem = tipos_de_dados.value_counts()
    
    # Retornar a contagem
    return contagem

# Definir uma função para converter os valores da coluna Salário
def converter_salario(valor):
    try:
        return float(valor)
    except ValueError:
        return valor

# Caminho para o arquivo CSV e nome da coluna específica
file_path = 'dados_fake.csv'
column_name = 'Salário'  # Corrigido para 'Salário'

# Ler o arquivo CSV
df_antes = pd.read_csv(file_path)

# Ler o arquivo CSV com o conversor para a coluna 'Salário'
df_depois = pd.read_csv(file_path, converters={"Salário": converter_salario})  # Corrigido para 'Salário'

# # Verificar os tipos de dados da coluna 'Salário'
# tipos_de_dados = df_depois['Salário'].apply(lambda x: type(x).__name__)

# # Imprimir os tipos de dados
# print("Tipos de dados da coluna 'Salário':")
# print(tipos_de_dados)

# Chamar a função e imprimir o resultado
resultado = contar_tipos_de_dados(df_antes, column_name)
print("Contagem de tipos de dados na coluna '{}' antes da transformação:".format(column_name))
print(resultado)

# Chamar a função e imprimir o resultado
resultado = contar_tipos_de_dados(df_depois, column_name)
print("Contagem de tipos de dados na coluna '{}' depois da transformação:".format(column_name))
print(resultado)
