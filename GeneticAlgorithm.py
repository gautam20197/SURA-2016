import numpy as np
import random  
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
#max1 = maximum fitness,	max2 = 2nd best fitness,    ind1 = index of summary with best fitness,   ind2 = index of summary with 2nd best fitness
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


#one-point crossover between two parent chromosomes
def crossover(parent1,parent2,S,N):
	pivot=random.randint(0,N-2)
	child1=[parent1[x] for x in range(0,pivot+1)]+[parent2[x] for x in range(pivot+1,N)]
	child2=[parent2[x] for x in range(0,pivot+1)]+[parent1[x] for x in range(pivot+1,N)]
	reswap(child1,child2,S,N)
	return [child1,child2]


#reswapping of bits (of offsprings) to make the number of ones equal in both children
def reswap(child1,child2,S,N):
	ones=sum(child1)
	if(ones>S):
		ind1=random.sample([x for x in range(N) if child1[x] == 1],ones-S)
		for i in ind1:
			child1[i]=0
		ind2=random.sample([x for x in range(N) if child2[x] == 0],ones-S)
		for i in ind2:
			child2[i]=1
	elif(ones<S):
		ind1=random.sample([x for x in range(N) if child1[x] == 0],S-ones)
		for i in ind1:
			child1[i]=1
		ind2=random.sample([x for x in range(N) if child2[x] == 1],S-ones)
		for i in ind2:
			child2[i]=0


#function to mutate the chromosome of an individual
def mutation(chromosome,N):
	ind=random.randint(0,N-1)
	if(ind==0):
		if(chromosome[0]==1&&chromosome[1]==0):
			(chromosome[0],chromosome[1])=(0,1)
		else:
			mutation(chromosome,N)
	elif(ind==N-1):
		if(chromosome[N-1]==1&&chromosome[N-2]==0):
			(chromosome[N-1],chromosome[N-2])=(0,1)
		else:
			mutation(chromosome,N)
	else:
		if(chromosome[ind]==1):
			if(chromosome[ind-1]==0&&chromosome[ind+1]==1):
				(chromosome[ind],chromosome[ind-1])=(0,1)
			elif(chromosome[ind-1]==1&&chromosome[ind+1]==0):
				(chromosome[ind],chromosome[ind+1])=(0,1)
			else:
				ind2=random.randint(0,1)
				if(ind2==0):
					(chromosome[ind],chromosome[ind+1])=(0,1)
				else:
					(chromosome[ind],chromosome[ind-1])=(0,1)
		else:
			mutation(chromosome,N)


			

def GA(size,S,N):
	population=initPopulation(size,S,N)
	fitnesses=[fitness(x) for x in population]
	best=elitism(fitnesses)


	(fitnesses[best[0]],fitnesses[best[1]])=(0,0)
	denom=sum(fitnesses)
	fitnesses=[x/denom for x in fitnesses]
	select=np.random.choice(range(size),2,replace=False,p=fitnesses)


	offspring=crossover(population[select[0]],population[select[1]],S,N)


	mutate=random.randint(0,1)
	if(mutate==1):
		mutation(offspring[0],N)
	mutate=random.randint(0,1)
	if(mutate==1)
		mutation(offspring[1],N)




GA(20,(int)(N/2),N)