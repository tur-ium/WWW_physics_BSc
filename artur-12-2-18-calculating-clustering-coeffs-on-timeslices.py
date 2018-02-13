# -*- coding: utf-8 -*-
"""
Created on Mon Feb 12 22:22:30 2018

@author: admin

Note that this will not work if there is a user called 'NaN'
"""
import Timeslice as ts
import networkx_extended as nx
import time
import matplotlib.pyplot as plt

#VARIABLES
dataPath = "Data/WeightedNetwork"
noMonths = 3
startDate = ts.EPOCH_MIN
endDate = ts.TIME_DICT["2009"]["JUNE"]

runtimes = list()
timesliceNames = list()
avgClusteringCoeffs = list()



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

    
counter = 0
Graph = nx.Graph()
Graph.add_edge('NaN','NaN',weight=1)  #Add a weighted edge in order to ensure that weighted addition can occur 

for YEAR in ["2007","2008","2009"]:
    for MONTH in ts.MONTHS:
        counter += 1
        
        startTime = time.time()
        if(ts.TIME_DICT[YEAR][MONTH] < startDate or ts.TIME_DICT[YEAR][MONTH] > endDate):
            continue
        print('{} {}'.format(MONTH, YEAR))
        
        if counter % noMonths == 0:
            Graph = nx.Graph()
            Graph.add_edge('NaN','NaN',weight=1) #Add a weighted edge in order to ensure that weighted addition can occur
        
        Graph = Graph + ts.loadGEXF("{}/{}_{}_WeightedGraph.gexf".format(dataPath,YEAR, MONTH))
        if len(Graph.edges('NaN','NaN')) > 0:
            Graph.remove_edge('NaN','NaN')  #Remove the fake edge
        
        print('CALCULATING CLUSTERING COEFFICIENTS')
        if counter % noMonths == 0:
            timesliceNames.append('{} {}'.format(MONTH, YEAR))   #Record name
            avgClustering, clusteringDict = computeClusteringCoefficients(Graph)
            avgClusteringCoeffs.append(avgClustering)
            print("Average Clustering - {} months up to and including {} - {}: {}".format(noMonths, YEAR, MONTH, avgClustering))
        plotClusteringHistogram(clusteringDict)
        
        #Time
        endTime = time.time()
        runtimes.append(endTime-startTime)
        print('RUNTIME: {}'.format(runtimes[-1]))
#PLOT AVG CLUSTERING COEFF OVER TIME
plt.figure(figsize=(10,5))
plt.title('Average clustering coefficients')
plt.ylabel('Av. clustering coefficient')
plt.xlabel('Timeslice')
plt.bar(timesliceNames,avgClusteringCoeffs)