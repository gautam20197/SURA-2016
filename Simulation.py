import numpy as np
import random 
import math
from Summary import *
import time

def index2chrom(indices,N):
	chrom=[0]*N
	for i in indices:
		chrom[i]=1
	return chrom

#print("d061\tN="+str(N)+"\tS="+str(len(gold_filtered))+"\tCF="+str(cohesionFactor(index2chrom(convertToChromosome(gold_original))))+"\tRF="+str(readabilityFactor(index2chrom(convertToChromosome(gold_original)))))

pos = []
pos.append([1,2,8,14,16,18,21,22,25,26,27,28,29])
pos.append([1,2,4,6,7,9,11,12])
pos.append([1,2,3,4,5,7,8,10,11])
pos.append([1,2,3,10,14,17,18])
pos.append([1,2,3,4,5,15,16,17,18,19,21,23,24])
pos.append([1,2,3,4,5,6,7,8,9,11,12,13,14,15,16,18,19,21,30,31,32,35])
pos.append([1,2,3,4,5,6,7,8,9,10,11,12,13,16,17,19,20,30,34])
pos.append([1,4,5,8,9,17,18,19])
pos.append([1,3,4,10,11,13,21,37,38])
pos.append([1,6,7,12,13,14,16,17,19,20])
pos.append([1,2,3,10,14,17,18])
pos.append([1,2,3,8,9,19])
pos.append([1,2,5,14,15,24,26,27,28,29,31,32,33])
pos.append([1,2,3,5,10,11,12,13,17,20])
pos.append([1,3,5,8,9,10,11,12,14])
pos.append([1,2,4,7,8,9,10,13])
pos.append([1,2,3,4,5,6,7,8,9,12,14,15,17,18,23,24])
pos.append([1,2,3,4,7,8,9,10,12,13,14,22,24])
pos.append([3,4,6,7,8,9,11,14,15,16,17,18,20,28])
pos.append([1,2,3,5,6,10,11])
pos.append([1,2,3,4,5,6,7,14,15])
pos.append([1,2,3,5,7,10,11,13,14])
pos.append([1,2,3,4,5,6,7,8,9,12,14,15,17,18,23,24])
pos.append([1,2,3,4,5,6,7,8,9,10,11,16,18,19,20,22,25,30])
pos.append([1,2,3,4,7,8,9,10,12,13,14,22,24])
pos.append([3,4,6,7,8,9,11,14,15,16,17,18,20,28])
pos.append([1,2,4,5,6,7,14])
pos.append([1,2,4,7,8,9,10,13])
pos.append([1,2,3,4,5,6,7,8,9,11,12,13,14,15,16,18,19,21,30,31,32,35])
pos.append([1,2,3,4,5,6,7,8,9,10,11,12,13,16,17,19,20,30,34])
pos.append([1,4,5,8,9,17,18,19])
pos.append([1,2,5,10,11])
pos.append([1,2,3,4,5,7,8,10,11])
pos.append([1,6,7,12,13,14,16,17,19,20])
pos.append([1,3,5,8,9,10,11,12,14])

#target = open("observations.txt","a")
#target.write("With N longest path\n")
for i in range(1,36):
	(filtered,original) = extractionFormatted('Documents/'+str(i)+'document.txt') 
	(IndexTerms,Query) = indexTerms(filtered) 
	N = len(filtered) 
	gold = [0]*N
	for j in pos[i-1]:
		gold[j-1]=1
	
	wM = weightMatrix(filtered,N,IndexTerms,filtered)
	(documentMatrix, M) = adjacency(filtered,N,IndexTerms,wM) #This variable stores the adjacency matrix of the document and maximum similarity
	R = maximumReadability(documentMatrix,N) #This variable stores the maximum readability matrix
	centralDocument = centralTheme(wM)
	#trf = themeSimilarity(centralDocument,centralTheme(summaryWeight(gold,wM)))
	summary = []
	positions = [i for i in range(N) if (gold[i]==1)]
	for k in positions:
		summary.append(filtered[k])
	wD = weightMatrix(summary,N,IndexTerms,filtered)
	trf = themeSimilarity(centralDocument,centralTheme(wD))
	print(str(i) + " -" + " Theme Relation is : "+str(trf))

	#queryList = querySimilarity(filtered,IndexTerms,Query,N)
	#target.write("document="+str(i)+"\tN="+str(N)+"\tS="+str(len(pos[i-1]))+"\tCF="+str(cohesionFactor(gold,N,M,documentMatrix))+"\tRF="+str(readabilityFactor(gold,N,documentMatrix,R))+"\n")
	#end = time.time()
	#print(end-start)
#target.close()

"""for i  in range(21,36):
	(filtered,original) = extractionFormatted('documents/'+str(i)+'document.txt')
	(IndexTerms,Query) = indexTerms(filtered)
	N = len(filtered)
	weightMatrix = weightMatrix(filtered,N,IndexTerms)
	(documentMatrix, M) = adjacency(filtered,N,IndexTerms,filtered) #This variable stores the adjacency matrix of the document and maximum similarity
	R = maximumReadability(documentMatrix,N) #This variable stores the maximum readability matrix
	gold = pos[i-1]
	print(i)
	main(20,len(gold),N,M,documentMatrix,R,gold)"""
