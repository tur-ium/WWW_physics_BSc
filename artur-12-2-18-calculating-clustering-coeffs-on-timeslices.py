# -*- coding: utf-8 -*-
"""
Created on Mon Feb 12 22:22:30 2018

@author: admin

TODO: Uncertainty
    Sampling
    Rerun
TODO: Null models - significance

TODO: number of users increases over time?
TODO: Av. degree
TOD0: Read Networkx code

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
endDate = ts.TIME_DICT["2009"]["JUN"]

runtimes = list()
timesliceNames = list()
avgClusteringCoeffs = list()
degreeList = list()


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

for YEAR in ["2007","2008"]:
    for MONTH in ts.MONTHS:
        counter += 1
        
        startTime = time.time()
        if(ts.TIME_DICT[YEAR][MONTH] < startDate or ts.TIME_DICT[YEAR][MONTH] > endDate-1):
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
            degree = sum(dict(nx.degree(Graph)).values())/len(Graph.nodes)
            degreeList.append(degree)
            avgClustering, clusteringDict = computeClusteringCoefficients(Graph)
            avgClusteringCoeffs.append(avgClustering)
            print("Average Clustering - {} months up to and including {} - {}: {}".format(noMonths, YEAR, MONTH, avgClustering))
        plotClusteringHistogram(clusteringDict)
        
        #Time
        endTime = time.time()
        runtimes.append(endTime-startTime)
        print('RUNTIME: {}'.format(runtimes[-1]))
#PLOT AVG CLUSTERING COEFF OVER TIME
fig = plt.figure(figsize=(10,3))
ax = fig.add_subplot(311)
ax1 = fig.add_subplot(313)
ax.set_title('Average clustering coefficients')
ax.set_ylabel('Av. clustering coefficient')
ax.set_xlabel('Timeslice')
ax1.set_title('Average degree')
ax1.set_ylabel('Av. degree')
ax1.set_xlabel('Timeslice')
ax.plot(range(len(timesliceNames)),avgClusteringCoeffs,'g-')
ax1.plot(range(len(timesliceNames)),degreeList,'b--')
ax.set_xticklabels(timesliceNames)
ax1.set_xticklabels(timesliceNames)