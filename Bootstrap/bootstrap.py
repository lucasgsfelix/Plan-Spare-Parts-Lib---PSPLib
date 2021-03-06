''' Responsible for all operation of the method.
Can be called by other methods and by the main bootstrap method.'''

import math
import multiprocessing
import random
import numpy as np


def single_probability_calc(probability_list, index_one, index_two):
	'''Calculates the probability of each list, in this fuction is necessary to pass the position of the given list'''
	probability = probability_list[index_one] + probability_list[index_two]

	if probability != 0:
		probability_list[index_one] = float(probability_list[index_one]/probability)
		probability_list[index_two] = float(probability_list[index_two]/probability)

	else:
		probability_list[index_one] = 0
		probability_list[index_two] = 0

	return probability_list

def define_transition_value(probability_one, probability_two, size_bool_array):
		'''Defines a transition value for the calculation'''
		if probability_one == probability_two:
			return random.randint(0, 1)
		aux = 0
		cont = 0
		while(aux != 1 and cont < size_bool_array):
			aux = random.randint(0, size_bool_array-1)
			cont = cont + 1
		if cont == size_bool_array:
			aux = random.randint(0, size_bool_array-1)

		return aux

def probability_matrix_calc(transition_array):
	'''Calculate a Probability Matrix based on the giver transition Array'''
	probability_list = np.zeros(4)
	for i in range(1, transition_array.size):
		if transition_array[i] == 0 and transition_array[i-1] == 0:
			probability_list[0] = probability_list[0] + 1
		elif transition_array[i] == 1 and transition_array[i-1] == 0:
			probability_list[1] = probability_list[1] + 1
		elif transition_array[i] == 0 and transition_array[i-1] == 1:
			probability_list[2] = probability_list[2] + 1
		elif  transition_array[i] == 1 and transition_array[i-1] == 1:
			probability_list[3] = probability_list[3] + 1

	probability_list = single_probability_calc(probability_list, 0, 1)
	probability_list = single_probability_calc(probability_list, 2, 3)

	### Now I have to reshape the list in a way it transforms in a matrix
	probability_list = probability_list.reshape((2, 2))
	return probability_list

def transition_calc(transition_bool_array, probability_matrix):
	'''Calculates the transition boolean value'''
	if len(transition_bool_array) == 0:
		return 0
	elif transition_bool_array.size <= 2:
		return transition_bool_array[0]
	aux_sum = np.sum(transition_bool_array) ## using this approach I avoid recalculation
	if aux_sum == 0:
		return 0
	elif aux_sum == transition_bool_array[transition_bool_array.size-1]:
		return 1
	if transition_bool_array[transition_bool_array.size-1] == 1:
		aux = define_transition_value(probability_matrix[1][0], probability_matrix[1][1], transition_bool_array.size)
	else:
		aux = define_transition_value(probability_matrix[0][0], probability_matrix[0][1], transition_bool_array.size)
	return transition_bool_array[aux]

class Bootstrap():
	'''Main bootstrap class, where is implemented all the necessary methods'''
	row = 0
	percentile_type = 'static'
	convergence_value =  100
	percentile = 10
	def __init__(self, percentile = None, convergence_value = None, number_threads = None):
		'''Initialization method'''
		random.seed()
		self.percentile = percentile or self.percentile
		self.convergence_value = 100 or convergence_value
		self.number_threads = number_threads


	def bootstrap_main_init(self, row, percentile_type = None, percentile = None, last_value = None):

		''' This function will be responsible to initialize the bootstrap method calling it
			will return the value of forecast value given a percentile and the percentile

			last value is the value that we are trying to predict
		'''
		self.percentile_type = percentile_type
		self.row = row
		self.percentile = percentile or self.percentile

		if len(row) == 1:
			return row[0], 0

		if str(type(row)) != "<class 'numpy.ndarray'>": ## casting the value
			self.row = np.array(row)
		forecasted_values = np.zeros(self.convergence_value)
		if self.number_threads == 0 or self.number_threads is None:

			forecasted_values = list(map(self.bootstrap_method, range(self.convergence_value)))
			forecasted_values = np.array(forecasted_values)
		else: ### is not working right
			pool = multiprocessing.Pool(self.number_threads)
			forecasted_values = pool.map(self.bootstrap_method, range(self.convergence_value))
			pool.close()
		forecasted_values = np.sort(forecasted_values)
		percentile_position = self.percentile_calc(forecasted_values.size, self.percentile) ## this part is not working right
		if percentile_type == 'static' or last_value is None:		
			return forecasted_values[percentile_position], self.percentile
		else:# is dynamic
			best_percentile = self.best_percentile_calc(forecasted_values, last_value, self.percentile)
			return forecasted_values[percentile_position], best_percentile




	def best_percentile_calc(self, forecasted_values, last_value, percentile):
		"""Calculing the best percentile position for the next round, dynamic percentile type"""
		percentile, best_last_value, percentile_position_best = 0, 0, 0
		
		while(percentile<=100):
			percentile_position = self.percentile_calc(forecasted_values.size, percentile)
			best_value = math.fabs(last_value - forecasted_values[percentile_position])
			
			if percentile == 0:
				best_last_value = best_value
			else:
				if best_last_value > best_value:
					best_last_value = best_value
					percentile_position_best = percentile_position
					if best_value == 0: # the first best percentile
						break

			percentile = percentile + 10

		return percentile_position_best

	def percentile_calc(self, size_of_array, percentile):
		'''Responsible to return the position in a array of a giver percentile'''
		return int((percentile * size_of_array)/100)-1

	def bootstrap_method(self, arg_void):
		'''This is were the method begins'''
		transition_bool_array = self.probability_transition()
		probability_matrix = probability_matrix_calc(transition_bool_array)
		probability_matrix = np.matmul(probability_matrix,probability_matrix) ### responsible for multiple the matrixs
		transition_value = transition_calc(transition_bool_array, probability_matrix)
		if transition_value == 0:
			return 0
		choosen_value = self.not_null_calc()
		choosen_value = self.jitter_calc(choosen_value)
		return choosen_value

	def probability_transition(self):
		'''Calculate a boolean array that will represent a transition array'''
		transition_array = np.zeros(self.row.size) ### this will be a one dimension array
		for i, element in enumerate(self.row):
			if element > 0:
				transition_array[i] = 1

		return transition_array

	def not_null_calc(self):
		'''Calculates a row without the zeros'''
		self.row = self.row[self.row != 0] ### extracting values not equal to zero
		return self.row[random.randint(0, self.row.size-1)]

	def jitter_calc(self, choosen_value):
		'''Calculates the Jittering of a ChoosenValue'''
		mean = np.mean(self.row[self.row != 0])
		std = np.std(self.row[self.row != 0])
		if std == 0:
			z_value = 0
		else:
			z_value = (choosen_value-mean)/std
		z_value = random.uniform(z_value*-1, z_value) ## example: -1 to 1
		s_value = 1 + int(choosen_value+z_value*math.sqrt(choosen_value))
		if s_value < 0:
			return choosen_value
		return s_value
