import numpy as np
from Summary import *

#initialize a random population for genetic algorithm
#size = no. of individuals in population, S = no. of sentences in a summary, N = length of source document
def initPopulation(size,S,N):
	init=[1]*S+[0]*(N-S);
	return [np.random.permutation(init) for x in range(size)]

#fitness function for a given summary, input  in the form of a chromosome 
def fitness(chromosome):
	f= 0.4*cohesionFactor(chromosome)+0.6*readabilityFactor(chromosome)
	return f

#evaluates the two individuals having the best values of fitness among the given population
def elitism(fitnesses):
	max1=0
	max2=0
	ind1=0
	ind2=0
	if(fitnesses[0]>fitnesses[1]):
		(max1,max2,ind1,ind2)=(fitnesses[0],fitnesses[1],0,1)
	else:
		(max1,max2,ind1,ind2)=(fitnesses[1],fitnesses[0],1,0)
	for i in range(2,len(fitnesses)):
		if(fitnesses[i]>max1):
			max2=max1
			ind2=ind1
			max1=fitnesses[i]
			ind1=i
		elif(fitnesses[i]>max2):
			max2=fitnesses[i]
			ind2=i
	return [ind1,ind2]


def GA(size,S,N):
	population=initPopulation(size,S,N)
	fitnesses=[fitness(x) for x in population]
	for i in range(25):
		best=elitism(fitnesses)

GA(20,(int)(N/2),N)