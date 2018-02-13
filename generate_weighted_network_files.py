# -*- coding: utf-8 -*-
"""
Created on Wed Feb  7 14:35:31 2018

@author: admin

#Start time: 23:50
"""
import networkx as nx
import Timeslice as ts
import time
import matplotlib.pyplot as plt
import pickle

def convertToSimpleGraph(Graph):
    G = nx.Graph(Graph)
    return G
def convertMultiDiGraphToWeighted(MultiDiGraph):
    G_W = nx.Graph(MultiDiGraph)
    weightedEdges = convertMultiEdgeToWeight(MultiDiGraph)
    for weightedEdge in weightedEdges:
        G_W[weightedEdge[0]][weightedEdge[1]]['weight'] = weightedEdge[2]
   
    return G_W
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


runtimes = list()
timesliceNames = list()
avgClusteringCoeffs = list()

#In this nested for loop - i am loading the cumulative networks and plotting clustering histograms
#It works, but only when you remove the avgClustering variable and return only the clusteringdict.

dataPath = "Data/TimeSlicedDataNew/TimeSlicedData"   #Root directory of GEXF and edgeList files
savePath = "Data/WeightedData"

for YEAR in ["2006","2007","2008","2009"]:
    for MONTH in ts.MONTHS:
        startTime = time.time()
        if(ts.TIME_DICT[YEAR][MONTH] < ts.EPOCH_MIN or ts.TIME_DICT[YEAR][MONTH] >= ts.EPOCH_MAX):
            continue
        print('{} {}'.format(MONTH, YEAR))
        timesliceNames.append('{} {}'.format(MONTH, YEAR))   #Record name
        
        #Load multidigraph
        loadedGraph = ts.loadGEXF("{}/GEXF/{}/{}_{}_MultiDiGraph.gexf".format(dataPath,YEAR, YEAR, MONTH))
        
        print('EDGES: {}'.format(len(loadedGraph.edges())))
        
        #Convert to weighted undirected graph (edges = number of interactions)
        Graph = convertMultiDiGraphToWeighted(loadedGraph)
        
        #Save weighted graph
        nx.write_gexf(Graph,"{}_{}_WeightedGraph.gexf".format(YEAR, MONTH))
        
        #Calculate clustering coefficients
        print('CALCULATING CLUSTERING COEFFICIENTS')
        avgClustering, clusteringDict = computeClusteringCoefficients(Graph)
        avgClusteringCoeffs.append(avgClustering)
        print("Average Clustering - {} - {}: {}".format(YEAR, MONTH, avgClustering))
        plotClusteringHistogram(clusteringDict)
        
        #Time
        endTime = time.time()
        runtimes.append(endTime-startTime)
        print('RUNTIME: {}'.format(runtimes[-1]))
        
pickle.dump(avgClusteringCoeffs,open('avgClusteringCoeffs{}-{}.pkl'.format(timesliceNames[0],timesliceNames[-1]),'wb'))
print("NOT CALCULATING CLUSTERING COEFFICIENT")
print("Code runs in {}".format(time.time()-startTime))
fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(timesliceNames,runtimes)
ax.set_title('Runtimes')
ax.set_ylabel('Runtime (s)')