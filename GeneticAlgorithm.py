import numpy as np
import random 
import math
from Summary import *

#Neural network weights
f1 = open('Neural_network_training\Theta1.txt','r')
Theta1=np.matrix([list(map(float,line.split(','))) for line in f1])
f1.close()
f2 = open('Neural_network_training\Theta2.txt','r')
Theta2=np.matrix([list(map(float,line.split(','))) for line in f2])
f2.close()
print(Theta1)
print(Theta2)

def sigmoid(x):
  return 1 / (1 + math.exp(-x))

def sigmoidArray(arr):
	(rows,columns)=np.shape(arr)
	for i in range(rows):
		arr[i][0]=sigmoid(arr[i][0])
	return arr

#function to implement forward propagation in neural network
def forward(X):
	hidden=sigmoidArray(Theta1*X)
	biasedHidden=np.matrix(([1]),dtype=float)
	biasedHidden=np.vstack((biasedHidden,hidden))
	output=sigmoidArray(Theta2*biasedHidden)
	return float(output[0][0])

#initialize a random population for genetic algorithm
#size = no. of individuals in population, S = no. of sentences in a summary, N = length of source document
def initPopulation(size,S,N):
	init=[1]*S+[0]*(N-S);
	return [np.random.permutation(init) for x in range(size)]

#fitness function for a given summary, input  in the form of a chromosome 
def fitness(a,b,chromosome):
	#f= a*cohesionFactor(chromosome)+b*readabilityFactor(chromosome)
	X=np.matrix(([1],[cohesionFactor(chromosome)],[readabilityFactor(chromosome)]),dtype=float)
	f=forward(X)
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
		if(chromosome[0]==1 and chromosome[1]==0):
			(chromosome[0],chromosome[1])=(0,1)
		else:
			mutation(chromosome,N)
	elif(ind==N-1):
		if(chromosome[N-1]==1 and chromosome[N-2]==0):
			(chromosome[N-1],chromosome[N-2])=(0,1)
		else:
			mutation(chromosome,N)
	else:
		if(chromosome[ind]==1):
			if(chromosome[ind-1]==0 and chromosome[ind+1]==1):
				(chromosome[ind],chromosome[ind-1])=(0,1)
			elif(chromosome[ind-1]==1 and chromosome[ind+1]==0):
				(chromosome[ind],chromosome[ind+1])=(0,1)
			elif(chromosome[ind-1]==0 and chromosome[ind+1]==0):
				ind2=random.randint(0,1)
				if(ind2==0):
					(chromosome[ind],chromosome[ind+1])=(0,1)
				else:
					(chromosome[ind],chromosome[ind-1])=(0,1)
			else:
				mutation(chromosome,N)
		else:
			mutation(chromosome,N)


#function to find the two individuals with the smallest fitness values
def smallest(fitnesses):
	min1=0
	min2=0
	ind1=0
	ind2=0
	if(fitnesses[0]<fitnesses[1]):
		(min1,min2,ind1,ind2)=(fitnesses[0],fitnesses[1],0,1)
	else:
		(min1,min2,ind1,ind2)=(fitnesses[1],fitnesses[0],1,0)
	for i in range(2,len(fitnesses)):
		if(fitnesses[i]<min1):
			min2=min1
			ind2=ind1
			min1=fitnesses[i]
			ind1=i
		elif(fitnesses[i]<min2):
			min2=fitnesses[i]
			ind2=i
	return [ind1,ind2]

			

#The overall genetic algorithm for a fixed fitness function
def GA(size,S,N,a,b):
	#initialize a random population of required size
	population=initPopulation(size,S,N)
	fitnesses=[fitness(a,b,x) for x in population]
	#best two individuals selected
	best=elitism(fitnesses)

	for i in range(25):
		#Phase1:- Selection of individuals for reproduction
		denom=sum(fitnesses)-fitnesses[best[0]]-fitnesses[best[1]]
		probabilities=[x/denom for x in fitnesses]
		(probabilities[best[0]],probabilities[best[1]])=(0,0)
		select=np.random.choice(range(size),2,replace=False,p=probabilities)


		#crossover between individuals
		offspring=crossover(population[select[0]],population[select[1]],S,N)


		#conditional mutation of the offsprings based on probability
		mutate=random.randint(0,1)
		if(mutate==1):
			mutation(offspring[0],N)
		mutate=random.randint(0,1)
		if(mutate==1):
			mutation(offspring[1],N)
		(f1,f2)=(fitness(a,b,offspring[0]),fitness(a,b,offspring[1]))

		
		#pruning the set by removing the two weakest individuals from the new set
		worst=smallest(fitnesses)
		temp=[f1,f2,fitnesses[worst[0]],fitnesses[worst[1]]]
		tempBest=elitism(temp)
		if(sum(tempBest)==1):
			(population[worst[0]],population[worst[1]],fitnesses[worst[0]],fitnesses[worst[1]])=(offspring[0],offspring[1],f1,f2)
		elif(sum(tempBest)==2):
			(population[worst[1]],fitnesses[worst[1]])=(offspring[0],f1)
		elif(sum(tempBest)==4):
			(population[worst[0]],fitnesses[worst[0]])=(offspring[1],f2)
		elif(sum(tempBest)==3 and (tempBest[0]==0 or tempBest[0]==3)):
			(population[worst[0]],fitnesses[worst[0]])=(offspring[0],f1)
		elif(sum(tempBest)==3 and (tempBest[0]==1 or tempBest[1]==2)):
			(population[worst[1]],fitnesses[worst[1]])=(offspring[1],f2)

		
		#finding new fittest individuals 
		temp=[fitnesses[best[0]],fitnesses[best[1]],fitnesses[worst[0]],fitnesses[worst[1]]]
		tempBest=elitism(temp)

		if(tempBest[0]==0):
			tempBest[0]=best[0]
		elif(tempBest[0]==1):
			tempBest[0]=best[1]
		elif(tempBest[0]==2):
			tempBest[0]=worst[0]
		elif(tempBest[0]==3):
			tempBest[0]=worst[1]
		if(tempBest[1]==0):
			tempBest[1]=best[0]
		elif(tempBest[1]==1):
			tempBest[1]=best[1]
		elif(tempBest[1]==2):
			tempBest[1]=worst[0]
		elif(tempBest[1]==3):
			tempBest[1]=worst[1]
		
		(best[0],best[1])=(tempBest[0],tempBest[1])
	
	return (population[best[0]],fitnesses[best[0]])


#runs 50iterations of GA function for different values of fitness function weights
def main(size,S,N):
	fittest=-1
	summary=[0]
	for i in range(50):
		a=random.random()
		(temp1,temp2)=GA(size,S,N,a,(1-a))
		if(temp2>fittest):
			fittest=temp2
			summary=temp1
		print(fittest)
	print("Precision of the fittest summary:")
	print(precision(summary,gold_original))
	print(fittest)
	print(cohesionFactor(summary),readabilityFactor(summary))
	print([i for i in range(N) if(summary[i]==1)])
	return convertToText(summary)

def main2(size,S,N,a,b):
	(temp1,temp2)=GA(size,S,N,a,b)
	print("Precision")
	print(precision(temp1,gold_original))
	print("Fitness")
	print(temp2)
	return precision(temp1,gold_original)
	



"""x2=0
prec=0
for i in range(21):
	a=i/20
	b=1-a
	print("*************Iteration**********")
	print(i)
	temp=main2(20,19,N,a,b)
	if(temp>prec):
		x2=a
		prec=temp
	temp=main2(20,19,N,a,b)
	if(temp>prec):
		x2=a
		prec=temp
print(prec)
print(x2)"""
print(main(20,19,N))

