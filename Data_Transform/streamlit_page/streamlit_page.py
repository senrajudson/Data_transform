import streamlit as st
from Data_transform.data_transform import interface
import os

def main():

  st.title("Hello, World!")
  st.write("Este é um aplicativo Streamlit simples que exibe 'Hello, World!'")

  st.title("Selecione a pasta do arquivo de banco de dados")

  # Widget para carregar a pasta
  folder_path = st.file_uploader("Selecione a pasta", type="directory", key="folder_selector")

  if folder_path is not None:
      # Convertendo o caminho da pasta para string
      folder_path_str = os.path.abspath(folder_path.name)

      # Chamar a função da interface com o caminho da pasta
      interface.db_arquive(folder_path_str)

if __name__ == "__main__":
  main()

### streamlit run --server.port 10007 Data_transform/streamlit_page/streamlit_page.py