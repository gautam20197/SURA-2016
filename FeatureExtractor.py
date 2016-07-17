import nltk 
import string
import re
import math
import operator
import sys
import numpy as np
import os
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords


# This function is used to extract the sentences from a non formatted document
def extraction(document):
	# punkt uses unsupervised learning to learn how to extract sentences
	tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
	f = open(document,'rU')
	docUnform = f.read()
	tokens = nltk.word_tokenize(docUnform) # to remove the extra /n's
	docForm = ' '.join(tokens)
	doc = tokenizer.tokenize(docForm) # Punctuations are still present in the sentences
	sentences = []
	for i in doc:
		i = i.lower()
		# RegexpTokenizer divides a sring into substrings based on alphabetical sequences
		tokenizer = RegexpTokenizer(r'\w+')
		tokens = tokenizer.tokenize(i)
		filtered_words = [w for w in tokens if not w in stopwords.words('english')]
		sentences.append(" ".join(filtered_words))
	f.close()
	return (sentences,doc)

# This function is used to extract the sentences from a formatted document
def extractionFormatted(document):
	f = open(document,'rU')
	docUnform = f.read()
	sentences = docUnform.split("\n")
	filtered = []
	for i in sentences:
		i = i.lower()
		# RegexpTokenizer divides a sring into substrings based on alphabetical sequences
		tokenizer = RegexpTokenizer(r'\w+')
		tokens = tokenizer.tokenize(i)
		filtered_words = [w for w in tokens if not w in stopwords.words('english')]
		filtered.append(" ".join(filtered_words))
	f.close()
	return(filtered,sentences)


# This function takes an list of sentences of a document(without stop words)
# and gives us an list of all the index terms
def indexTerms(document):
	document = ' '.join(document)
	words = nltk.word_tokenize(document)
	freqDist = nltk.FreqDist(words)
	sorted_freqDist = list(reversed(sorted(freqDist.items(), key=operator.itemgetter(1))))
	IndexTerms = [a for (a,b) in sorted_freqDist]
	Query = [b for (a,b) in sorted_freqDist[0:5]]
	return (IndexTerms,Query)


# This function takes a string as an input to return an list of weights of all the terms (only index terms)
def weight(sentence,N,IndexTerms,filtered):
	if(sentence == ''):
		return [0]*len(IndexTerms)
	weights = []
	words = nltk.word_tokenize(sentence)
	freqDist = nltk.FreqDist(words)
	(a,b) = freqDist.most_common(1)[0]
	for i in IndexTerms:
		tf = freqDist[i]/b
		# N has been defined as the number of total sentences
		isf = 0
		if(tf!=0):
			# filtered stores the list of sentences without punctuations and stopwords
			isf = math.log(N/occurence(i,filtered))
		weights.append(tf*isf)
	return weights

# This function returns the number of sentences a given string appears in
def occurence(word,filtered):
	count = 0
	for sentence in filtered:
		if (word in sentence):
			count+=1
	return count

# This function returns the similarity between two sentences s1 and s2 taken as two strings
def similarity(s1,s2,N,IndexTerms,filtered):	
	w1 = weight(s1,N,IndexTerms,filtered)
	w2 = weight(s2,N,IndexTerms,filtered)
	combined = list(zip(w1,w2))
	similarity = 0
	for i in combined:
		(a,b) = i
		similarity = similarity + (a*b) # dot product of the two vectors w1 and w2
	w1 = [w*w for w in w1] 
	total1 = math.sqrt(sum(w1)) # square root of the sum of sqaures of all elements of w1
	w2 = [w*w for w in w2]
	total2 = math.sqrt(sum(w2)) # square root of the sum of sqaures of all elements of w2
	if(total1==0 or total2==0):
		return 0
	return (similarity/(total1*total2))

# This function is used to return the similarity of two given weight lists
def similarityWeights(w1,w2):
	combined = list(zip(w1,w2))
	similarity = 0
	for i in combined:
		(a,b) = i
		similarity = similarity + (a*b) # dot product of the two vectors w1 and w2
	w1 = [w*w for w in w1] 
	total1 = math.sqrt(sum(w1)) # square root of the sum of sqaures of all elements of w1
	w2 = [w*w for w in w2]
	total2 = math.sqrt(sum(w2)) # square root of the sum of sqaures of all elements of w2
	if(total1==0 or total2==0):
		return 0
	return (similarity/(total1*total2))


# This function is used to return the adjacency matrix of the directed acyclic graph of a list of sentences s
def adjacency(s,N,IndexTerms,filtered,weightMatrix):
	try:
		dim = len(s) 
		matrix = [[0 for i in range(dim)] for j in range(dim)] #creates a matrix of dimension dim*dim with each element zero
		max1 = 0 #this variable stores the maximum similarity
		for i in range(dim):
			currentSentence = s[i]
			for j in range((i+1),dim):
				matrix[i][j] = similarityWeights(weightMatrix[i],weightMatrix[j])
				if(max1<matrix[i][j]):
					max1 = matrix[i][j]
		return (matrix,max1)
	except:
		print(i)
		print (currentSentence)
		print("###############")
		print (j)
		print(s[j])

# This function takes the adjacency matrix of the document and returns the maximum readability (uses dynamic programming)
def maximumReadability(matrix,N):
	result = [(N*[0]) for _ in range(N)] #creates a matrix of dimension N*N with each element zero
	for i in range(1,N):
		result[i] = list(result[i-1])
		for j in range(1,i+1):
			for k in range(0,i):
				if((result[i][j])<(result[k][j-1]+ matrix[k][i])):
					result[i][j] = (result[k][j-1]+ matrix[k][i])
	return result

# This function takes the list of sentences of a document and the list of index terms
# and returns the similarity of all the sentences in a list to the query ie 5 most frequent
# index terms
def querySimilarity(filtered,IndexTerms,Query,N):
	queryList = []
	query = []
	freq = sum(Query)
	for i in range(5): #The range is 5 because we want the top five occuring words
		#isf = math.log(N/occurence(IndexTerms[i]))
		query.append(Query[i]/freq)
	w1 = [w*w for w in query] # squares of weights of query
	total1 = math.sqrt(sum(w1))
	for i in filtered:
		similarity = 0
		w2 = weight(i,N,IndexTerms,filtered)
		combined = list(zip(query,w2))
		for (a,b) in combined:
			similarity = similarity + (a*b)
		w2 = [w*w for w in w2]
		total2 = math.sqrt(sum(w2))
		if(total1==0 or total2==0):
			queryList.append(0)
		else:
			queryList.append(similarity/(total1*total2))
	return queryList	

# This function takes an list of sentences and returns the matrix of the weights of all the
# sentences
def weightMatrix(s,N,IndexTerms,filtered):
	w = []
	for i in s:
		w.append(weight(i,N,IndexTerms,filtered))
	return w

# This function takes a matrix of weights of sentences and returns the central theme vector
def centralTheme(matrix):
	l = len(matrix)
	a = np.array(matrix)
	sumOfColumns = a.sum(axis=0)
	central = [i/l for i in list(sumOfColumns)]
	return central

# This function takes all the filtered sentences of the document and the sentiment dictionary
# and returns a list with the sentiment value (ie summation of sentiments of the words of a single 
# sentence) of all the sentences.
def sentiment(afinn,filtered):
	senti = []
	for i in filtered:
		current = i.split(" ")
		total = 0
		for j in current:
			total+=afinn.get(j,0)
		senti.append(total)
	return senti

#targetFile = open(str(i)+".txt","a")
#for i in range(len(original)):
#	targetFile.write(str(i)+". "+original[i]+"\n")
#targetFile.close()

#(IndexTerms,Query) = indexTerms(filtered) #This variable stores the list of all the index terms
#The variable Query stores the frequencies of top five words
#(gold_filtered,gold_original) = extraction('new.txt') #This variable stores the list of sentences of golden summary
#N = len(filtered) #This variable stores the number of sentences 
#(documentMatrix, M) = adjacency(filtered,N,IndexTerms,filtered) #This variable stores the adjacency matrix of the document and maximum similarity
#R = maximumReadability(documentMatrix,N) #This variable stores the maximum readability matrix
#queryList = querySimilarity(filtered,IndexTerms,Query,N)

