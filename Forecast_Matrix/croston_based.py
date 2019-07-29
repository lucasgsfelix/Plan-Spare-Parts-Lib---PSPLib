"""Croston Based algorithms and Exponential"""
import sys
import numpy as np
import pandas as pd
sys.path.append("..")
from Bootstrap import bootstrap
from Error_Calc import error
from tqdm import tqdm


def calculate_method_exponential(alfa, data_value, forecast_value):
	"""Calculates the exponential method"""
	return alfa*data_value + (1 -alfa)*forecast_value

class Croston_Based():

	alfa, beta, convergence_value, percentile = 0.1, 0.1,1000,10 ## class atributes
	choosen_algorithm, alfa_condition, beta_condition = 'croston', 'fix', 'fix'
	heating_period = 12
	bootstrap_call = False
	data = pd.DataFrame()

	def croston_main(self, data, alfa_condition=None, beta_condition = None, alfa=None, beta=None, choosen_algorithm=None, 
							bootstrap_call=None, convergence_value=None, percentile=None, heating_period = None):
		"""Call and defines methods
			alfa_condition: fix ou dynamic
			alfa: most be in a range of 0 to 1
			beta_condition: fix ou dynamic
			beta: most be in range of 0 to 1
			data: the data most be a pandas dataframe
			choosen_algorithm: sba, croston, tsb or exponential
			bootstrap_call: if true call boostrap, but does not work if exponential
			convergence_value: the value of convergence for the bootstrap method, most be in greater than 0
			percentile: defines the percentile for the bootstrap method, most be between 0 ~ 100
			heating_period: defines the initialization period
		"""
		self.alfa = alfa or self.alfa
		self.beta = beta or self.beta
		self.data = data
		self.alfa_condition = alfa_condition or self.alfa_condition
		self.beta_condition = beta_condition or self.beta_condition
		self.choosen_algorithm = choosen_algorithm or self.choosen_algorithm
		self.bootstrap_call = bootstrap_call or self.bootstrap_call
		self.convergence_value = convergence_value or self.convergence_value
		self.percentile = percentile or self.percentile
		self.heating_period = heating_period or self.heating_period
		forecast_matrix = np.zeros(shape=data.shape, dtype=np.float64)
		
		for_initial_pass = 0
		if self.choosen_algorithm.lower() == 'exponential':
			for_initial_pass = 1
		
		if self.bootstrap_call == True: ### instatiating boostrap object
			bootstrap_obj = bootstrap.Bootstrap(percentile=self.percentile, convergence_value=self.convergence_value, number_threads=0)
		
		# heating process
		previous_p, previous_z, actual_z, actual_p, value_q = 0.0,0.0,0.0,0.0,0.0
		list_p, list_z, list_q = [], [], []
		for i in range(0, len(data.index)):
			z, p, cont_z, cont_p, value_q = 0.0, 0.0, 0.0, 0.0, 0.0
			for j in range(0, heating_period):
				if data.iloc[i][j] == 0:
					value_q+=1
				else:
					p+=value_q
					z+=data.iloc[i][j]

					if value_q != 0:
						cont_p+=1

					value_q = 1
					cont_z+=1

			if cont_p == 0:
				actual_p = value_q/2
			else:
				actual_p = p/cont_p

			if cont_z == 0:
				actual_z = 1
			else:
				actual_z = z/cont_z

			if self.choosen_algorithm.lower() == 'croston':
				forecast_matrix[i][j] = actual_z/actual_p
			elif self.choosen_algorithm.lower() == 'sba':
				forecast_matrix[i][j] = actual_z/actual_p
				forecast_matrix[i][j] = (1.0 - (self.alfa/2))*forecast_matrix[i][j] ## sba method
			elif self.choosen_algorithm.lower() == 'exponential':
				forecast_matrix[i][j] = self.alfa*data.iloc[i][j] + (1 -self.alfa)*actual_z
			elif self.choosen_algorithm.lower() == 'tsb':
				forecast_matrix[i][j] = actual_z*actual_p

			list_q.append(value_q)
			list_z.append(actual_z)
			list_p.append(actual_p)

		t_actual_p = actual_p
		t_actual_z = actual_z
		t_value_q = value_q


		for_initial_pass = heating_period
		for i in tqdm(range(0, len(data.index))):
			previous_p = list_p[i]
			previous_z = list_z[i]
			value_q = list_q[i]
			for j in (range(for_initial_pass, len(data.iloc[i]))): 
				if data.iloc[i][j] == 0:
					if self.bootstrap_call == True:
						value = bootstrap_obj.bootstrap_main_init(row = data.iloc[i][for_initial_pass:j+1])
						forecast_matrix[i][j] = value[0]
						previous_p = actual_p
						previous_z = actual_z
						value_q = value_q + 1
					else:
						if self.choosen_algorithm.lower() == 'tsb':

							actual_p = previous_p + (self.beta * (0 - previous_p))
							actual_z = previous_z
							previous_p = actual_p
							forecast_matrix[i][j] = actual_z*actual_p

						elif self.choosen_algorithm.lower() != 'exponential':
							previous_p = actual_p
							previous_z = actual_z
							value_q = value_q + 1
							if self.choosen_algorithm.lower() == 'croston':
								forecast_matrix[i][j] = actual_z/actual_p
							else:
								forecast_matrix[i][j] = actual_z/actual_p
								forecast_matrix[i][j] = (1.0 - (self.alfa/2))*forecast_matrix[i][j] ## sba method
						else:

							forecast_matrix[i][j] = calculate_method_exponential(self.alfa, data.iloc[i][j], forecast_matrix[i][j-1])
					
				else:
					if self.choosen_algorithm.lower() == 'exponential':
						forecast_matrix[i][j] = calculate_method_exponential(self.alfa, data.iloc[i][j], forecast_matrix[i][j-1])
					elif self.choosen_algorithm.lower() == 'tsb':
						forecast_matrix[i][j], actual_z, actual_p = self.tsb_method(data.iloc[i][j], self.alfa, self.beta, previous_p, previous_z)
					else: # croston and sba
						forecast_matrix[i][j],actual_p, actual_z = self.calculate_method_croston_based(data.iloc[i][j], self.alfa, value_q, previous_p, previous_z)
					if self.alfa_condition.lower() == 'dynamic':
						if self.choosen_algorithm.lower() == 'tsb':
							self.alfa, self.beta = self.dynamic_alfa_beta(data.iloc[i][j], previous_p, previous_z)
						else:
							self.alfa = self.dynamic_alfa(data.iloc[i][j], value_q, forecast_matrix[i][j-1], previous_p, previous_z) ## choosing the best value for alfa
					value_q = 1
					previous_p = actual_p
					previous_z = actual_z

		return forecast_matrix

	def calculate_method_croston_based(self, data_value, alfa, value_q, previous_p, previous_z):
		"""Responsible for calculating what is needed"""
		actual_p = previous_p + alfa*float(value_q-previous_p)
		actual_z = previous_z + alfa*(data_value-previous_z)
		if actual_p > 0:
			forecast_value = actual_z/actual_p
		else:
			forecast_value = data_value

		if self.choosen_algorithm.lower() == 'sba': # by default croston
			forecast_value = (1.0 - (alfa/2))*forecast_value ## sba method

		return round(forecast_value, 3), actual_p, actual_z

	def tsb_method(self, data_value, alfa, beta, previous_p, previous_z):
		"""TSB method implementation"""
		actual_p = previous_p + (beta * (1-previous_p))
		actual_z = previous_z + alfa * (data_value - previous_z)

		return actual_p * actual_z, actual_z, actual_p
	
	def dynamic_alfa(self, value_q, data_value, forecast_value, previous_p, previous_z):
		"""Calculates the dynamic alfa value"""
		alfa = 0.1
		smaller_alfa, diff_value, previous_diff = 0, 0, 0
		while(alfa<=1):
			if self.choosen_algorithm == 'exponential':
				dynamic_value = calculate_method_exponential(alfa, data_value, forecast_value)
			else:
				dynamic_value = self.calculate_method_croston_based(data_value, alfa, value_q, previous_p, previous_z)
			if isinstance(dynamic_value, float) or isinstance(dynamic_value, int):
				diff_value = error.simple_error(data_value, dynamic_value)
			else: 
				diff_value = error.simple_error(data_value, dynamic_value[0])
			if alfa == 0.1: ### avoiding a array
				previous_diff = diff_value
				smaller_alfa = 0.1
			else:
				#print(alfa, diff_value, previous_diff)
				if diff_value < previous_diff:
					smaller_alfa = alfa # smaller alfa is really the alfa with the smaller error
					previous_diff = diff_value
			alfa = alfa + 0.1

		return smaller_alfa

	def dynamic_alfa_beta(self, data_value, previous_p, previous_z):

		alfa, beta, flag = 0, 0, 0
		best_alfa, best_beta = 0, 0
		while(alfa<=1):
			beta = 0
			while(beta<=1):
				predicted_value, actual_z, actual_p = self.tsb_method(data_value, alfa, beta, previous_p, previous_z)
				error_value = error.simple_error(data_value, predicted_value)
				
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