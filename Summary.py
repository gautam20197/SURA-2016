from FeatureExtractor import *

# This function takes an list of length N which has zeros or ones i.e represents a summary and 
# returns the subgraph from the adjacency matrix of the document
def subgraph(s,N,documentMatrix):
	positions = [i for i in range(N) if(s[i]==1)]
	S = len(positions)
	matrix = [[0 for i in range(S)] for j in range(S)]
	for i in range(S):
		current = positions[i]
		for j in range((i+1),S):
			matrix[i][j] = documentMatrix[current][positions[j]]
	return matrix

# This function takes an list of binary digits representing a summary and 
# returns the Cohesion Factor of the summary
def cohesionFactor(s,N,M,documentMatrix):
	positions = [i for i in range(N) if(s[i]==1)]
	S = len(positions)
	matrix = subgraph(s,N,documentMatrix)
	rowSum = [sum(i) for i in matrix] 
	#takes the sum of each individual rows and returns the sum in the form of an list
	totalSum = sum(rowSum)
	cohesion = (totalSum*2)/(S*(S-1))
	normalizedCohesion = (math.log(9*cohesion+1)/math.log(9*M+1))
	return normalizedCohesion

# This function takes an list of binary digits representing a summary and 
# returns the Readability Factor of the summary
def readabilityFactor(s,N,documentMatrix,R):
	readability = 0
	positions = [i for i in range(N) if(s[i]==1)]
	S = len(positions)
	for i in range(S-1):
		readability += documentMatrix[positions[i]][positions[i+1]]
	normalizedReadability = readability/(R[N-1][S-1])
	return normalizedReadability

# This function takes an list of binary digits representing a summary and 
# converts into a string that represents the summary
def convertToText(s,original):
	positions = [i for i in range(N) if(s[i]==1)]
	summary = []
	S = len(positions)
	for i in positions:
		summary.append(original[i])
	return (' '.join(summary))

# This function takes an list of binary digits representing a summary and also 
# the original list of sentences of the golden summary and returns the precision
def precision_old(s,N,gold_original,original):
	positions = [i for i in range(N) if(s[i]==1)]
	summary = []
	S = len(positions)
	for i in positions:
		summary.append(original[i])
	common_sentences = list(set(summary).intersection(gold_original))
	return(len(common_sentences)/len(summary))

# This function takes a chromosome and the positions of sentences in the ideal 
# summary and returns the precision
def precision(chrom,positions):
	position = [(i+1) for i in range(len(chrom)) if(chrom[i]==1)]
	common = list(set(positions).intersection(position))
	return(len(common)/len(positions))

# This function takes a summary in the form of a list of strings(sentences) and 
# returns an int list of the positions of the sentences in the document
def convertToChromosome(summary,original):
	positions = []
	for i in summary:
		positions.append(original.index(i))
	return positions

# This function takes an list of binary digits representing a summary and  
# returns the Topic Relation Factor of the summary
def topicRelationFactor(s,N,queryList):
	positions = [i for i in range(N) if (s[i]==1) ]
	relation = 0
	for i in positions:
		relation+= queryList[i]
	S = len(positions)
	duplicate = list(queryList)
	duplicate = list(reversed(duplicate.sort()))
	duplicate = duplicate[:S]
	maximum = sum(duplicate)
	return (relation/maximum)

# This function takes a list of positions in integer form and then computes readability
# based on the order of these positions (not being used)
def readabilityFactor2(positions,N,documentMatrix):
	readability = 0
	S = len(a)
	for i in range(S-1):
		readability += documentMatrix[a[i]][a[i+1]]
	normalizedReadability = readability/(R[N-1][S-1])
	return normalizedReadability

# This function takes the central theme of the document and the central theme of summary
# and finds the similarity by taking dot product of unti vectors
def themeSimilarity(centralDocument,centralSummary):
	combined = list(zip(centralDocument,centralSummary))
	similarity = 0
	for i in combined:
		(a,b) = i
		similarity = similarity + (a*b) # dot product of the two vectors
	w1 = [w*w for w in centralDocument] 
	total1 = math.sqrt(sum(w1)) # square root of the sum of sqaures of all elements of centralDocument
	w2 = [w*w for w in centralSummary]
	total2 = math.sqrt(sum(w2)) # square root of the sum of sqaures of all elements of centralSumaary
	if(total1==0 or total2==0):
		return 0
	return (similarity/(total1*total2))







