"""Every class will have access to this.
This common methods and indicators for every code."""

import math
import statistics
import numpy as np
import pandas as pd



def lead_time_calc(lead_value, forecast_line):
	"""Calculate the lead time for a forecast line"""
	forecast_line = _verify_instance(forecast_line)
	lead_value = math.floor(lead_value/30)
	added_values = lead_value*[0]
	if lead_value == 0:
		return list(map(lambda x: x, forecast_line[forecast_line.columns[0]]))

	forecast_line = list(map(lambda x: x, forecast_line[forecast_line.columns[0]]))
	forescast_line = [forecast_line.insert(0, i) for i in added_values]
	return forecast_line

def coefficient_of_variation(forecast_line):
	'''forecast_line cannot have a header'''
	forecast_line = _verify_instance(forecast_line)
	forecast_line = forecast_line[forecast_line != 0]
	mean = forecast_line.mean()
	stdev = forecast_line.std()
	if mean.iloc[0] == 0:
		return 0.0

	return round(stdev/mean, 3)

def indicator_adi(forecast_line):

	forecast_line = _verify_instance(forecast_line)

	non_zeros = forecast_line[forecast_line != 0].count()
	zeros = forecast_line[forecast_line == 0].count()

	return round((zeros.iloc[0])/(non_zeros.iloc[0]), 3)
		
def intermediate_cost(stock, forecast, data):
	
	cost = []
	#print(len(stock.index), len(forecast.index), len(data.index))
	for index in range(1, len(data.index)):
		cost.append(stock + forecast.iloc[index] - float(data.iloc[index-1]))

	return cost

def mean_stock_level(stock):

	return statistics.mean(stock)

def mean_stock_cost(forecast, price):

	return (forecast.sum()/len(forecast.index))*price

def fill_rate(forecast_values, original_values, initial_stock):


	forecast_values = _verify_instance(forecast_values)
	original_values = _verify_instance(original_values)
	original_values = original_values[1:]
	forecast_values = forecast_values[:len(forecast_values.index)-1]
	sub_values = np.subtract(original_values, forecast_values)
	attended_demand, not_attended_demand = 0, 0
	intermediate_stock = np.array([])
	intermediate_stock = np.append(intermediate_stock, initial_stock)

	for index, value in sub_values.iterrows():

		v = value.iloc[0] # getting the only column
		if initial_stock > 0:

			if v > initial_stock:
				not_attended_demand, initial_stock, intermediate_stock  = _not_demand_calc(v, 
										  not_attended_demand, initial_stock, intermediate_stock)
			else:
				attended_demand, initial_stock, intermediate_stock = _demand_calc(v, 
									 attended_demand, initial_stock, intermediate_stock)
		else:
			not_attended_demand, initial_stock, intermediate_stock = _not_demand_calc(v, 
									 not_attended_demand, initial_stock, intermediate_stock)


	sum_values = sum(list(filter(lambda x:x<0, intermediate_stock)))
	y_value = not_attended_demand+attended_demand
	if y_value != 0:
		fill_rate = float(attended_demand/y_value)
	else:
		fill_rate = 0.0
	burst_rate = float(sum_values/len(intermediate_stock))

	
	return round(fill_rate, 3), intermediate_stock, round(burst_rate, 3)

def _not_demand_calc(value, not_attended_demand, initial_stock, intermediate_stock):
	not_attended_demand = not_attended_demand + 1
	initial_stock = initial_stock - value
	intermediate_stock = np.append(intermediate_stock, initial_stock)

	return not_attended_demand, initial_stock, intermediate_stock

def _demand_calc(value, attended_demand, initial_stock, intermediate_stock):
	attended_demand = attended_demand + 1
	initial_stock = initial_stock - value
	intermediate_stock = np.append(intermediate_stock, initial_stock)

	return attended_demand, initial_stock, intermediate_stock

def _verify_instance(line):
	if not isinstance(line, pd.DataFrame):
		line = pd.DataFrame(line)

	return line
