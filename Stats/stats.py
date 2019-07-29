import statistics
import pandas as pd

class Stats():
	"""Calculate the statistics of a data"""
	header = True
	data = pd.DataFrame()


	def verify_instance(data, header):

		if not isinstance(data, pd.DataFrame):
			if header is True:
				data = pd.DataFrame(data = data[1:len(data)-1], columns = data[0])
			else:
				data = pd.DataFrame(data = data)

		return data

	def calc_stats(self, data, header):

		self.data = verify_instance(data)

		columns = len(data.columns)
		rows = len(data.index) # number of instances
		if columns > 1:
			results = stats(data)
		else:
			results = []
			for column in data:
				results.append(stats(data[column]))

		return results

	def stats(self, data):

		self.extreme_values(extreme = 'Min')
		first_quartile = data.quantile(q = 0.25)
		third_quartile = data.quantile(q = 0.75)
		mean = data.mean()
		variance = data.var()
		std_dev = data.std()
		median = data.median()

		results = [first_quartile, third_quartile, mean, median, variance, std_dev]
		return results

	def extreme_values(self, extreme):
		"""Calculating extremes, min and max"""

		if extreme.lower() == 'min':
			return data.min()
		elif extreme.lower() == 'max':
			return data.max()
		else:
			assert 'Invalid Parameter !'

