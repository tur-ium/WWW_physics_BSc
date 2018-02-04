#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  1 10:08:21 2018

@author: RamanSB
"""

import Timeslice as ts
import networkx as nx
import copy
import numpy as np
import time
import matplotlib.pyplot as plt


MONTH = ""
YEAR = 2007
'''
loadedGraph = ts.loadGEXF("/Users/RamanSB/Documents/University/3rd-Year Physics/3rd Year Project/Real Data/TimeSlicedData/GEXF/{}/{}_{}MultiDiGraph.gexf".format(YEAR, YEAR, MONTH))
nodeSet = []

noOfSCC = nx.number_strongly_connected_components(loadedGraph)
noOfWCC = nx.number_weakly_connected_components(loadedGraph)
WCC = nx.weakly_connected_components(loadedGraph)
SCC = nx.strongly_connected_components(loadedGraph)
'''
startTime = time.time()



def convertToSimpleGraph(Graph):
    G = nx.Graph(Graph)
    return G

def convertMultiDiGraphToWeighted(MultiDiGraph):
    G_W = nx.Graph(MultiDiGraph)
    weightedEdges = convertMultiEdgeToWeight(MultiDiGraph)
    for weightedEdge in weightedEdges:
        G_W[weightedEdge[0]][weightedEdge[1]]['weight'] = weightedEdge[2]
   
    return G_W


#Need to make this method more efficient.
#Returns list of tuples - [(node1, node2, weight), ...]
def convertMultiEdgeToWeight(MultiDiGraph):
    MultiDiGraphEdges = MultiDiGraph.edges()
    MultiGraph = MultiDiGraph.to_undirected() #Removes directionality i.e. [(1,2), (2,1)] ---> (1,2)
    uniqueEdges = list(set(MultiGraph.edges()))
    edgeWeights = []
    
    for uniqueEdge in uniqueEdges:
        edgeCounter = 0
        for edge in MultiDiGraphEdges:
            if(uniqueEdge == edge or uniqueEdge == edge[::-1]):
                edgeCounter += 1
        edgeWeights.append(edgeCounter)
     
    weightedEdges = []
    for i in range(len((edgeWeights))):
        weightedEdges.append((uniqueEdges[i][0], uniqueEdges[i][1], edgeWeights[i]))
    
    return weightedEdges
   
        
def computeClusteringCoefficients(Graph, isWeighted=False):
    clustering_dicts = nx.algorithms.cluster.clustering(Graph)
    #This causes the error - here's the doc: https://networkx.github.io/documentation/networkx-1.9/_modules/networkx/algorithms/cluster.html#average_clustering
    avgClusteringCoefficient = nx.average_clustering(Graph)
    return avgClusteringCoefficient, clustering_dicts
       
def plotClusteringHistogram(clusteringDict, binSize=20):
    clusteringValues = list(clusteringDict.values())
    plt.hist(clusteringValues, bins=binSize, ec='black')
    plt.title("Clustering Coefficient Histogram {}-{}".format(YEAR, MONTH))
    plt.xlabel("Clustering Coefficient Bins")
    plt.ylabel("Frequency")
    plt.figure()
    plt.show()


'''The histograms for annual timeslices I've got (2005 & 2006) work using the commented code below
(3 lines) - however for 2007 the code just doesn't run - it gets stuck on the convertMultiDiGraphToWeighted
method. - Need to investigate. 


'''


#weightedGraph = convertMultiDiGraphToWeighted(loadedGraph)
#clusteringDict = computeClusteringCoefficients(weightedGraph)
#plotClusteringHistogram(clusteringDict)


#In this nested for loop - i am loading the cumulative networks and plotting clustering histograms
#It works, but only when you remove the avgClustering variable and return only the clusteringdict.
for YEAR in ts.YEARS:
    for MONTH in ts.MONTHS:
        loadedGraph = ts.loadGEXF("/Users/RamanSB/Documents/University/3rd-Year Physics/3rd Year Project/Real Data/CumulativeNetwork/GEXF/{}/C{}_{}_MultiDiGraph.gexf".format(YEAR, YEAR, MONTH))
        Graph = convertToSimpleGraph(loadedGraph)
        avgClustering, clusteringDict = computeClusteringCoefficients(Graph)
        print("Average Clustering - {} - {}: {}".format(YEAR, MONTH, avgClustering))
        plotClusteringHistogram(clusteringDict)

print("Code runs in {}".format(time.time()-startTime))





'''
GENERATES TIMESLICED DATA. - DO NOT RUN


activityEdgeList = ts.readEdgelistFromPath(ts.activityEdgelistPath, isWeighted=True)
for YEAR in ts.YEARS:
    for MONTH in ts.MONTHS:
        timeSliceEdgeList = ts.timeSliceEdges(activityEdgeList, cutOffTime=ts.TIME_DICT[YEAR][MONTH], retainWeights=False)
        timeSliceGraph = ts.generateTimeSliceGraph(timeSliceEdgeList)
        ts.createGEXFFromGraph(timeSliceGraph, ts.cumulative_filePath_gexf+YEAR+"/", "C"+YEAR+"_"+MONTH+"_MultiDiGraph.gexf")
        ts.writeEdgeListToFile(timeSliceEdgeList, ts.cumulative_filePath_text+YEAR+"/", "C"+YEAR+"_"+MONTH+".txt")
'''


'''
type(G)
Out[146]: networkx.classes.multidigraph.MultiDiGraph

Out[156]: 
[(7, 4),
 (1, 2),
 (1, 2),
 (1, 5),
 (1, 3),
 (2, 3),
 (3, 7),
 (4, 3),
 (4, 7),
 (5, 4),
 (6, 5)]

G.nodes()
Out[148]: [7, 1, 2, 3, 4, 5, 6]
'''
    