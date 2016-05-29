from FeatureExtractor import *
#from Summary import *

(filtered,original) = extraction('new.txt') #This variable stores the array of sentences 
N = len(filtered) #This variable stores the number of sentences 
(documentMatrix, M) = adjacency(filtered) #This variable stores the adjacency matrix of the document
print(filtered)
print(original)
print(documentMatrix)
print(M)