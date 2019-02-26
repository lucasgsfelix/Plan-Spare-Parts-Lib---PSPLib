"""Croston Based algorithms"""
import numpy as np
import pandas as pd
from Error_Calc import error
from Bootstrap import bootstrap
class Croston_Based():

	alfa, data, convergence_value, percentile = 0,0,0,0 ## class atributes
	choosen_algorithm, alfa_condition = 'croston', 'fix' ##
	bootstrap_call = False

	def croston_main(alfa_condition, alfa, data, choosen_algorithm, bootstrap_call, convergence_value, percentile):
		
		self.alfa = alfa ## range 0 ~ 1
		self.data = data ## pandas dataframe
		self.alfa_condition = alfa_condition ## fix ou dynamic
		self.choosen_algorithm = choosen_algorithm ## sba or croston
		self.bootstrap_call = bootstrap_call ## if True, call bootstrap
		self.convergence_value = convergence_value ## convergence value for the bootstrap method
		self.percentile = percentile
		forecast_matriz = np.zeros(shape=data.shape, dtype=np.float64)
		if bootstrap_call == True: ### instatiating boostrap object
			bootstrap_obj = bootstrap.Bootstrap(percentile=percentile, convergence_value=self.convergence_value, number_threads=0)
		for i in enumerate(data.itertuples()):
			value_q, previous_p, actual_p, previous_z, actual_z = 0,0,0,0,0
			for j in range(0, len(i)): 
				if data[i][j] == 0:
					if bootstrap_call == True:
						bootstrap_obj.bootstrap_main_init(row = data[i][0:j])
					else:
						previous_p = actual_p
						previous_z = actual_z
						value_q = value_q + 1
				else:
					forecast_matriz[i][j] = self.calculate_method(data[i][j], alfa, value_q)
					if self.alfa_condition.lower() == 'dynamic':
						alfa = self.dynamic_alfa(data[i][j], value_q) ## choosing the best value for alfa

					value_q = 1

	def calculate_method(self, data_value, alfa, value_q):
		"""Responsible for calculating what is needed"""
		actual_p = previous_p + alfa*float(value_q-previous_p)
		actual_z = previous_z + alfa*(data_value-previous_z)
		if actual_p > 0:
			forecast_value = actual_z/actual_p
		else:
			forecast_value = data_value

		if self.choosen_algorithm.lower() == 'sba': # by default
			forecast_value = (1.0 - (alfa/2))*forecast_value ## sba method

		return forecast_value
	
	def dynamic_alfa(self, value_q, data_value):
		"""Calculates the dynamic alfa value"""
		alfa = 0.1
		smaller_alfa, diff_value, previous_diff = 0
		while(alfa<=1):
			dynamic_value = self.calculate_method(data_value, alfa, value_q)
			diff_value = error.simple_error(data_value, dynamic_value)
			if alfa == 0.1:
				previous_diff = diff_value
				smaller_alfa = 0.1
			else:
				if diff_value < previous_diff:
					smaller_alfa = alfa # smaller alfa is really the alfa with the smaller error
					previous_diff = diff_value
			alfa = alfa + 0.1

		return smaller_alfa

