import numpy as np
import random
import math
import multiprocessing
import time
import pandas as pd
class Bootstrap(object):

	def __init__(self, percentile, convergenceValue, numberOfThreads): 

		self.percentile = percentile
		self.convergenceValue = convergenceValue
		self.numberOfThreads = numberOfThreads


	def bootstrapInit(self, row):

		''' This function will be responsible to initialize the bootstrap method calling it
			will return the value of forecast value giver a percentile
		'''

		self.row = row
		if not str(type(self.row)) ==  "<class 'numpy.ndarray'>": ## casting the value
			self.row = np.array(row)
		

		random.seed()
		forecastValues = np.zeros(self.convergenceValue)
		if self.numberOfThreads == 0 or self.numberOfThreads is None:
			map(self.bootstrapMethod, range(self.convergenceValue))
		else: ### is not working right
			pool = multiprocessing.Pool(self.numberOfThreads)
			forecastValues = pool.map(self.bootstrapMethod, range(self.convergenceValue))
			pool.close()

		forecastValues = np.sort(forecastValues)
		percentilePosition = self.percentileCalc(forecastValues.size) ## this part is not working right
	

		return forecastValues[percentilePosition]

	def percentileCalc(self, sizeOfArray):

		return int((self.percentile * (sizeOfArray+1))/100)

	def bootstrapMethod(self, argVoid):
		#row = self.data ### the receive data is threated as a row 
		leadTime = np.sum(self.row)
		transitionBoolArray = self.probabilityTransition()
		probabilityMatrix = self.probabilityMatrixCalc(transitionBoolArray)
		probabilityMatrix = np.matmul(probabilityMatrix, probabilityMatrix) ### responsible for multiple the matrixs
		transitionValue = self.transitionCalc(transitionBoolArray, probabilityMatrix)
		if transitionValue == 0:
			return 0
		else:
			choosenValue = self.notNullCalc()
			return self.JitterCalc(choosenValue)

	def probabilityTransition(self):

		transitionArray = np.zeros(self.row.size) ### this will be a one dimension array 
		for i, element in enumerate(self.row):
			if element > 0:
				transitionArray[i] = 1

		return transitionArray

	def probabilityMatrixCalc(self, transitionArray):

		probabilityList = np.zeros(4)

		for i in range(1, transitionArray.size):

			if transitionArray[i] == 0 and transitionArray[i-1] == 0 :
				probabilityList[0] = probabilityList[0] + 1
			elif transitionArray[i] == 1 and transitionArray[i-1] == 0:
				probabilityList[1] = probabilityList[1] + 1
			elif transitionArray[i] == 0 and transitionArray[i-1] == 1:
				probabilityList[2] = probabilityList[2] + 1
			elif  transitionArray[i] == 1 and transitionArray[i-1] ==1:
				probabilityList[3] = probabilityList[3] + 1

		probabilityList = self.singleProbabilityCalc(probabilityList, 0, 1)
		probabilityList = self.singleProbabilityCalc(probabilityList, 2, 3)

		### Now I have to reshape the list in a way it transforms in a matrix
		probabilityList = probabilityList.reshape((2,2))
	
		return probabilityList

	def singleProbabilityCalc(self, probabilityList, indexOne, indexTwo):

		probability = probabilityList[indexOne] + probabilityList[indexTwo]

		if probability != 0:
			probabilityList[indexOne] = float(probabilityList[indexOne]/probability)
			probabilityList[indexTwo] = float(probabilityList[indexTwo]/probability)

		else:
			probabilityList[indexOne] = 0
			probabilityList[indexTwo] = 0

		return probabilityList

	def transitionCalc(self, transitionBoolArray, probabilityMatrix):

		if transitionBoolArray.size <=2:
			return transitionBoolArray[random.randint(0, transitionBoolArray.size-1)]
		else:
			auxSum = np.sum(transitionBoolArray) ## using this approach I avoid recalculation
			if auxSum == 0:
				return 0
			elif auxSum == transitionBoolArray[transitionBoolArray.size-1]:
				return 1
			else:
				if transitionBoolArray[transitionBoolArray.size-1] == 1:
					aux = self.defineTransitionValue(probabilityMatrix[1][0], probabilityMatrix[1][1], transitionBoolArray.size)
				else:
					aux = self.defineTransitionValue(probabilityMatrix[0][0], probabilityMatrix[0][1], transitionBoolArray.size)

			return transitionBoolArray[aux]

	def defineTransitionValue(self, probabilityOne, probailityTwo, sizeBoolArray):

		if probabilityOne == probailityTwo:
			return random.randint(0, 1)
		else:
			aux = 0
			cont = 0
			while(aux!=1 and cont<sizeBoolArray):
				aux = random.randint(0, sizeBoolArray-1)
				cont = cont + 1
			if cont == sizeBoolArray:
				aux = random.randint(0, sizeBoolArray-1)

			return aux

	def notNullCalc(self):

		self.row = self.row[self.row !=0] ### extracting values not equal to zero

		return self.row[random.randint(0, self.row.size-1)]

	def JitterCalc(self, choosenValue):

		mean = np.mean(self.row[self.row!=0])
		std = np.std(self.row[self.row!=0])
		if std == 0:zValue = 0
		else:zValue = (choosenValue-mean)/std
		zValue = random.uniform(zValue*-1, zValue) ## example: -1 to 1
		sValue = 1 + int(choosenValue+zValue*math.sqrt(choosenValue))
		if sValue<0:
			return choosenValue
		else:
			return sValue

