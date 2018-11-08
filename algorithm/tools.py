# -*- coding: utf-8 -*-
"""
function tools
"""


#initiate stock list signal
def stocksignal(population,populationSize):
    for i in range(populationSize):
        stocklist=[]
        for j in range(12):
            if population[i][0][j]>0:
                stocklist.append(1)
            else:
                stocklist.append(0)
        if len(population[i])==1:
            population[i].append(stocklist)
        else:
            population[i][1]=stocklist
    return population

def yagersEntropy(porprotion,n):
    H=0
    for i in range(n):
        H+=abs(porprotion[i]-1/n)
        
    return H