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
	return sentences

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
	for sentence in a:
		if (word in sentence):
			count+=1
	return count

a = extraction('d061.txt') #This variable stores the array of sentences 
N = len(a) 
print(N)
print(a[0])
print(weight(a[0]))
print(occurence('gilbert'))

