from FeatureExtractor import *

# This function takes an array of length N which has zeros or ones i.e represents a summary and returns the subgraph from the adjacency matrix of the document
def subgraph(s):
	positions = [i for i in range(N) if(s[i]==1)]
	S = len(positions)
	matrix = [[0 for i in range(S)] for j in range(S)]
	for i in range(S):
		current = positions[i]
		for j in range((i+1),S):
			matrix[i][j] = documentMatrix[current][positions[j]]
	return matrix

# This function takes an array of binary digits representing a summary and returns the Cohesion Factor of the summary
def cohesionFactor(s):
	positions = [i for i in range(N) if(s[i]==1)]
	S = len(positions)
	matrix = subgraph(s)
	rowSum = [sum(i) for i in matrix] #takes the sum of each individual rows and returns the sum in the form of an array
	totalSum = sum(rowSum)
	cohesion = (totalSum*2)/(S*(S-1))
	normalizedCohesion = (math.log(9*cohesion+1)/math.log(9*M+1))
	return normalizedCohesion
