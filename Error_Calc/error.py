"""This code is responsible to calculate the error in the forecast methods."""
import math
from operator import sub
import numpy as np

def simple_error(real_values, forecasted_values):
	"""Simple dif error"""
	return real_values-forecasted_values

class Error():
	"""This class will be responsible to calculate the error of the forecast methods."""

	def __init__(self, forecasted_values, real_values, round_value):
		"""Class constructor."""
		if forecasted_values.size != real_values.size:
			assert("The size of the list most be the same !")
			exit()
		self.forecasted_values = forecasted_values[:forecasted_values.size-1]
		# the last value is main predicted value for this reason, we don't have any value to compare it
		self.real_values = real_values[1:]
		# the first value can be remove cause I only can predict after the second value
		if round_value is None or round_value <= 0:
			self.round_value = 3
		else:
			self.round_value = round_value

	def mase_error(self):
		"""Mase Error."""
		diff_real_real = 0
		for i in range(1, len(self.real_values)):
			diff_real_real = diff_real_real + math.fabs(self.real_values[i]-self.real_values[i-1])
		diff_real_forecasted = np.array(map(sub, self.real_values, self.forecasted_values))
		diff_real_forecasted = np.array(map(math.fabs, diff_real_forecasted)) # absolute values
		sum_values = np.sum(diff_real_forecasted)

		aux_x = (diff_real_real/(real_values.size-1))
		aux_y = (diff_real_forecasted)/(real_values.size-1)

		return round((aux_y/(real_values.size-1)), self.round_value)

	def absolute_mean_error(self):
		"""Absolute Mean Error."""
		diff = np.array(map(sub, self.real_values, self.forecasted_values))
		diff = np.array(map(math.fabs, diff)) # absolute values
		return round((np.sum(diff)/(self.real_values.size-1)), self.round_value)

	def percentage_error(self):
		"""Percentage error. This error doesn't consider zeros."""
		sum_values = 0
		for index, i in enumerate(self.real_values):
			if i != 0:
				sum_values = (((i-self.forecasted_values[index])/i)*100)+sum_values
		return round(sum_values/self.real_values[self.real_values!=0].size,self.round_value) ### removing the zero values

	def mean_error(self):
		"""Mean Error."""
		diff = np.array(map(sub, self.real_values, self.forecasted_values))
		return round((np.sum(diff)/real_values.size-1), self.round_value)

	def quadratic_mean_error(self):
		"""Quadratic Mean Error."""
		diff = np.array(list(map(sub, self.real_values, self.forecasted_values)))
		quadratic_values = [x**2 for x in diff]
		return round(np.sum(quadratic_values)/(self.real_values.size-1), self.round_value)

	def mean_squared_error(self):
		"""Mean Squared Error."""
		return round(math.sqrt(self.quadratic_mean_error()), self.round_value)

	def absolute_percentage_error(self):
		"""Absolute Percentage Error."""
		sum_values = 0
		for index, i in enumerate(self.real_values):
			if i!=0:
				sum_values = math.fabs((((i-self.forecasted_values[index])/i)*100))+sum_values
		return round(sum_values/(self.real_values.size-1), self.round_value)

''' 
if __name__ == '__main__':
	
	valores_previstos = np.array([0,1,2,4])
	valores_reais = np.array([0,1,2,4])
	sis = Error(valores_reais, valores_previstos, 3)
	print(sis.mean_squared_error())'''


