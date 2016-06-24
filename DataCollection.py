import numpy as np
import random  
from Summary import *
import re

pos = []
pos.append([1,2,8,15,16,18,21,22,25,26,27,28,29])
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

def training(indicesOne):
	S=len(indicesOne)	
	chrom=[0]*N
	indices=[x-1 for x in indicesOne]
	for i in indices:
		chrom[i]=1
	others=[x for x in range(N) if(chrom[x]==0)]
	trf = themeSimilarity(centralDocument,centralTheme(summaryWeight(chrom,wm)))
	dataFile.write(str(trf)+","+str(S/N)+","+str(cohesionFactor(chrom,N,M,documentMatrix))+","+str(readabilityFactor(chrom,N,documentMatrix,R))+",1")
	dataFile.write("\n")
	for i in range(1,min(len(indices),len(others))+1):
		indexZero=random.sample(indices,i)
		indexOne=random.sample(others,i)
		for j in indexZero:
			chrom[j]=0
		for j in indexOne:
			chrom[j]=1
		trf = themeSimilarity(centralDocument,centralTheme(summaryWeight(chrom,wm)))
		dataFile.write(str(trf)+","+str(S/N)+","+str(cohesionFactor(chrom,N,M,documentMatrix))+","+str(readabilityFactor(chrom,N,documentMatrix,R))+","+str(precision(chrom,indicesOne)))
		dataFile.write("\n")
		chrom=[0]*N
		for j in indices:
			chrom[j]=1

	for i in range(min(len(indices),len(others))):
		chrom=np.random.permutation(chrom)
		trf = themeSimilarity(centralDocument,centralTheme(summaryWeight(chrom,wm)))
		dataFile.write(str(trf)+","+str(S/N)+","+str(cohesionFactor(chrom,N,M,documentMatrix))+","+str(readabilityFactor(chrom,N,documentMatrix,R))+","+str(precision(chrom,indicesOne)))
		dataFile.write("\n")

dataFile=open("data.txt",'w')
dataFile.truncate()
for it in range(1,21):
	(filtered,original) = extractionFormatted('documents/'+str(it)+'document.txt')
	(IndexTerms,Query) = indexTerms(filtered)
	N = len(filtered)
	(documentMatrix, M) = adjacency(filtered,N,IndexTerms,filtered) #This variable stores the adjacency matrix of the document and maximum similarity
	R = maximumReadability(documentMatrix,N) #This variable stores the maximum readability matrix
	gold = pos[it-1]
	wm=weightMatrix(filtered,N,IndexTerms,filtered)
	centralDocument=centralTheme(wm)
	print(it)
	training(gold)	
dataFile.close()
