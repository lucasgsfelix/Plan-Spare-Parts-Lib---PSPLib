import bootstrap
import pandas as pd

class Bootstrap_Main_Method(bootstrap.Bootstrap):


	''' 
	This class will be responsible for calling the bootstrap method in 
	his most classic way, as defined in the original article:
	A new approach to forecasting intermittent demand for service parts inventories from
	Thomas R. Willemain, Charles N. Smart, Henry F. Schwarz
	 '''
	def __init__(self, data, percentile, convergenceValue):
		''' 
		Data has as entry the matrix witch the model will give the prevision
		'''
		self.data = data

		self.percentile = percentile
		self.convergenceValue = convergenceValue


	def bootstrapMain_init(self):

		boot = bootstrap.Bootstrap(percentile = self.percentile, convergenceValue = self.convergenceValue)
		for i in self.data.itertuples(): ### will iterate over each row
			bootstrap.bootstrapInit(i)
			exit()
			



if __name__ == '__main__':
	
	data  = pd.read_table("demanda.txt", delimiter = '\t')
	data.head()
	sis = Bootstrap_Main_Method(data = data, percentile = 10, convergenceValue = 10)
	sis.bootstrapMain_init()













