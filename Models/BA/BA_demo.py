#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  9 15:06:56 2018

@author: RamanSB
"""

import numpy as np
import BA
from matplotlib import pyplot as plt
import time
import networkx as nx
import measure_new 
import Timeslice as ts
import Analysis


activityNetworkFilePath = "Data/TimeSlicedData/GEXF/2008/2008_DEC_MultiDiGraph.gexf"
def extractDataFromActivity(filePath):
    activityNetwork = nx.gexf.read_gexf(filePath)
    numberOfNodes = activityNetwork.number_of_nodes() 
    '''
    #weightDict = nx.get_edge_attributes(activityNetwork, 'weight')
    #weightValues = weightDict.values()
    #print(len(weightValues))
    #totalWeight = sum(weightValues)
    #meanWeight = totalWeight/numberOfNodes
    '''
    meanWeight = activityNetwork.number_of_edges()/numberOfNodes

    print("Mean Weight:{}\nFinal Number of Nodes:{}".format(meanWeight, numberOfNodes))
    return meanWeight, numberOfNodes
    
    
m, N = extractDataFromActivity(activityNetworkFilePath)  #Average number of nodes in network, #Average weight of network,
numberOfIterations = 3

startTime = time.time()
print("Code started")
graphs = [BA.BA(m, N)]

for i in range(numberOfIterations):
    graphs = [BA.BA(m, N)]
    for graph in graphs:
        no = graph.getNo() #Initial number of nodes in graph.
        N = graph.getN() #Final number of nodes required
        maxTime = N - no #Time required / amount of vertices to add to obtain N vertices
        timeArray = list(range(1, maxTime+1)) #Intervals of 1.
    
        for t in timeArray:
    
            startAttachmentTime = time.time()
            newNodeLabel = no + t - 1
            graph.addNewNodeToNetwork(newNodeLabel)
            graph.addEdgesViaPPA(i)
            
            print("{}/{} nodes added in {}s".format(t, len(timeArray), time.time()-startAttachmentTime))
  
        #Plotting the degree distribution.
        degreeDict = measure_new.getDegreeDist(graphs[-1].G)
        #Removing edges
        
        graph.edgeRemoval(i, randomRemoval=True)
        
        
        print("Code completed in {}s".format(time.time()-startTime))
    
    

measure_new.plot_distribution(degreeDict, "Degree distribution - Modified (BA)")
    


#LCS_ADD, LCS_REMOVE, ACC_ADD, ACC_REMOVE = graphs[-1].Analysis.collateData(noOfFiles=10)
#AVG_LCS_ADD, STD_LCS_ADD, AVG_LCS_REMOVE, STD_LCS_REMOVE, AVG_ACC_ADD, STD_ACC_ADD, AVG_ACC_REMOVE, STD_ACC_REMOVE = graphs[-1].processData(LCS_ADD, LCS_REMOVE, ACC_ADD, ACC_REMOVE)





