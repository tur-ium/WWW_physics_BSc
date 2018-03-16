#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 28 21:17:12 2018

@author: RamanSB
"""
'''This class defines methods that are undergo in the Barbasi Albert model.
Initial Configuration - A complete Graph containing N(t=t_0) vertices, say N(t_0) = m+1,
each vertex has a degree of m, by definition of the complete graph.


Properties/Variables to keep track of:
    -Number of nodes in final network, N. 
    -m: number of edges that must be attached from the added vertex at time t.


'''

import networkx as nx
import random
import numpy as np
import math
import pylab
import Analysis 


class BA():
    
    #m - the number of edges between vertices in the complete graph initially,
    #also the number of edges to attach from node added at time t.
    #N - number of nodes required at networks final state.
    
    
    
    def __init__(self, m, N):
        self.m = m #This is the average weight (average number of messages sent)
        self.N = N
        self.no = math.ceil(m)+1 #Initial number of nodes in graph.
        self.G = nx.complete_graph(self.no-1) #Complete graphs creates a complete graph with (m+1) nodes / m edges.
        self.newEdges = []
        self.newNodes = []
        self.vertexDegree = [] #A list of vertices, each vertex appears an amount of times equal to its 'weighted' degree.
        self.newWeight = 0
        self.Analysis = Analysis.Analysis()
        for node in self.G.nodes():
            for i in range(nx.degree(self.G, node)):
                self.vertexDegree.append(node)
            
        #Attaching initial weights of 1 to the existing edges.
        for edges in self.G.edges():
            self.G[edges[0]][edges[1]]['weight'] = 1
        
        #Checking variables are storing the desired values.
        print("Average weight:{}\nRequired nodes, N:{}\nInitial number of nodes:{}\n{}".format(self.m, self.N, self.no,self.vertexDegree))
    
    #Nodes in initial graph are coloured red.
    def nodeColorMap(self):
        nodeColorMap = []
        for node in self.G.nodes():
            if(node<self.no):
                nodeColorMap.append('red')
            else:
                nodeColorMap.append('green')
        return nodeColorMap
    
    def drawNetwork(self):
       
        nodeColorMap = self.nodeColorMap()
        nx.draw(self.G, node_color = nodeColorMap)
        #nx.draw_networkx_edge_labels(self.G,pos) #Comment this out to remove weights
   
        #nx.draw(self.G, node_color = nodeColorMap, with_labels=True)
        
    #Returns initial number of nodes in graph.
    def getNo(self):
        return self.no
    
    #Returns number of nodes desired in final graph.
    def getN(self):
        return self.N

    #Returns list of all current edges in graph.
    def getEdgelist(self):
        return nx.edges(self.G)
    
    def getNodeList(self):
        return nx.nodes(self.G)
    
    #Edge Attachment methods must be called in succession with the method below.
    def addNewNodeToNetwork(self, nodeLabel):
        if(self.G.has_node(nodeLabel)):
            print("Node {} already exists in the network".format(nodeLabel))
        else:
            self.newNodes.append(nodeLabel) #Keeps track of nodes added to the initial graph.
            self.G.add_node(nodeLabel)
        
 
    
    #Adding edges of total weight m to (new) vertex via phase 1. (Preferential Attachment)
    def addEdgesViaPPA(self, i):
        newNode = self.newNodes[-1]
        nodesTotalWeight = 0
        
        selectedNodes = []
        
        #Differs from BA model completely, as incorporates weight. #m is the average number of messages not degree.
        while(nodesTotalWeight < math.floor(self.m)):
            selectedNode = random.choice(self.vertexDegree) #selected based on degree distribution.
            selectedNodes.append(selectedNode) #Keeps track of frequency of edges.
            if(selectedNode==newNode): #Ignore self loops
                pass
            if(self.G.has_edge(newNode, selectedNode)): #If edge exists increment weight.
                self.G[newNode][selectedNode]['weight'] += 1
            else: #Add the edge.
                self.newEdges.append((newNode, selectedNode)) #Tracking additional edges.
                self.G.add_edge(newNode, selectedNode)
                self.G[newNode][selectedNode]['weight'] = 1
            
            #Measure LCS and ACC every time 50 edges or weight are drawn.
            self.newWeight+=1
            if(self.newWeight%50==0):
                self.Analysis.computeLCS(self.G, i, removal=False , addition=True)
                self.Analysis.computeACC(self.G, i, removal=False , addition=True)
            
            self.vertexDegree.append(selectedNode) #Adding selectedNode to weightedDegree distribution.
            nodesTotalWeight +=1
            
        #Drawing the edges.
        for i in range(len(selectedNodes)):
            self.vertexDegree.append(newNode) #Adds new vertex to vertexDegree list, (m times).
        
    def edgeRemoval(self, i,  randomRemoval=True):
        numberOfEdges = self.G.number_of_edges()
        totalWeight = sum([self.G[edge[0]][edge[1]]['weight'] for edge in self.G.edges()])
        if(randomRemoval==True):
            weightsRemoved = 0
            edgesRemoved = 0
            
            while(weightsRemoved < totalWeight):
                edge = random.choice(self.G.edges())#randomEdge 
                if(self.G[edge[0]][edge[1]]['weight'] > 1):
                    self.G[edge[0]][edge[1]]['weight'] -= 1
                else:
                    self.G.remove_edge(edge[0], edge[1])
                    edgesRemoved+=1
                    #print("{}/{} edges removed".format(edgesRemoved, numberOfEdges))
                
                weightsRemoved +=1
                print("{}/{} weights removed".format(weightsRemoved, totalWeight))
                print(self.G.number_of_edges())
                if(weightsRemoved%50==0):
                    self.Analysis.computeLCS(self.G, i, removal=True, addition=False)
                    self.Analysis.computeACC(self.G, i, removal=True, addition=False)
            
            
    
    
        
        
        
        
    