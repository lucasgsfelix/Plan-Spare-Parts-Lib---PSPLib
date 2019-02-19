''' Responsible to calling the classic boostrap method '''
import time
import pandas as pd
import numpy as np

import bootstrap

class BootstrapMainMethod(bootstrap.Bootstrap):
	'''This class will be responsible for calling the bootstrap method in 
	his most classic way, as defined in the original article:
	A new approach to forecasting intermittent demand for service parts inventories from
	Thomas R. Willemain, Charles N. Smart, Henry F. Schwarz'''
	def __init__(self, data, percentile, convergence_value):
		'''Data has as entry the matrix witch the model will give the prevision'''
		self.data = data
		self.percentile = percentile
		self.convergence_value = convergence_value

	def bootstrap_main_init(self):
		''' This method is responsible for calling and instatiating the the class Bootstrap '''
		boot = bootstrap.Bootstrap(percentile=self.percentile, convergence_value=self.convergence_value, number_threads=0)
		forecast_matrix = np.empty(shape=self.data.shape, dtype=np.float64)
		for index_i, i in enumerate(self.data.itertuples()): ### will iterate over each row
			for j in range(2, len(i)+1): ### pandas has his index, this way force me to initiate the cont in 2
				forecast_matrix[index_i][j-2] = boot.bootstrapInit(i[0:j])

if __name__ == '__main__':
	
	INICIO = time.time()
	DATA = pd.read_table("demanda.txt", delimiter='\t')
	DATA.head()
	SIS = BootstrapMainMethod(data=DATA, percentile=10, convergence_value=10)
	SIS.bootstrap_main_init()
	FIM = time.time()
	print(FIM-INICIO)