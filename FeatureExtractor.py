import nltk 
import string
import re
import math
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords

# This function is used to extract the sentences from a document
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
	return (sentences,doc)

# This function takes a string as an input to return an array of weights of all the terms (only index terms)
def weight(sentence):
	weights = []
	words = nltk.word_tokenize(sentence)
	freqDist = nltk.FreqDist(words)
	(a,b) = freqDist.most_common(1)[0]
	for i in words:
		tf = freqDist[i]/b
		# N has been defined below as the number of total sentences
		isf = math.log(N/occurence(i))
		weights.append(tf*isf)
	return weights

# This function returns the number of sentences a given string appears in
def occurence(word):
	count = 0
	for sentence in filtered:
		if (word in sentence):
			count+=1
	return count

# This function returns the similarity between two sentences s1 and s2 taken as two strings
def similarity(s1,s2):
	w1 = weight(s1)
	w2 = weight(s2)
	combined = list(zip(w1,w2))
	similarity = 0
	for i in combined:
		(a,b) = i
		similarity = similarity + (a*b) # dot product of the two vectors w1 and w2
	w1 = [w*w for w in w1] 
	total1 = math.sqrt(sum(w1)) # square root of the sum of sqaures of all elements of w1
	w2 = [w*w for w in w2]
	total2 = math.sqrt(sum(w2)) # square root of the sum of sqaures of all elements of w2
	return (similarity/(total1*total2))

# This function is used to return the adjacency matrix of the directed acyclic graph of an array of sentences s
def adjacency(s):
	dim = len(s) 
	matrix = [[0 for i in range(dim)] for j in range(dim)] #creates a matrix of dimension dim*dim with each element zero
	max = 0 #this variable stores the maximum similarity
	for i in range(dim):
		currentSentence = s[i]
		for j in range((i+1),dim):
			matrix[i][j] = similarity(currentSentence,s[j])
			if(max<matrix[i][j]):
				max = matrix[i][j]
	return (matrix,max)

# This function takes the adjacency matrix of the document and returns the maximum readability (uses dynamic programming)
def maximumReadability(matrix):
	distance = [-1]*N
	distance[0] = 0
	for i in range(N):
		for j in range(i+1,N):
			if(distance[j]<distance[i]+matrix[i][j]):
				distance[j] = distance[i]+matrix[i][j]
	return distance[-1]


(filtered,original) = extraction('d061.txt') #This variable stores the array of sentences 
(gold_filtered,gold_original) = extraction('new.txt') #This variable stores the array of sentences of golden summary
N = len(filtered) #This variable stores the number of sentences 
(documentMatrix, M) = adjacency(filtered) #This variable stores the adjacency matrix of the document and maximum similarity
R = maximumReadability(documentMatrix) #This variable stores the maximum readability
