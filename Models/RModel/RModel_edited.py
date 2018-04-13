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
from matplotlib import pyplot as plt
import pickle
import random
import copy
import measure_new

#Nodes are categorized by 2 groups - Neighbours & Others.
#Neighbours consist of normal neighbours and those that form cliques. 
#I suspect that neighbours that form a clique have a higher probability for interactions than any other node category.
#Assumption; There is never a 0 probability of interacting with a node, regardless of how many edges away they may be on the Social Network

socialNetworkFilePath = "Data/GEXF_social_network.gexf"
activityNetworkFilePath = "Data/TimeSlicedData/GEXF/2008/2008_DEC_MultiDiGraph.gexf"
savedDataFilePath = "IncomingResults/"
generatedDataFilePath = "GeneratedResults/"

startTime = time.time()
print("Code Started")

friendshipNetwork = ts.loadGEXF(socialNetworkFilePath)
print("Time to load network:{}s".format(time.time()-startTime))

class Model():
    
    
    def __init__(self, p):
        self.p = p
    
    
    def collectDataFromSocialNetwork(self, socialNetwork):
        startTime = time.time()
        self.allNodes = socialNetwork.nodes()
        relationsDict = {}
        print(len(self.allNodes))
        i=0
        for node in friendshipNetwork.nodes():
            loopstartTime = time.time()
          
            nodeId = node
            neighbors = nx.neighbors(friendshipNetwork, node)
            relationsDict[nodeId] = [neighbors] 
            i+=1
            print("Loop {}: Time taken to establish neighbors {}: ".format(i, time.time()-loopstartTime))
        return relationsDict
    
    
    def collectDataFromActivityNetwork(self, activityNetworkFilePath):
        print("Collecting data from degree data {}".format(activityNetworkFilePath))
        startTime = time.time()
        activityNetwork = ts.loadGEXF(activityNetworkFilePath)
        NO_OF_EDGES = activityNetwork.number_of_edges()
        degreeDict = activityNetwork.degree()
        nodesSlice = list(degreeDict.keys())
        print("Time taken to load network & establish final degree distribution: {}s".format(time.time()-startTime))
        return degreeDict, nodesSlice, NO_OF_EDGES
    
    
        
        
    #p is the probability of drawing an edge between a node and a friend. (1-p) other
    def generateEdgesWithProbability(self, nodeCategoryDict, M, iteration):
     
        modelG = nx.Graph()
        edgesAdded = []
        LCS = []
        m=0
        while(m<M):
            startLoopTime = time.time()
           
            sourceNode = self.allNodes[random.randint(0, len(self.allNodes)-1)]
            modelG.add_node(sourceNode)
            sourceNodeNeighbors = nodeCategoryDict[sourceNode][0]
            
            #Finding Non-Neighbors
            nodeListCopy = copy.copy(self.allNodes)
            nodeListCopy.remove(sourceNode)
            for neighbors in sourceNodeNeighbors:
                nodeListCopy.remove(neighbors)
            
            sourceNodeOthers = nodeListCopy
            targetNodeCategory = random.choices([sourceNodeNeighbors, sourceNodeOthers], weights=[self.p, 1-self.p])
            targetNode = targetNodeCategory[0][random.randint(0,len(targetNodeCategory[0])-1)]
            #print("Source Node: {}\nTarget Node: {}".format(sourceNode, targetNode))
            if(targetNode not in modelG[sourceNode].keys()):
                modelG.add_edge(sourceNode, targetNode)
                modelG[sourceNode][targetNode]['weight'] = 1
            else:
                modelG[sourceNode][targetNode]['weight'] += 1
            m+=1
            edgesAdded.append(m)
           
            if(m%50==0): 
                LCS_measured = measure_new.computeLCS(modelG)
                LCS.append(LCS_measured)
                #ACC = nx.average_clustering(modelG)
                self.writeDataToFile(str(iteration)+"LCS(no_of_edges_add) P"+str(Model.p), LCS_measured) 
                #self.writeDataToFile(str(iteration)+"ACC(no_of_edges_add) P"+str(Model.p), ACC)
                print("{}/{} Edge generated in {}s".format(m, M, time.time()-startLoopTime))
        
        edges = modelG.edges()
        
        return modelG, edges
        
    
    #Develop edge Removal method. #How to ensure neighbors exist  with redges.
    def removingEdges(self, modelG, nodeCategoryDict, iteration):
        nodeList = modelG.nodes()
        M = modelG.number_of_edges()
        m=0
        W = modelG.size(weight='weight') #TotalWeight Of Graph
        
        while(W>m):
            startTime = time.time()
            chosenNode = nodeList[random.randint(0,len(nodeList)-1)]
            chosenNodesEdgeList = modelG.edges(chosenNode)
            nodesInEdges = [node[1] for node in chosenNodesEdgeList]
            
            nodeNeighbors = nodeCategoryDict[chosenNode][0]
           #print("chosen node: {}".format(chosenNode))
            neighborNodes = []
            nonNeighborNodes = []
            
            #Categorizes edges in to edges with neighbors or non-neighbors.
            for nodes in nodesInEdges:
                if(nodes in nodeNeighbors):
                    neighborNodes.append(nodes)
                else:
                    nonNeighborNodes.append(nodes)
            
            nodeRemoval = int()
            
            #Removing neighborEdges with probability (1-p) and nonNeighborEdges with p
            #NeighborEdges are more likely to remain, as they were most probable to add.
            if(len(nonNeighborNodes) != 0 and len(neighborNodes) !=0):
                edgeRemovalCategory = random.choices([neighborNodes, nonNeighborNodes], weights=[1-self.p, self.p])[0]
                #print("Length of category: {}".format(len(edgeRemovalCategory)))
            #Removing the edge containing (ChosenNode & nodeRemoval)          
                nodeRemoval = edgeRemovalCategory[random.randint(0, len(edgeRemovalCategory)-1)]
            #If no nonNeighborNodes exist remove neighborNode Edges (randomly).
            elif(len(nonNeighborNodes)==0 and len(neighborNodes)!=0):
                nodeRemoval = random.choice(neighborNodes)
            #If no NeighborNodes exist remove nonNeighborNode Edges (randomly).
            elif(len(nonNeighborNodes)!=0 and len(neighborNodes)==0):
                nodeRemoval = random.choice(nonNeighborNodes)
            #Else if chosenNode has no neighbors or non-neighbors edges, remove node from network.
            else:
                modelG.remove_node(chosenNode)
                nodeList = modelG.nodes()
                continue

            
           
            #print("Edges containing node: {}".format(chosenNodesEdgeList))
            #print("Node Removal: {}".format(nodeRemoval))
            #print("NonNeighbor Nodes: {}\nNeighbor Nodes:{}".format(nonNeighborNodes, neighborNodes))
            #print("removing node: {}".format(nodeRemoval))
            
            #If nodeWeight is greater than 1 then decrement weight, if weight is 1, remove edge.
            if(modelG[chosenNode][nodeRemoval]['weight'] > 1):
                modelG[chosenNode][nodeRemoval]['weight'] -= 1
            elif(modelG[chosenNode][nodeRemoval]['weight'] == 1):
                modelG.remove_edge(chosenNode, nodeRemoval)
            

            m+=1 #Incrementing number of edges removed.
            if(m%50==0):
                #ACC = measure_new.computeClusteringCoefficient(modelG, isWeighted=True)[0]
                #self.writeDataToFile(str(iteration)+"ACC(no_of_edges_remove) P"+str(Model.p), ACC)
                LCS = measure_new.computeLCS(modelG)
                self.writeDataToFile(str(iteration)+"LCS(no_of_edges_remove) P"+str(Model.p), LCS)
                print("{}/{} Edges removed in {}s".format(no_of_edges_removed ,M, time.time()-startTime))
                
            no_of_edges_removed = M-modelG.number_of_edges()
            #
            #print("{}/{} Weights removed in {}s".format(m, W, time.time()-startTime))
            
        if(modelG.number_of_edges() == 0):
            print("All edges have been successfully removed.")
        
        
        return modelG
            
           
    def writeDataToFile(self, fileName, data):
        try:
            file = open(generatedDataFilePath+fileName, mode='a+')
            file.writelines("{}\n".format(data))
        except:
            file = open(generatedDataFilePath+fileName, mode='w')
            file.writelines("{}\n ".format(data))
        file.close()    
                      
    
    def initiateModel(self, activityNetworkFilePath, numberOfGraphsInEnsemble):
        categoryNodes = self.collectDataFromSocialNetwork(friendshipNetwork)
        nodesInTimeSlice, noOfEdgesInTimeSlice = self.collectDataFromActivityNetwork(activityNetworkFilePath)[1:]
        self.modelGraph = nx.Graph()
        for i in range(numberOfGraphsInEnsemble):
            self.modelGraph, modelEdgeList = self.generateEdgesWithProbability(categoryNodes, noOfEdgesInTimeSlice, i)
            gexfSavePath = generatedDataFilePath+"RModel_graph_V"+str(noOfEdgesInTimeSlice)+"_P"+str(Model.p)+"-"+str(i)+".gexf"
            nx.write_gexf(self.modelGraph,gexfSavePath)
            self.finalGraph = Model.removingEdges(self.modelGraph, categoryNodes, i)
            
no_of_graphs_in_ensemble = 10
p=0.25
Model = Model(p) 
Model.initiateModel(activityNetworkFilePath, no_of_graphs_in_ensemble)
nx.write_gexf(Model,generatedDataFilePath+'R_modelp={}.gexf'.format(p))

#When running our model, data for average clustering coefficients - clustering coefficient dictionaries
#As well as larget component size for a given time slice model must be recorded. These will be written
#To seperate files, such that data can be read from those files and plotted.



    
print("Code complete in {}s".format(time.time()-startTime))