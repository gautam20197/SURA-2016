import numpy as np
import random  
from Summary import *
import re

TAG_RE = re.compile(r'<[^>]+>')

#function to remove xml tags from summary file
def remove_tags(text):
    return TAG_RE.sub('', text)

def training(indices):
	
	chrom=[0]*N
	for i in indices:
		chrom[i]=1
	others=[x for x in range(N) if(chrom[x]==0)]
	dataFile.write(str(cohesionFactor(chrom))+","+str(readabilityFactor(chrom))+",1")
	dataFile.write("\n")
	for i in range(1,(len(indices))+1):
		for t in range(2):
			indexZero=random.sample(indices,i)
			indexOne=random.sample(others,i)
			for j in indexZero:
				chrom[j]=0
			for j in indexOne:
				chrom[j]=1
			dataFile.write(str(cohesionFactor(chrom))+","+str(readabilityFactor(chrom))+","+str((len(indices)-i)/len(indices))+","+str(precision(chrom,gold_original)))
			dataFile.write("\n")
			chrom=[0]*N
			for j in indices:
				chrom[j]=1


dataFile=open("data.txt",'w')
dataFile.truncate()
"""for i in range(62,80):
	training(convertToChromosome(gold_original))
	(filtered,original) = extraction('d0'+str(i)+'.txt') 
	(IndexTerms,Query) = indexTerms(filtered) 
	(gold_filtered,gold_original) = extraction('new.txt') 
	N = len(filtered)  
	(documentMatrix, M) = adjacency(filtered) 
	R = maximumReadability(documentMatrix)
	queryList = querySimilarity(filtered,IndexTerms,Query)"""
training(convertToChromosome(gold_original))	
dataFile.close()
