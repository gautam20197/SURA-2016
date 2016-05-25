import nltk 

def extraction(document):
	f = open(document,'rU')
	docUnform = f.read()
	tokens = nltk.word_tokenize(docUnform)
	docForm = ' '.join(tokens)
	sentences = docForm.split('.')
	return sentences

a = extraction('d061.txt')
print(a[0])