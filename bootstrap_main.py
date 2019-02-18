import bootstrap

class Bootstrap_main(bootstrap.Bootstrap):
	''' This class will be responsible for calling the bootstrap method in 
	his most classic way, as defined in the original article:
	A new approach to forecasting intermittent demand for service parts inventories from
	Thomas R. Willemain, Charles N. Smart, Henry F. Schwarz0
	 '''
	def __init__(self, data, percentil, convergenceValue):
		bootstrap.Bootstrap(data, percentil, convergenceValue)
	
