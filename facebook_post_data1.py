#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  7 16:41:59 2017

@authors: RamanSB, ArturD

#TODO:
13/12/17
* Check entropy results
* Check critical occ prob results
* Address memory issues with loading data
"""

import os
import numpy as np
import time
import matplotlib.pyplot as plt

#%%
dataPath = "facebook-wosn-wall/out.facebook-wosn-wall"

def readData(path,verbose=False):
    #Skip the first 2 lines which contains comments.
    lineCounter = 0
    data = open(dataPath).read().splitlines()[2:]
    finalData = []
    print('Using only first 500,000 edges')
    for line in data:
        #TODO: Only reading the first 500,000 lines due to memory limits
        
        if lineCounter >= 500000:
            break
        line = line.split(" ")
        line[2] = line[2].replace("\t", "")
        line_data = [int(val) for val in line]
        finalData.append(line_data)
        lineCounter+=1
    if verbose:
        print('# of edges: {}'.format(lineCounter))
    return finalData
    

def getNodeSet(data):
    '''Get a set of nodes in the dataset
    Returns
    ---
    vertices, numberOfVertices: set, int
        set of vertices and number of vertices'''
    vertices = set()
    for info in data:
        vertices.add(info[0])
        vertices.add(info[1])
    
    numberOfVertices = len(vertices)
    
    return vertices, numberOfVertices

def getEdgeList(data):
    edgeList = []

    for info in data:
        edgeList.append([int(info[0]), int(info[1])])
       
        
    return edgeList
    
def getAdjacencyMatrix(vertices, edgeList):
    N = len(vertices)
    A = np.zeros((N,N))
    #if there exists an edge from vertex j to i, we populate the adjancey matrix column i-j.
    for i, j in edgeList:
            A[j-1,i-1]+=1

    return A
#%%
start = time.time()
data = readData(dataPath)    
vertices, networkSize = getNodeSet(data)
end = time.time()
print('Time taken to get list of vertices: {:.3g} s'.format(end-start))
edgeList = getEdgeList(data)
AdjMatrix = getAdjacencyMatrix(vertices, edgeList)
print(AdjMatrix)

#Yields correct shape of matrix
print(np.shape(AdjMatrix))

#%%
def getOutDegreeDistr(adjMatrix):
    N = AdjMatrix.shape[0]
    outDegree = np.zeros(N)
    outDegreeDist = dict()
    for i in range(N):
        degree = np.sum(AdjMatrix[i,:])
        outDegree[i] = degree
        if not degree in outDegreeDist.keys():
            outDegreeDist[degree] = 0
        outDegreeDist[degree]+=1
    plt.figure()
    plt.hist(outDegree,log=True)   #Expect a power law distribution from Zipf's Law
    plt.title('Out degree distribution')
    plt.xlabel('Out degree')
    plt.ylabel('Frequency')
    return outDegreeDist

def getInDegreeDistr(adjMatrix):
    N = AdjMatrix.shape[0]
    inDegree = np.zeros(N)
    inDegreeDist = dict()
    for i in range(N):
        degree = np.sum(AdjMatrix[:,i])
        inDegree[i] = degree
        if not degree in inDegreeDist.keys():
            inDegreeDist[degree] = 0
        inDegreeDist[degree]+=1
    plt.figure()
    plt.hist(inDegree,log=True)   #Expect a power law distribution from Zipf's Law
    plt.title('In degree distribution')
    plt.xlabel('In degree')
    plt.ylabel('Frequency')
    return inDegreeDist

def shannon_entropy(distr):
    '''Calculates the Shannon entropy for a frequency distribution distr, given\
    as a dictionary'''
    Nout = sum(distr.values())   #Total of the number of out edges
    #TODO: Should it be the total number of edges?
    print('Number of out edges: {} s'.format(Nout))
    entropy = 0   #Information entropy
    for degree, freq in distr.items():
        p = freq/Nout
        entropy -= p* np.log2(p)
    return entropy

def crit_prob(degree_distr):
    '''Returns critical occupation probability for uniform removal, given a degree\
    distribution `degree_distr` given as a dictionary'''
    N = sum(degree_distr.values())  #Number of edges
    k_exp = 0   #Expectation value of degree
    k_sq_exp = 0   #Expectation value of the degree
    for degree, freq in degree_distr.items():
        p = freq/N
        k_exp += p*degree
        k_sq_exp += p*degree**2
    return k_exp/(k_sq_exp-k_exp)
        
outDegreeDistr = getOutDegreeDistr(AdjMatrix)
inDegreeDistr = getInDegreeDistr(AdjMatrix)
entropy_out = shannon_entropy(outDegreeDistr)
entropy_in = shannon_entropy(inDegreeDistr)
critical_occ_prob_out = crit_prob(outDegreeDistr)
critical_occ_prob_in = crit_prob(inDegreeDistr)
print('Entropy of distribution: {:.3g} bits (in edges)'.format(entropy_in))
print('Entropy of distribution: {:.3g} bits (out edges)'.format(entropy_out))
print('Critical occ prob (in degree): {:.3%}'.format(critical_occ_prob_in))
print('Critical occ prob (out degree): {:.3%}'.format(critical_occ_prob_out))
#Critical occ prob = 0.8% i.e. for the percolating cluster to fail 99.2% of users \
# would have to be removed

#Similar crit occ prob using in and out degrees
#%%