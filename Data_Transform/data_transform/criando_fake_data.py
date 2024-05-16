import csv
import numpy as np
import random
import string
from tqdm import tqdm

# Definir o tamanho do conjunto de dados fake
num_rows = 500000

# Abrir o arquivo CSV para escrita
with open('fake_data.csv', 'w', newline='', encoding='utf-16') as csvfile:
    fieldnames = ['ID', 'Nome', 'Idade', 'Salário']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    # Escrever cabeçalho
    writer.writeheader()

    with tqdm(total=num_rows) as pbar:  # Inicializar a barra de progresso
        # Escrever os dados fake
        for i in range(1, num_rows + 1):
            # Gerar dados fake
            ID = i
            Nome = f'Nome{i}'
            Idade = np.random.randint(18, 65)
            Salário = np.random.uniform(1000, 5000)

            # Converter aleatoriamente alguns salários em strings
            if np.random.rand() < 0.1:
                Salário = ''.join(random.choices(string.ascii_letters, k=3))

            # Escrever na linha do CSV
            writer.writerow({'ID': ID, 'Nome': Nome, 'Idade': Idade, 'Salário': Salário})
            pbar.update(1)

print("Dados foram escritos!")
