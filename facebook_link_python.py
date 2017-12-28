#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 21 16:13:59 2017

@author: RamanSB
"""
import copy
import time

dataPath = "facebook_links_data/facebook-links.txt.anon"
lineCounter = 1000
data = []



def readData():
    rawData = open(dataPath).read().splitlines()#[:lineCounter]
    unformattedData = []
    for lines in rawData:
        unformattedData.append(lines.split())
    
    return unformattedData

def getEdgeList(data):
    edgeList = []
    
    for edgeData in data:
        edgeList.append([int(edgeData[0]), int(edgeData[1])])
    
    #print(edgeList)
    print("Edge list length:" + str(len(edgeList)))
    return sorted(edgeList)


def getNodeSet(edgeList):

    
    nodeTempList1 = []
    nodeTempList2 = []
    for edgePair in edgeList:
        nodeTempList1.append(edgePair[0])
        nodeTempList2.append(edgePair[1])

    nodeSet1 = set(nodeTempList1)
    nodeSet2 = set(nodeTempList2)
  
    networkNodeSet = set(list(nodeSet1) + list(nodeSet2))
    
    print("Number of nodes in network:" + str(len(networkNodeSet)))
    print(len(nodeSet1))
    print(len(nodeSet2))
    
    return list(networkNodeSet), nodeTempList1, nodeTempList2

def swapListElements(List2D):
    for i in range(len(List2D)):
        List2D[i][0], List2D[i][1] = List2D[i][1], List2D[i][0]
        
    return List2D

def redrawEdges(edgeList):
    edge_1 = sorted(edgeList, key=lambda x : x[0])
    edge_2 = sorted(edgeList, key=lambda x: x[1])
    edge_2 = copy.deepcopy(edge_2)
    edge_2 = swapListElements(edge_2)
    #print(edge_1[:10])
    #print(edge_2[:10])
    allEdges = edge_1 + edge_2
    edgeSet = set(tuple(edge) for edge in allEdges)
    
    finalEdgeList = list(edgeSet)
    print("Edge List Length:" + str(len(finalEdgeList)))
    return finalEdgeList
    
#Leave this commented out, not needed 
'''
def writeSortedEdgeToFile(sortedEdges):
    with open("facebook_links_data/.txt", 'w') as file_handler:
        for edge in sortedEdges:
            file_handler.write("{}\n".format(edge))
  '''  
    
initialTime = time.time()
data = readData()
edgeList= getEdgeList(data)

NodeSet, NEdge_1, NEdge_2 = getNodeSet(edgeList)
#Running this with the edgeList from the dataset 'edgeList' we find we have
#63671 nodes in our network, 60102 / 63630 


finalEdgeList = redrawEdges(edgeList)
#Running getNodeSet with redrawn Edges we have '63731' nodes.
getNodeSet(finalEdgeList)

#Node set contains consecutive integers from 1, to len(NodeSet)
#writeSortedEdgeToFile(edgeList)






finalTime = time.time()


processTime = finalTime-initialTime

print("Code runs in {} seconds".format(processTime))