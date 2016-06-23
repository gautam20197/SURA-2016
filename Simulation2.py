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

i=67
start = time.time()
(filtered,original) = extraction('Documents2/d0'+str(i)+'.txt') 
(IndexTerms,Query) = indexTerms(filtered) 
(gold_filtered,gold_original) = extraction('Summaries/d0'+str(i)+'_400.txt')
#print([original[i] for i in range(len(filtered)) if(len(filtered[i])==3)])


N = len(filtered) 
(documentMatrix, M) = adjacency(filtered,N,IndexTerms,filtered) 
R = maximumReadability(documentMatrix,N) 
gold = index2chrom(convertToChromosome(gold_original,original),N)
#queryList = querySimilarity(filtered,IndexTerms,Query)

print("d0"+str(i)+"\tN="+str(N)+"\tS="+str(len(gold_original))+"\tCF="+str(cohesionFactor(gold,N,M,documentMatrix))+"\tRF="+str(readabilityFactor(gold,N,documentMatrix,R)))
end = time.time()
print(end-start)