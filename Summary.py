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

# This function takes a chromosome of a summary and returns the weight of the 
# sentences present in the summar from the weight matrix
def summaryWeight(s,weightMatrix):
	matrix =[]
	positions = [i for i in range(len(s)) if (s[i]==1)]
	for i in positions:
		matrix.append(weightMatrix[i])
	return matrix

# This function takes the central theme of the document and the central theme of summary
# and finds the similarity by taking dot product of unti vectors
def themeSimilarity(centralDocument,centralSummary):
	combined = list(zip(centralDocument,centralSummary))
	similarity = 0
	for i in combined:
		(a,b) = i
		similarity = similarity + (a*b) # dot product of the two vectors
	w1 = [w*w for w in centralDocument] 
	#total1 = math.sqrt(sum(w1)) # square root of the sum of sqaures of all elements of centralDocument
	w2 = [w*w for w in centralSummary]
	#total2 = math.sqrt(sum(w2)) # square root of the sum of sqaures of all elements of centralSumaary
	#if(total1==0 or total2==0):
	#		return 0
	return similarity

# This function takes a chromosome and the original document and writes the summary generated 
# into a file in systems which is then used by rouge to find the precision
def writeToFile(s,original,id):
	positions = [i for i in range(len(s)) if(s[i]==1)]
	dataFile = open("systems/"+"d"+id+".txt","w")
	dataFile.truncate()
	dataFile.write("<SUM>")
	dataFile.write("\n")
	for i in positions:
		dataFile.write("<s>")
		dataFile.write(original[i])
		dataFile.write("</s>")
		dataFile.write("\n")
	dataFile.write("</SUM>")
	dataFile.close()

# This function takes a chromosome and then returns the sentence position summation for the 
# sentences present in the summary and normalized by taking the sum of first S sentences position
# importance
def sentencePosition(s):
	positions = [i for i in range(len(s)) if(s[i]==1)]
	total = 0
	N = len(s)
	for i in positions:
		total+= (2*(N-i))/(N*(N+1))
	S = len(positions)
	maximum = 0
	for i in range(S):
		maximum+= (2*(N-i))/(N*(N+1))
	return (total/maximum)

# This function takes a chromosome and the document matrix ie the adjacency matrix of a document
# and gives the aggregate similarity ie the sum of columns of the sentences present in the summary
def aggregateSimilarity(s,documentMatrix,sortedAggregate):
	positions = [i for i in range(len(s)) if(s[i]==1)]
	N = len(s)
	S = len(positions)
	a = np.array(documentMatrix)
	total = 0
	for i in positions:
		total+=sum(a[:,i])
	normalizationFactor = sum(sortedAggregate[:S])
	return (total/normalizationFactor)

# This function returns the number of sentences of the summary which have positive sentiments 
# divided by total number of sentences
def positiveSentiment(s,senti):
	positions = [i for i in range(len(s)) if(s[i]==1)]
	S = len(positions)
	total = 0
	for i in positions:
		if(senti[i]>0):
			total+=1
	return (total/S)

# This function returns the number of sentences of the summary which have negative sentiments 
# divided by total number of sentences
def negativeSentiment(s,senti):
	positions = [i for i in range(len(s)) if(s[i]==1)]
	S = len(positions)
	total = 0
	for i in positions:
		if(senti[i]<0):
			total+=1
	return (total/S)

# This function returns the sum of the absolute sentiment divided by the maximum sum possible
# by taking the sum of the sorted absolute sentiment values upto S
def sentimentFactor(s,senti,abs_senti):
	S = sum(s)
	positions = [i for i in range(len(s)) if(s[i]==1)]
	normalizing = sum(abs_senti[:S])
	total = 0
	for i in positions:
		total += abs(senti[i])
	return (total/normalizing)

# This function returns the number of words in the summary by using the original
# list of sentences
def extractWords(s,original):
	sen = []
	p = [i for i in range(len(s)) if(s[i]==1)]
	for i in p:
		sen.append(original[i])
	words = sum([len(i.split(" ")) for i in sen])
	return words

# This function returns the number of letters in the summary by using the original
# list of sentences
def extractLetters(s,original):
	sen = []
	p = [i for i in range(len(s)) if(s[i]==1)]
	for i in p:
		sen.append(original[i])
	letters = 0
	for i in sen:
		letters+=sum([len(j) for j in i])
	return letters

# This function returns the number of syllables in a word by using cmudict and the 
# process described in the FeatureExtractor below the statement that imports cmudict
def nsyl(word):
	word = word.lower()
	digits = ['0','1','2','3','4','5','6','7','8','9']
	if(syllables.get(word,0)==0):
		return 0
	else:
		return [len(list(y for y in x if (y[-1] in digits))) for x in syllables[word.lower()]][0]

# This function returns the number of syllables in a summary
def extractSyllables(s,original):
	sen = []
	p = [i for i in range(len(s)) if(s[i]==1)]
	for i in p:
		sen.append(original[i])
	syllables = 0
	for i in sen:
		for j in i:
			syllables+=nsyl(j)
	return syllables

# This function is used to find out the number of complex words in the summary.
# We calculate the complex words by counting the words with three or more than three syllables
def complexWords(s,original):
	sen = []
	p = [i for i in range(len(s)) if(s[i]==1)]
	for i in p:
		sen.append(original[i])
	c = 0
	for i in sen:
		for j in i:
			if(nsyl[j]>=3):
				c+=1
	return c

# This function returns the Coleman-liu factor for readability of a summary
def coleman(s,original):
	words = extractWords(s,original)
	letters = extractLetters(s,original)
	sen = sum(s)
	L = (letters/words)*100
	S = (sen/words)*100
	CLI = 0.0588*L-0.296*S-15.8
	return CLI

# This function returns the automated readability index of a summary
def automatedReadability(s,original):
	words = extractWords(s,original)
	letters = extractLetters(s,original)
	sen = sum(s)
	ARI = 4.71*(letters/words)+0.5*(words/sen) - 21.43
	return (int(math.ceil(ARI)))

# This function applies the flesch kincaid readability test and returns the value of reading ease
def flesch(s,original):
	sen = sum(s)
	words = extractWords(s,original)
	syl = extractSyllables(s,original)
	return (206.835-1.015*(words/sen)-84.6*(syl/words))

# This function returns the Gunning Fog Index using complex words extracted using complexWords function
def gunningFog(s,original):
	sen = sum(s)
	words = extractWords(s,original)
	c = complexWords(s,original)
	return (0.4*((words/sen)+100*(c/words)))















