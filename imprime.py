import time
import pandas as pd
import numpy as np
from Common import common_methods
import impressao as imp


if __name__ == '__main__':
	
	inicio = time.time()
	forecast_matrix = pd.read_table('Saida/matriz_previsao.txt', sep = '\t')
	df = pd.read_table('Data/database_final.csv', sep = '\t')
	lead_time = df['Lead Time']
	estoque = df['EstoqInicial']
	preco = df['Preco']
	df = df.drop(axis = 1, columns = ['Lead Time', 'EstoqInicial', 'Preco'])
	hp = 4 # heating - aquecimento
	corte = 8 # corte da base

	colunas = df.columns
	df_indic = df.drop(axis = 1, columns = [colunas[i] for i in range(0, corte)])
	df_indic = df_indic.reset_index(drop=True)
	fm_indic = forecast_matrix.drop(axis = 1, columns = [str(i) for i in range(0, corte)])
	fm_indic = fm_indic.reset_index(drop=True)


	imp.print_indicadores(df_indic, fm_indic, estoque, preco, "indicadores.txt")

	forecast_matrix.to_csv("Saida/matriz_previsao.txt", sep = '\t', index = False)
	matriz_lead_time = imp.calcula_lead_time(lead_time, forecast_matrix, len(df.columns))
	imp.print_indicadores(df, matriz_lead_time, estoque, preco, "indicadores_leadtime.txt")
	matriz_lead_time.to_csv("Saida/matriz_lead_time.txt", sep = '\t', index = False)

	imp.print_error(df, forecast_matrix, "erro_previsao.txt")
	imp.print_error(df, matriz_lead_time, "erro_leadtime.txt")
	
	forecast_matrix = forecast_matrix.drop(axis = 1, columns = [str(i) for i in range(0, hp-1)])
	forecast_matrix = forecast_matrix.reset_index(drop=True)
	colunas = list(df.columns)[:hp-1]
	df = df.drop(axis = 1, columns = colunas)
	df = df.reset_index(drop=True)

	print("Tempo de execuação: ", time.time()-inicio)
