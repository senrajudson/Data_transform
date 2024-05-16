from Data_transform.data_transform import interface

interface.data_csv_file("fake_data.csv")
interface.printar_tipos_de_dados()
interface.remover_coluna(["ID", "Nome"])
interface.printar_tipos_de_dados()
interface.converter_valores()
interface.plotar_mapa_de_correlacao("Salário")