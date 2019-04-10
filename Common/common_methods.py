"""Every class will have acess to this"""
import math

class Common_Methods():

	def lead_time_calc(lead_value, forecast_line):
		
		lead_value = math.floor(lead_value/30)
		added_values = [0 for i in lead_value]
		lead_value = added_values + lead_value