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
    -Number of nodes in network, N. 
    -m: number of edges that must be attached from the added vertex at time t.

'''


'''Note: 
    your network package/graph library has a function that chooses an edge at random. Then choose an end at random.
    
• keep a list of existing edges and choose one at random (or again a library might 
do this for you), then choose one end of that edge at random.

• every time you add an edge to a vertex, add that vertex (or its index) to a list. 
Choosing an entry at random from this list gives you a vertex in proportion 
to its degree (why?).

'''

import networkx as nx
import random
import numpy as np



class BA():
    
    #m - the number of edges between vertices in the complete graph initially,
    #also the number of edges to attach from node added at time t.
    #N - number of nodes required at networks final state.
    
    
    
    def __init__(self, m, N):
        self.m = m
        self.N = N
        self.no = m+1 #Initial number of nodes in graph.
        self.G = nx.complete_graph(m+1) #Complete graphs creates a complete graph with (m+1) nodes / m edges.
        self.newEdges = []
        self.newNodes = []
        self.vertexDegree = [] #A list of vertices, each vertex appears an amount of times equal to its degree.
        for node in self.G.nodes():
            for i in range(nx.degree(self.G, node)):
                self.vertexDegree.append(node)
        
        #Checking variables are storing the desired values.
        print("{}\n{}\n{}\n{}".format(self.m, self.N, self.no,self.vertexDegree))
    
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
        nx.draw(self.G, node_color = nodeColorMap, with_labels=True)
        
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
        
    #Adds a vertex to a list, when an edge is attachde to that vertex.
    def addVertexToDegreeList(self, vertex):
        self.vertexDegree.append(vertex)
    
    
    #Adding (m) edges to (new) vertex via phase 1. (Preferential Attachment)
    def addEdgesViaPPA(self):
        newNode = self.newNodes[-1]
        newNodeDegree = 0
        
        selectedNodes = [] #Ensures multi-edges aren't drawn. Tracks of nodes that are already connected to new vertex.
        
        #A paper cannot make 2 citations to the same paper, hence ensure no mulitple edges.
        while(newNodeDegree < self.m):
            selectedNode = random.choice(self.G.nodes())#selected based on degree distribution.
            if(selectedNode not in selectedNodes):
                selectedNodes.append(selectedNode) #Node has been selected and is now appended to selectedNodes.
                newNodeDegree +=1
            else:
                print("Node {} already has an existing edge with New Node {}".format(selectedNode, newNode))
                pass
            
        #Drawing the edges.
        for node in selectedNodes:
            self.newEdges.append((newNode, selectedNode)) #Keeping track of (new) additional edges
            self.G.add_edge(newNode, node) #Adding nodes to the network.
            self.vertexDegree.append(node) #Adds new vertex to vertexDegree list, (m times).
            self.vertexDegree.append(selectedNode) #Adds existing vertices to vertexDegree list, an amount of times equal to the number of new edges attached.
            
    
    
        
        
        
        
    