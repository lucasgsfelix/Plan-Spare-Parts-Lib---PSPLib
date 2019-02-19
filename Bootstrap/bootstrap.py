import math
import multiprocessing
import random
import numpy as np
class Bootstrap(object):

	def __init__(self, percentile, convergence_value, number_threads): 

		self.percentile = percentile
		self.convergence_value = convergence_value
		self.number_threads = number_threads


	def bootstrapInit(self, row):

		''' This function will be responsible to initialize the bootstrap method calling it
			will return the value of forecast value giver a percentile
		'''

		self.row = row
		if not str(type(self.row)) ==  "<class 'numpy.ndarray'>": ## casting the value
			self.row = np.array(row)
		

		random.seed()
		forecasted_values = np.zeros(self.convergence_value)
		if self.number_threads == 0 or self.number_threads is None:
			map(self.bootstrap_method, range(self.convergence_value))
		else: ### is not working right
			pool = multiprocessing.Pool(self.number_threads)
			forecasted_values = pool.map(self.bootstrap_method, range(self.convergence_value))
			pool.close()

		forecasted_values=np.sort(forecasted_values)
		percentilePosition = self.percentile_calc(forecasted_values.size) ## this part is not working right
	

		return forecasted_values[percentilePosition]

	def percentile_calc(self, size_of_array):

		return int((self.percentile * (size_of_array+1))/100)

	def bootstrap_method(self, arg_void):
		#row = self.data ### the receive data is threated as a row 
		transition_bool_array = self.probability_transition()
		probability_matrix = self.probability_matrix_calc(transition_bool_array)
		probability_matrix = np.matmul(probability_matrix, probability_matrix) ### responsible for multiple the matrixs
		transitionValue = self.transition_calc(transition_bool_array, probability_matrix)
		if transitionValue == 0:
			return 0
		else:
			choosen_value = self.not_null_calc()
			return self.jitter_calc(choosen_value)

	def probability_transition(self):

		transition_array = np.zeros(self.row.size) ### this will be a one dimension array 
		for i, element in enumerate(self.row):
			if element > 0:
				transition_array[i] = 1

		return transition_array

	def probability_matrix_calc(self, transition_array):

		probability_list = np.zeros(4)

		for i in range(1, transition_array.size):

			if transition_array[i] == 0 and transition_array[i-1] == 0 :
				probability_list[0] = probability_list[0] + 1
			elif transition_array[i] == 1 and transition_array[i-1] == 0:
				probability_list[1] = probability_list[1] + 1
			elif transition_array[i] == 0 and transition_array[i-1] == 1:
				probability_list[2] = probability_list[2] + 1
			elif  transition_array[i] == 1 and transition_array[i-1] ==1:
				probability_list[3] = probability_list[3] + 1

		probability_list = self.single_probability_calc(probability_list, 0, 1)
		probability_list = self.single_probability_calc(probability_list, 2, 3)

		### Now I have to reshape the list in a way it transforms in a matrix
		probability_list = probability_list.reshape((2,2))
	
		return probability_list

	def single_probability_calc(self, probability_list, index_one, index_two):

		probability = probability_list[index_one] + probability_list[index_two]

		if probability != 0:
			probability_list[index_one] = float(probability_list[index_one]/probability)
			probability_list[index_two] = float(probability_list[index_two]/probability)

		else:
			probability_list[index_one] = 0
			probability_list[index_two] = 0

		return probability_list

	def transition_calc(self, transition_bool_array, probability_matrix):

		if transition_bool_array.size <=2:
			return transition_bool_array[random.randint(0, transition_bool_array.size-1)]
		else:
			auxSum = np.sum(transition_bool_array) ## using this approach I avoid recalculation
			if auxSum == 0:
				return 0
			elif auxSum == transition_bool_array[transition_bool_array.size-1]:
				return 1
			else:
				if transition_bool_array[transition_bool_array.size-1] == 1:
					aux = self.define_transition_value(probability_matrix[1][0], probability_matrix[1][1], transition_bool_array.size)
				else:
					aux = self.define_transition_value(probability_matrix[0][0], probability_matrix[0][1], transition_bool_array.size)

			return transition_bool_array[aux]

	def define_transition_value(self, probability_one, probability_two, size_bool_array):

		if probability_one == probability_two:
			return random.randint(0, 1)
		else:
			aux = 0
			cont = 0
			while(aux!=1 and cont<size_bool_array):
				aux = random.randint(0, size_bool_array-1)
				cont = cont + 1
			if cont == size_bool_array:
				aux = random.randint(0, size_bool_array-1)

			return aux

	def not_null_calc(self):

		self.row = self.row[self.row !=0] ### extracting values not equal to zero

		return self.row[random.randint(0, self.row.size-1)]

	def jitter_calc(self, choosen_value):

		mean=np.mean(self.row[self.row!=0])
		std=np.std(self.row[self.row!=0])
		if std == 0:z_value = 0
		else:z_value = (choosen_value-mean)/std
		z_value = random.uniform(z_value*-1, z_value) ## example: -1 to 1
		s_value = 1 + int(choosen_value+z_value*math.sqrt(choosen_value))
		if s_value<0:
			return choosen_value
		else:
			return s_value

