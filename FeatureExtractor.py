import nltk 
import string
import re
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

a = extraction('d061.txt') #This variable stores the array of sentences 