from Error_Calc import error
from Common import common_methods
import pandas as pd
import numpy as np
from tqdm import tqdm

def calcula_lead_time(lead_time, forecast_matrix, num_colunas):

	m = []
	print("LEAD TIME CALC")
	for index, line in tqdm(enumerate(forecast_matrix.iterrows())):
		l_aux = common_methods.lead_time_calc(lead_time.iloc[index], 
					forecast_matrix.iloc[index])[:num_colunas]
		m.append(l_aux)
		
	lt = pd.DataFrame(m)

	return lt

def print_error(df, forecast_matrix, file_name):
	c =  ["AbsolutePercentage", "Mase", "Absolute Mean",
		"Percentage", "Mean", "Quadratic", "Mean Squared"]
	edf = pd.DataFrame(columns = c)
	print("PRINTING ERROR")
	for index, line in tqdm(enumerate(forecast_matrix.iterrows())):
		err = error.Error(forecast_matrix.iloc[index], df.iloc[index])
		edf.loc[index, "AbsolutePercentage"] = err.absolute_percentage_error()
		edf.loc[index, "Mase"] = err.mase_error()
		edf.loc[index, "Absolute Mean"] = err.absolute_mean_error()
		edf.loc[index, "Percentage"] = err.percentage_error()
		edf.loc[index, "Mean"] = err.mean_error()
		edf.loc[index, "Quadratic"] = err.quadratic_mean_error()
		edf.loc[index, "Mean Squared"] = err.mean_squared_error()



	edf.to_csv("Saida/"+file_name, sep = '\t', index = True)

def print_indicadores(df, for_matrix, estoque, preco, file_name):

	# Custo Medio, Nivel Medio Estque, Fill Rate, Taxa ruptura

	c = ['CV', 'ADI', 'Fill Rate', 'Taxa Ruptura', 'Medio Estoque']
	edf = pd.DataFrame(columns = c)

	cv, adi = [], []
	print("INDIC.")
	for index, _ in tqdm(df.iterrows()):
		cv.append(common_methods.coefficient_of_variation(df.iloc[index]).item())
		adi.append(common_methods.indicator_adi(df.iloc[index]))

	edf['CV'], edf['ADI'] = cv, adi
	fill_r, taxa_rup, me = [], [], []
	for index, _ in tqdm(df.iterrows()):
		fr, ei, tr = common_methods.fill_rate(df.iloc[index], for_matrix.iloc[index], estoque.iloc[index]) # fill rate, estoque intermediario, taxa ruptura
		estoque_intermediario = common_methods.intermediate_cost(estoque[index], for_matrix.iloc[index], df.iloc[index])
		media_estoque = common_methods.mean_stock_level(estoque_intermediario)

		fill_r.append(fr)
		taxa_rup.append(tr)
		me.append(media_estoque)

	edf['Fill Rate'], edf['Taxa Ruptura'], edf['Medio Estoque'] = fill_r, taxa_rup, me

	edf.to_csv("Saida/"+file_name, sep = '\t', index = False)