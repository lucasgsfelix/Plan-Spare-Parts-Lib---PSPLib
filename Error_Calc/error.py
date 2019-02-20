"""This code is responsible to calculate the error in the forecast methods."""
import math
from operator import sub
import numpy as np

class Error():
	"""This class will be responsible to calculate the error of the forecast methods."""

	def __init__(forecasted_values, real_values, round_value):
		"""Class constructor."""
		if forecasted_values.size != forecast_real.size:
			assert("The size of the list most be the same !")
			exit()
		self.forecasted_values = forecasted_values.delete(forecasted_values.size-1) 
		# the last value is main predicted value for this reason, we don't have any value to compare it
		self.real_values = real_values.delete(0) 
		# the first value can be remove cause I only can predict after the second value
		if round_value is None or round_value == 0:
			self.round_value = 3
		else:
			self.round_value = round_value

	def mase_error(self):
		pass

	def absolute_mean_error(self):
		"""Absolute Mean Error."""
		diff = np.array(map(sub, self.real_values, self.forecasted_values))
		diff = np.array(map(math.abs, diff)) # absolute values
		return round((np.sum(diff)/(self.real_values.size-1)), self.round_value)

	def percentage_error(self):
		"""Percentage error. This error doesn't consider zeros."""
		sum_values = 0
		for index, i in enumerate(self.real_values):
			if i != 0:
				sum_values = (((i-self.forecasted_values[index])/i)*100)+sum_values
		return round(sum_values/self.(real_values[self.real_values!=0]).size,self.round_value) ### removing the zero values

	def mean_error(self):
		"""Mean Error."""
		diff = np.array(map(sub, self.real_values, self.forecasted_values))
		return round((np.sum(diff)/real_values.size-1), self.round_value)

	def quadratic_mean_error(self):
		"""Quadratic Mean Error."""
		diff = np.array(map(sub, self.real_values, self.forecasted_values))
		quadratic_values = np.array(map(**2, diff))
		return np.sum(quadratic_values)/(self.real_values.size-1)

	def mean_squared_error(self):
		"""Mean Squared Error."""
		pass

	def absolute_percentage_error(self):
		"""Absolute Percentage Error."""
		sum_values = 0
		for index, i in enumerate(self.real_values):
			if i!=0:
				sum_values = math.abs((((i-self.forecasted_values[index])/i)*100))+sum_values
		return sum_values/(self.real_values.size-1)




