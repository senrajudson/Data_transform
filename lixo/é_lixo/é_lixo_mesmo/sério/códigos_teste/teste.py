from Data_Transform.data_transform.services import DataTransfromServices

data_transform = DataTransfromServices()
data_transform.data_csv_file = "dados_fake.csv"
data_transform.open_csv_file()
data_transform.contar_tipos_de_dados()
data_transform.column_name = "Salário"
data_transform.converter_column_value()
data_transform.contar_tipos_de_dados()