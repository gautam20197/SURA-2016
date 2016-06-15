import numpy as np
import random 
import math
from Summary import *

def index2chrom(indices):
	chrom=[0]*N
	for i in indices:
		chrom[i]=1
	return chrom

#print("d061\tN="+str(N)+"\tS="+str(len(gold_filtered))+"\tCF="+str(cohesionFactor(index2chrom(convertToChromosome(gold_original))))+"\tRF="+str(readabilityFactor(index2chrom(convertToChromosome(gold_original)))))

for i in range(62,71):
	(filtered,original) = extraction('Documents\d0'+str(i)+'.txt') 
	(IndexTerms,Query) = indexTerms(filtered) 
	(gold_filtered,gold_original) = extraction('Summaries\d0'+str(i)+'_400.txt')
	print([original[i] for i in range(len(filtered)) if(len(filtered[i])==3)])


	N = len(filtered) 
	(documentMatrix, M) = adjacency(filtered) 
	R = maximumReadability(documentMatrix) 
	#queryList = querySimilarity(filtered,IndexTerms,Query)
	print("d0"+str(i)+"\tN="+str(N)+"\tS="+str(len(gold_filtered))+"\tCF="+str(cohesionFactor(index2chrom(convertToChromosome(gold_original))))+"\tRF="+str(readabilityFactor(index2chrom(convertToChromosome(gold_original)))))
