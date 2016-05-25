import nltk 

f = open('d061.txt','rU')
file = f.read()
tokens = nltk.word_tokenize(file)
document = ' '.join(tokens)
sentences = document.split('.')
print(sentences[0])