"""Croston Based algorithms and Exponential"""
import numpy as np
import pandas as pd
from Error_Calc import error
from Bootstrap import bootstrap

def calculate_method_exponential(alfa, data_value, forecast_value):
	"""Calculates the exponential method"""
	return alfa*data_value + (1 -alfa)*forecast_value

class Croston_Based():

	alfa, data, convergence_value, percentile = 0,0,0,0 ## class atributes
	choosen_algorithm, alfa_condition = 'croston', 'fix' ##
	bootstrap_call = False

	def croston_main(alfa_condition, alfa, data, choosen_algorithm, bootstrap_call, convergence_value, percentile):
		"""Call and defines methods"""
		self.alfa = alfa ## range 0 ~ 1
		self.data = data ## pandas dataframe
		self.alfa_condition = alfa_condition ## fix ou dynamic
		self.choosen_algorithm = choosen_algorithm ## sba, croston, exponential
		self.bootstrap_call = bootstrap_call ## if True, call bootstrap
		self.convergence_value = convergence_value ## convergence value for the bootstrap method
		self.percentile = percentile
		forecast_matriz = np.zeros(shape=data.shape, dtype=np.float64)
		
		for_initial_pass = 0
		if choosen_algorithm.lower()==exponential:
			for_initial_pass = 1
		
		if bootstrap_call == True: ### instatiating boostrap object
			bootstrap_obj = bootstrap.Bootstrap(percentile=percentile, convergence_value=self.convergence_value, number_threads=0)
		
		for i in enumerate(data.itertuples()):
			value_q, previous_p, actual_p, previous_z, actual_z = 0,0,0,0,0
			
			for j in range(for_initial_pass, len(i)): 
				
				if data[i][j] == 0:
					if bootstrap_call == True and choosen_algorithm.lower() != 'exponential':
						bootstrap_obj.bootstrap_main_init(row = data[i][0:j])
					else:
						if choosen_algorithm.lower() != 'exponential':
							previous_p = actual_p
							previous_z = actual_z
							value_q = value_q + 1
				else:
					if choosen_algorithm.lower() == 'exponential':
						forecast_matriz[i][j] = calculate_method_exponential(alfa, data[i][j], forecast_value[i][j-1])
					else:
						forecast_matriz[i][j] = self.calculate_method(data[i][j], alfa, value_q)

					if self.alfa_condition.lower() == 'dynamic':
						alfa = self.dynamic_alfa(data[i][j], value_q, forecast_matriz[i][j-1]) ## choosing the best value for alfa
					value_q = 1

	def calculate_method_croston_based(self, data_value, alfa, value_q):
		"""Responsible for calculating what is needed"""
		actual_p = previous_p + alfa*float(value_q-previous_p)
		actual_z = previous_z + alfa*(data_value-previous_z)
		if actual_p > 0:
			forecast_value = actual_z/actual_p
		else:
			forecast_value = data_value

		if self.choosen_algorithm.lower() == 'sba': # by default croston
			forecast_value = (1.0 - (alfa/2))*forecast_value ## sba method

		return forecast_value
	
	def dynamic_alfa(self, value_q, data_value, forecast_value):
		"""Calculates the dynamic alfa value"""
		alfa = 0.1
		smaller_alfa, diff_value, previous_diff = 0
		while(alfa<=1):
			if self.choosen_algorithm == 'exponential':
				dynamic_value = calculate_method_exponential(alfa, data_value, forecast_value)
			else:
				dynamic_value = self.calculate_method_croston_based(data_value, alfa, value_q)
			diff_value = error.simple_error(data_value, dynamic_value)
			if alfa == 0.1: ### avoiding a array
				previous_diff = diff_value
				smaller_alfa = 0.1
			else:
				if diff_value < previous_diff:
					smaller_alfa = alfa # smaller alfa is really the alfa with the smaller error
					previous_diff = diff_value
			alfa = alfa + 0.1

		return smaller_alfa

