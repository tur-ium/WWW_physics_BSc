#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 14 20:59:22 2018

@author: RamanSB
"""

import Timeslice as ts
import time
import networkx as nx
import numpy as np
from matplotlib import cbook
import User
import pickle
import random

#Nodes are categorized by 2 groups - Neighbours & Others.
#Neighbours consist of normal neighbours and those that form cliques. 
#I suspect that neighbours that form a clique have a higher probability for interactions than any other node category.
#Assumption; There is never a 0 probability of interacting with a node, regardless of how many edges away they may be on the Social Network

socialNetworkFilePath = "/Users/RamanSB/Documents/University/3rd-Year Physics/3rd Year Project/Real Data/GEXF_social_network.gexf"
activityNetworkFilePath = "/Users/RamanSB/Documents/University/3rd-Year Physics/3rd Year Project/Real Data/TimeSlicedData/GEXF/2008/2008_JAN_MultiDiGraph.gexf"
savedDataFilePath = "/Users/RamanSB/Documents/University/3rd-Year Physics/3rd Year Project/PythonSavedData/"

startTime = time.time()
print("Code Started")

friendshipNetwork = ts.loadGEXF(socialNetworkFilePath)
print("Time to load network:{}s".format(time.time()-startTime))

class Model():
    
    
    
    def collectDataFromSocialNetwork(self, socialNetwork):
        startTime = time.time()
        self.allNodes = socialNetwork.nodes()
        relationsDict = {} #Contains Neighbours & Non-Neighbour nodes for each node. Key-Node : Value - [[Neighbors], [Nodes]]
        
        i=0
        for node in friendshipNetwork.nodes():
            loopstartTime = time.time()
          
            nodeId = node
            neighbors = nx.neighbors(friendshipNetwork, node)
           
            nonNeighbors = [] #Array containing nodes that are not neighbours of the node in question.
            self.allNodes.remove(nodeId) #Removing current node - to avoid drawing in selfloops
            for nodes in self.allNodes:
                if(nodes not in neighbors):
                    nonNeighbors.append(nodes) #Creates array of nodes that are not neighbours
                
            self.allNodes.append(nodeId) #Add back in node in consideration.
            #data = [nodeId, neighbors, nonNeighbors]
            #writeDataToFile("categoryNodes.txt", data) Takes way tool ong up to 0.7 seconds per node.
            relationsDict[nodeId] = [neighbors, nonNeighbors]
            i+=1
            print("Loop {}: Time taken to establish neighbors {}: ".format(i, time.time()-loopstartTime))
        return relationsDict
    
    
    def collectDataFromActivityNetwork(self, activityNetworkFilePath):
        print("Collecting data from degree data {}".format(activityNetworkFilePath))
        startTime = time.time()
        activityNetwork = ts.loadGEXF(activityNetworkFilePath)
        degreeDict = activityNetwork.degree()
        nodeList = degreeDict.nodes()
        print("Time taken to load network & establish final degree distribution: {}s".format(time.time()-startTime))
        return degreeDict, nodeList
    
    
    '''  
    def writeDataToFile(fileName, data):
        file = open(savedDataFilePath+fileName, 'a+')
        file.writelines("{} {} {}".format(data[0], data[1], data[2]))
        file.close()    
    '''    
        
    
    
    
    #def initiateNetworkModel():
        
    #p is the probability of drawing an edge between a node and a friend. (1-p) other
    def generateEdgesWithProbability(self, nodeCategoryDict, nodeList, degreeDict, p):
        edgeGenerationStartTime = time.time()
        print("Generating Edges at time {}s".format(edgeGenerationStartTime))
        edges = []
        for node in nodeList:
            nodeNeighbors = nodeCategoryDict[str(node)][0]
            nodeOthers = nodeCategoryDict[str(node)][1]
            nodeDegree = degreeDict[str(node)]
            print("Generating edges for node {} at time: {}s".format(node, time.time()-edgeGenerationStartTime))
            for i in range(nodeDegree):
                nodeCat =  random.choices([nodeNeighbors, nodeOthers], weights=[p, 1-p])
                nodeInteracting = nodeCat[random.randint(0, len(nodeCat)-1)]
                edges.append((node, nodeInteracting))
                
        return edges
        
                
                
            
            
                    
            
        
        
Model = Model() 

categoryNodes = Model.collectDataFromSocialNetwork(friendshipNetwork) 
nodeDegreeDist, nodeList = Model.collectDataFromActivityNetwork(activityNetworkFilePath) 
modelEdgeList = Model.generateEdgesWithProbability(categoryNodes, nodeList, nodeDegreeDist)
        

    
    
    



    
print("Code complete in {}s".format(time.time()-startTime))