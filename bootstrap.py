import numpy as np
import random
import math

class bootstrap(object):

	def __init__(self, data, percentil, convergenceValue): 

		self.data = data
		self.percentil = percentil
		self.convergenceValue = convergenceValue


	def bootstrapMethod(self, row):

		#row = self.data ### the receive data is threated as a row 
		leadTime = np.sum(row)
		transitionBoolArray = self.probabilityTransition(row)
		probabilityMatrix = self.probabilityMatrixCalc(transitionBoolArray)
		probabilityMatrix = np.matmul(probabilityMatrix, probabilityMatrix) ### responsible for multiple the matrixs
		transitionValue = self.transitionCalc(transitionBoolArray, probabilityMatrix)
		if transitionValue == 0:
			return 0
		else:
			choosenValue = self.notNullCalc(row)
			return self.JitterCalc(choosenValue, row)

	def probabilityTransition(self, row):

		transitionArray = np.zeros(row.size) ### this will be a one dimension array 
		for i, element in enumerate(row):
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

	def notNullCalc(self, row):

		row = row[row !=0] ### extracting values not equal to zero

		return row[random.randint(0, row.size-1)]

	def JitterCalc(self, choosenValue, row):

		mean = np.mean(row[row!=0])
		std = np.std(row[row!=0])
		if std == 0:zValue = 0
		else:zValue = (choosenValue-mean)/std
		zValue = random.uniform(zValue*-1, zValue) ## example: -1 to 1
		sValue = 1 + int(choosenValue+zValue*math.sqrt(choosenValue))
		if sValue<0:
			return choosenValue
		else:
			return sValue

'''
if __name__ == '__main__':
	
	random.seed()
	row = np.array([0,1,2])
	sis = bootstrap(data = row, percentil = 10, convergenceValue = 5)
	previsto = sis.bootstrapMethod(row) '''

		


				








