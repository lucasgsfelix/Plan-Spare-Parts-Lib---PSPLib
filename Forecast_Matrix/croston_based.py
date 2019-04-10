"""Croston Based algorithms and Exponential"""
import sys
import numpy as np
import pandas as pd
sys.path.append("..")
from Bootstrap import bootstrap


def calculate_method_exponential(alfa, data_value, forecast_value):
	"""Calculates the exponential method"""
	return alfa*data_value + (1 -alfa)*forecast_value

class Croston_Based():

	alfa, beta, convergence_value, percentile = 0.1, 0.1,100,10 ## class atributes
	choosen_algorithm, alfa_condition = 'croston', 'fix'
	bootstrap_call = False
	data = pd.DataFrame()

	def croston_main(self, alfa_condition=None, alfa=None, beta=None, data, choosen_algorithm=None, 
							bootstrap_call=None, convergence_value=None, percentile=None):
		"""Call and defines methods
			alfa_condition: fix ou dynamic
			alfa: most be in a range of 0 to 1
			data: the data most be a pandas dataframe
			choosen_algorithm: sba, croston, tsb or exponential
			bootstrap_call: if true call boostrap, but does not work if exponential
			convergence_value: the value of convergence for the bootstrap method, most be in greater than 0
			percentile: defines the percentile for the bootstrap method, most be between 0 ~ 100
		"""
		self.alfa = alfa
		self.beta = beta
		self.data = data
		self.alfa_condition = alfa_condition
		self.choosen_algorithm = choosen_algorithm
		self.bootstrap_call = bootstrap_call
		self.convergence_value = convergence_value
		self.percentile = percentile
		forecast_matrix = np.zeros(shape=data.shape, dtype=np.float64)
		
		for_initial_pass = 0
		if choosen_algorithm.lower() == 'exponential':
			for_initial_pass = 1
		
		if bootstrap_call == True: ### instatiating boostrap object
			bootstrap_obj = bootstrap.Bootstrap(percentile=percentile, convergence_value=self.convergence_value, number_threads=0)
		
		for i in enumerate(data.itertuples()):
			value_q, previous_p, actual_p, previous_z, actual_z = 0,0,0,0,0
			
			for j in range(for_initial_pass, len(i)): 
				
				if data[i][j] == 0:
					if bootstrap_call == True:
						bootstrap_obj.bootstrap_main_init(row = data[i][0:j])
					else:
						if choosen_algorithm.lower() != 'exponential' and choosen_algorithm.lower() != 'tsb':
							previous_p = actual_p
							previous_z = actual_z
							value_q = value_q + 1

						elif choosen_algorithm.lower() == 'tsb':
							actual_p = previous_p + beta * (0 - previous_p)
							actual_z = previous_z
							forecast_matrix[i][j] = actual_z*actual_z

				else:
					if choosen_algorithm.lower() == 'exponential':
						forecast_matrix[i][j] = calculate_method_exponential(alfa, data[i][j], forecast_value[i][j-1])
					elif choosen_algorithm.lower() == 'tsb':
						forecast_matrix[i][j] = tsb_method(data_value, alfa, beta)
					else:
						forecast_matrix[i][j] = self.calculate_method(data[i][j], alfa, value_q)

					if self.alfa_condition.lower() == 'dynamic':
						if choosen_algorithm.lower() == 'tsb':
							alfa, beta = dynamic_alfa_beta(data_value)
						else:
							alfa = self.dynamic_alfa(data[i][j], value_q, forecast_matrix[i][j-1]) ## choosing the best value for alfa
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

	def tsb_method(self, data_value, alfa, beta):
		"""TSB method implementation"""
		actual_p = previous_p + beta * (1-previous_p)
		actual_z = previous_z + alfa * (data_value - previous_z)
		
		return actual_p * actual_z
	
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

	def dynamic_alfa_beta(data_value):

		alfa, beta, flag = 0, 0, 0
		best_alfa, best_beta = 0, 0
		while(alfa<=1):
			beta = 0
			while(beta<=1):
				predicted_value = tsb_method(data_value, alfa, beta)
				error_value = error.simple_error(data_value, dynamic_value)
				
				if flag == 0:	
					aux = error_value
					best_beta = beta
					best_alfa = alfa
					flag = 1
				
				else:
					if aux>error_value:
						error_value = aux
						best_beta = beta
						best_alfa = alfa

				beta = beta + 0.1
			alfa = alfa + 0.1

		return alfa, beta