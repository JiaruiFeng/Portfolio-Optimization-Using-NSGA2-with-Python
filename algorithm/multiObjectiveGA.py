# -*- coding: utf-8 -*-
"""
one objective GA
"""
import pandas as pd
import tools
import random
from crossover import crossover
from mutation import mutation
from repair import repair
from NSGA2Selection import NSGA2Selection

returns=pd.read_excel('../processedData/returns.xlsx')
turnovers=pd.read_excel('../processedData/turnovers.xlsx')
minmax=pd.read_excel('../processedData/minmaxValue.xlsx')

populationSize=50
generation=50
Pm=0.5
Pc=0.9
l=0.05
u=0.3

    
#initiate population    
population=[[] for i in range(populationSize)]
selectedPopulation=[[] for i in range(populationSize)]
for i in range(populationSize):
    entity=[0 for i in range(12)]
    n=1
    label=[i for i in range(12)]
    for j in range(12):
        if n>u:
            t=random.choice(label)
            entity[t]=random.uniform(l,u)
            n-=entity[t]
            label.remove(t)
        elif n<l:            
            entity[t]+=n
            n=0
        else:
            t=random.choice(label)
            entity[t]=random.uniform(l,n)
            n-=entity[t]         
            label.remove(t)              
    population[i].append(entity)
    selectedPopulation[i].append(entity)
newPopulation=tools.stocksignal(population,populationSize)


#GA loop
for i in range(generation):
    offspring=crossover(newPopulation,populationSize,Pc,l,u)
    offspring=mutation(offspring,populationSize,Pm)
    offspring=repair(offspring,populationSize,l,u)
    selectPopulation=selectedPopulation+offspring
    selectedPopulation,firstFront,NDFSet=NSGA2Selection(selectPopulation,populationSize,minmax,returns,turnovers)
    newPopulation=tools.stocksignal(selectedPopulation,populationSize)
    print (i)


name=['000002','600690','002001','600009','000001','002008','002236','002384','002304','600885','000046','000858']
result=pd.DataFrame([[0 for j in range(len(name))] for i in range(len(firstFront))])
for i in range(len(firstFront)):
    for j in range(len(name)):
        result.iloc[i,j]=newPopulation[firstFront[i]][0][j]

result.columns=name
result.to_excel('../resultData/result2.xlsx',encoding='utf-8')


