"""This code is responsible to calculate the error in the forecast methods."""
import math
import numpy as np
import statistics

def simple_error(real_values, forecasted_values):
	"""Simple dif error"""
	return math.fabs(real_values-forecasted_values)

class Error():
	"""This class will be responsible to calculate the error of the forecast methods."""

	def __init__(self, forecasted_values, real_values, round_value = None):
		"""Class constructor."""
		if forecasted_values.size != real_values.size:
			assert("The size of the list most be the same !")
			exit()
		self.forecasted_values = forecasted_values.iloc[:forecasted_values.size-1]
		# the last value is main predicted value for this reason, we don't have any value to compare it
		self.real_values = real_values.iloc[1:]
		# the first value can be remove cause I only can predict after the second value
		self.forecasted_values  = self.forecasted_values.reset_index(drop = True)
		self.real_values = self.real_values.reset_index(drop = True)
		if round_value is None or round_value <= 0:
			self.round_value = 3
		else:
			self.round_value = round_value

	def mase_error(self):
		"""Mase Error."""
		diff_real_forecasted = np.subtract(self.real_values, self.forecasted_values) # et
		diff_real_forecasted = list(map(math.fabs, diff_real_forecasted)) # absolute values
		#sum_values = np.sum(diff_real_forecasted)
		diff_real_real = 0
		aux = []
		diff_aux = []
		j=0
		for k in range(0, len(self.real_values)):
			diff_real_real = 0
			j = k
			for i in range(1, j+1):
				diff_real_real+=math.fabs(self.real_values[i]-self.real_values[i-1])

			if j > 0:
				diff_real_real = diff_real_real/(j)
				try:
					aux.append(diff_real_forecasted[k]/diff_real_real)
				except:
					aux.append(0)
		
		if len(aux) > 0:
			aux = statistics.mean(aux)
		else:
			aux = 0
		return aux

	def absolute_mean_error(self):
		"""Absolute Mean Error."""
		diff = np.subtract(self.real_values, self.forecasted_values)
		diff = list(map(math.fabs, diff)) # absolute values
		return round((np.sum(diff)/(self.real_values.size)), self.round_value)

	def percentage_error(self):
		"""Percentage error. This error doesn't consider zeros."""
		sum_values = 0
		for index, i in enumerate(self.real_values):
			if i != 0:
				sum_values = (((i-self.forecasted_values[index])/i)*100)+sum_values

		if self.real_values[self.real_values!=0].size == 0:
			return 0
		return round(sum_values/self.real_values[self.real_values!=0].size,self.round_value) ### removing the zero values

	def mean_error(self):
		"""Mean Error."""
		diff = np.subtract(self.real_values, self.forecasted_values)
		return round((np.sum(diff)/self.real_values.size), self.round_value)

	def quadratic_mean_error(self):
		"""Quadratic Mean Error."""
		diff = np.subtract(self.real_values, self.forecasted_values)
		quadratic_values = [x**2 for x in diff]
		return round(np.sum(quadratic_values)/(self.real_values.size), self.round_value)

	def mean_squared_error(self):
		"""Mean Squared Error."""
		return round(math.sqrt(self.quadratic_mean_error()), self.round_value)

	def absolute_percentage_error(self):
		"""Absolute Percentage Error."""
		sum_values = 0
		cont = 0
		for index, i in enumerate(self.real_values):
			if i!=0:
				sum_values = math.fabs((((i-self.forecasted_values[index])/i)*100))+sum_values
				cont+=1
		return round(sum_values/(self.real_values.size), self.round_value)

''' 
if __name__ == '__main__':
	
	valores_previstos = np.array([0,1,2,4])
	valores_reais = np.array([0,1,2,4])
	sis = Error(valores_reais, valores_previstos, 3)
	print(sis.mean_squared_error())'''


