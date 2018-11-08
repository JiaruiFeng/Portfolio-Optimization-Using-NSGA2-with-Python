# -*- coding: utf-8 -*-
"""
NSGA2 selection
"""
import pandas as pd
import numpy as np

#compute the expectation of the returns of the portfolio
def expectation(returns,weights):
    eArray=np.array(returns.mean())
    return np.dot(eArray,weights.T)

#compute the variance of the returns of the portfolio
def variance(returns,weights):    
    return np.dot(weights.T, np.dot(returns.cov()*len(returns.index),weights))
    
#compute the skewness of the returns of the portfolio
def turnover(turnovers,weights):
    tArray=np.array(turnovers.mean())
    return np.dot(tArray,weights.T)

#generate value set for every objective
def objectiveValueSet(population,populationSize,fun,data):
    valueList=[0 for i in range(populationSize)]
    for i in range(populationSize):
        valueList[i]=fun(data,np.array(population[i][0]))
    return valueList

#Fast Nondominated Sorting Approach
def NSGA(population,populationSize,returns,turnovers):
    #build list and compute return,variance,turnover rate for every entity in the population
    returnList=objectiveValueSet(population,populationSize,expectation,returns)
    varianceList=objectiveValueSet(population,populationSize,variance,returns)
    turnoverList=objectiveValueSet(population,populationSize,turnover,turnovers)
    
    #define the dominate set Sp
    dominateList=[set() for i in range(populationSize)]
    #define the dominated set
    dominatedList=[set() for i in range(populationSize)]
    #compute the dominate and dominated entity for every entity in the population
    for i in range(populationSize):
        for j in range(populationSize):
            if returnList[i]> returnList[j] and varianceList[i]<varianceList[j] and turnoverList[i]>turnoverList[j]:
                dominateList[i].add(j)
                
            elif returnList[i]< returnList[j] and varianceList[i]>varianceList[j] and turnoverList[i]<turnoverList[j]:
                dominatedList[i].add(j)
    #compute dominated degree Np
    for i in range(len(dominatedList)):
        dominatedList[i]=len(dominatedList[i])
    #create list to save the non-dominated front information
    NDFSet=[]
    #compute non-dominated front
    while max(dominatedList)>=0:
        front=[]
        for i in range(len(dominatedList)):
            if dominatedList[i]==0:
                front.append(i)
        NDFSet.append(front)
        for i in range(len(dominatedList)):
            dominatedList[i]=dominatedList[i]-1                                
    return NDFSet

#crowded distance
def crowdedDistance(population,Front,minmax,returns,turnovers):
    #create distance list to save the information of crowded for every entity in front
    distance=pd.Series([float(0) for i in range(len(Front))], index=Front)
    #save information of weight for every entity in front
    FrontSet=[]
    for i in Front:
        FrontSet.append(population[i])

    #compute and save objective value for every entity in front
    returnsList=objectiveValueSet(FrontSet,len(FrontSet),expectation,returns)
    varianceList=objectiveValueSet(FrontSet,len(FrontSet),variance,returns)
    turnoverList=objectiveValueSet(FrontSet,len(FrontSet),turnover,turnovers)   
    returnsSer=pd.Series(returnsList,index=Front)
    varianceSer=pd.Series(varianceList,index=Front)
    turnoverSer=pd.Series(turnoverList,index=Front)
    #sort value
    returnsSer.sort_values(ascending=False,inplace=True)
    varianceSer.sort_values(ascending=False,inplace=True)
    turnoverSer.sort_values(ascending=False,inplace=True)
    #set the distance for the entities which have the min and max value in every objective 
    distance[returnsSer.index[0]]=1000
    distance[returnsSer.index[-1]]=1000
    distance[varianceSer.index[0]]=1000
    distance[varianceSer.index[-1]]=1000
    distance[turnoverSer.index[0]]=1000
    distance[turnoverSer.index[-1]]=1000
    for i in range(1,len(Front)-1):
        distance[returnsSer.index[i]]=distance[returnsSer.index[i]]+(returnsSer[returnsSer.index[i-1]]-returnsSer[returnsSer.index[i+1]])/(minmax.iloc[0,1]-minmax.iloc[0,0])
        distance[varianceSer.index[i]]+=(varianceSer[varianceSer.index[i-1]]-varianceSer[varianceSer.index[i+1]])/(minmax.iloc[1,1]-minmax.iloc[1,0])
        distance[turnoverSer.index[i]]+=(turnoverSer[turnoverSer.index[i-1]]-turnoverSer[turnoverSer.index[i+1]])/(minmax.iloc[2,1]-minmax.iloc[2,0])
    distance.sort_values(ascending=False,inplace=True)
    return distance
#crowded compare operator
def crowdedCompareOperator(population,populationSize,NDFSet,minmax,returns,turnovers):
    newPopulation=[]
    #save the information of the entity the new population have
    count=0
    #save the information of the succession of the front 
    number=0
    while count<populationSize:            
        if count + len(NDFSet[number])<=populationSize:
            if number==0:
                #save the information of the first non-dominated front
                firstFront=[i for i in range(len(NDFSet[number]))]
            for i in NDFSet[number]:
                newPopulation.append(population[i])
            count+=len(NDFSet[number])
            number+=1
        else:
            if number==0:
                firstFront=[i for i in range(populationSize)]
            n=populationSize-count
            distance=crowdedDistance(population,NDFSet[number],minmax,returns,turnovers)
            for i in range(n):
                newPopulation.append(population[distance.index[i]])
            number+=1
            count+=n

    return newPopulation,firstFront


def NSGA2Selection(population,populationSize,minmax,returns,turnovers):
    NDFSet=NSGA(population,populationSize*2,returns,turnovers)
    newPopulation,firstFront=crowdedCompareOperator(population,populationSize,NDFSet,minmax,returns,turnovers)
    return newPopulation,firstFront,NDFSet




