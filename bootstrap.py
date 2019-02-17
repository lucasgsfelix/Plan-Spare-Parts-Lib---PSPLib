import numpy as np

class bootstrap(object):

	def __init__(self, data, percentil, convergenceValue): 

		self.data = data
		self.percentil = percentil
		self.convergenceValue = convergenceValue


	def bootstrapMethod(self):

		row = self.data ### the receive data is threated as a row 
		leadTime = np.sum(row)
		transitionBoolArray = self.probabilityTransition(row)
		probabilityMatrix = self.probabilityMatrixCalc(transitionArray)
		probabilityMatrix = np.matmul(probabilityMatrix, probabilityMatrix) ### responsible for multiple the matrixs
		self.transitionCalc(transitionBoolArray, probabilityMatrix)


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

		pass



if __name__ == '__main__':
	
	row = np.array([0,1,2])
	sis = bootstrap(data = row, percentil = 10, convergenceValue = 5)
	sis.bootstrapMethod()

		


				








