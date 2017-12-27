# -*- coding: utf-8 -*-
"""
Created on Wed Dec 27 17:28:46 2017
NETWORK TOOLKIT

@authors: Ramandeep and Artur

#CHANGES:
27-11-17:Checked KONECT Facebook wallpost description. 1st col is from, 2nd is \
to, therefore have changed `getAdjacencyMatrix` accordingly
#TODO:
* Get adjacency tree/adjacency list representation
"""
import numpy as np

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

def getAdjacencyMatrix(vertices,edgeList,directed=True):
    '''Creates an adjacency matrix for an edgeList e.g. [[0,1], ..., [i,j],...]\
where edges are from i TO j
    PARAMETERS
    ---
    vertices: list 
        List of labels for each vertex. The order determines the order of\
columns in the adjacency matrix
    edgeList: List of edges where 1st element is the beginning of the edge, and\
2nd is at the end
    directed: boolean (default: True)
        Set as True if the network is undirected and edges are not repeated
    '''
    N = len(vertices)
    A = np.zeros((N,N))
    #If there exists an edge from vertex i to j, we populate the adjancey matrix column i-j.
    for i, j in edgeList:
        fromNode = vertices.index(i)
        toNode = vertices.index(j)
        A[fromNode,toNode] += 1
        if directed == False:
            A[toNode,fromNode] += 1
    return A
