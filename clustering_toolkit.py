#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 14 22:23:36 2018

@author: RamanSB
#CHANGELOG:
23-1-17: 
    Made into a module. 
    Removed loading from the file

"""

'''
(Link 1): https://networkx.github.io/documentation/networkx-1.10/reference/generated/networkx.algorithms.cluster.clustering.html?highlight=clustering#networkx.algorithms.cluster.clustering
(Link 2): https://networkx.github.io/documentation/networkx-1.10/reference/generated/networkx.algorithms.centrality.current_flow_betweenness_centrality.html#networkx.algorithms.centrality.current_flow_betweenness_centrality
(Link 3): https://networkx.github.io/documentation/networkx-1.10/reference/generated/networkx.algorithms.centrality.closeness_centrality.html#networkx.algorithms.centrality.closeness_centrality

'''
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import time

'''
Note social Network is undirected, activity network is directed - must consider 
when calculating certain metrics.

Change filePath according to your file location.
'''

def loadNetworkFromFilePath(filePath):
    return nx.gexf.read_gexf(filePath)

def calculateClusteringCoeffPerNode(graph):
    #We're after the activity network with this if statement.
    if(nx.is_weighted(graph) and nx.is_directed(graph)):
        #For weighted graphs clustering coefficients are calculated in a different way
        #See (Link 1 Above), however timestamps as weight are not of importance in determining 
        #the value of clustering coefficients
        print("We aim to meet the criteria of the activity network in this if statement")
    #We seek to impose a condition to extract the Social Network
    clustering_dict = nx.clustering(graph)
    clustering_coeffs = list(clustering_dict.values())
    
    return clustering_dict, clustering_coeffs
    
def plotClusteringHist(clustering_data, binsize=20):
    plt.hist(clustering_data, binsize, ec='black')
    plt.legend("Bin width = {}".format( 1/binsize))
    plt.xlabel("Clustering Coefficient Bins")
    plt.ylabel("Frequency")
    plt.title("Histogram of Clustering Coefficient")
    plt.figure()
    plt.show()
    
#current_flow_betweenness_centrality - uses electrical circuit to model information flow opposed
#to shortest path.    
def calculateClosenessC(graph):
    #We're after the activity network with this if statement.
    if(nx.is_weighted(graph) and nx.is_directed(graph)):
        #For weighted graphs clustering coefficients are calculated in a different way
        #See (Link 1 Above), however timestamps as weight are not of importance in determining 
        #the value of clustering coefficients
        print("We aim to meet the criteria of the activity network in this if statement")
    #We seek to impose a condition to extract the Social Network
    closeness_dict = nx.closeness_centrality(graph)
    closeness_values = list(closeness_dict.values())
    
    return closeness_dict, closeness_values

def plotClosenessHist(closeness_data, binsize=20):
    plt.hist(closeness_data, binsize, ec='black')
   # plt.legend("Bin width = " + 1/binsize)
    plt.xlabel("Closeness Centrality Bins")
    plt.ylabel("Frequency")
    plt.title("Histogram of Closeness Centrality")
    plt.figure()
    plt.show()
    
    
