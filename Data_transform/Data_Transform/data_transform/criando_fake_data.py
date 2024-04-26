import pandas as pd
import numpy as np

# Definir o tamanho do conjunto de dados fake
num_rows = 100

# Criar um DataFrame com dados fake
df_fake = pd.DataFrame({
    'ID': np.arange(1, num_rows + 1),  # Coluna de IDs sequenciais
    'Nome': ['Nome' + str(i) for i in range(1, num_rows + 1)],  # Coluna de nomes fake
    'Idade': np.random.randint(18, 65, size=num_rows),  # Coluna de idades fake entre 18 e 64 anos
    'Salário': np.random.uniform(1000, 5000, size=num_rows)  # Coluna de salários fake entre 1000 e 5000
})

# Função para converter aleatoriamente alguns salários em strings
def convert_to_string(salario):
    if np.random.rand() < 0.1:  # Probabilidade de 10% de transformar o salário em string
        return str(salario)+"str"
    else:
        return salario

# Aplicar a função à coluna de salários
df_fake['Salário'] = df_fake['Salário'].apply(convert_to_string)

# Verificar os tipos de dados da coluna 'Salário'
tipos_de_dados = df_fake['Salário'].apply(lambda x: type(x).__name__)

# Imprimir os tipos de dados
print("Tipos de dados da coluna 'Salário':")
print(tipos_de_dados)

# Exportar o DataFrame para um arquivo CSV
df_fake.to_csv('dados_fake.csv', index=False, float_format="%.2f")
