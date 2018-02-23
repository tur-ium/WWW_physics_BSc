# -*- coding: utf-8 -*-
"""
measure.py

Any measurements of quantities on the network

"""
import networkx_extended as nx
import matplotlib.pyplot as plt
import time
import numpy as np

#Find degree distribution
def getDegreeDist(WeightedGraph):
    '''Gets the degree distribution for a weighted graph where weights represent\
number of messages sent
RETURNS
---
degree_dict:
    Dictionary (user: degree)
'''

    degree_dict = dict() #person: degree
     
    for edge in WeightedGraph.edges():
        #For each edge in the Weighted Graph, add its weight to the degree of \
        # the source and target nodes
        
        s = edge[0]
        t = edge[1]
        weight = WeightedGraph[s][t]['weight']
        
        #Add people to the degree dictionary if they are not already in it
        if not s in degree_dict:
            degree_dict[s] = 0
        if not t in degree_dict:
            degree_dict[t] = 0
        
        degree_dict[s]+=weight
        degree_dict[t]+=weight
    return degree_dict

#Largest Component Size
def computeLCS(G):
    '''Computes largest component size on the graph G'''
    return len(max(nx.connected_components(G)))

#Average Clustering Coefficient
def computeClusteringCoefficient(G, isWeighted=False):
    '''Compute average and local clustering coefficients on the graph G
    RETURNS
    ---
    avgClusteringCoefficient: float
        Average clustering coefficient on the network
    clustering_dicts: dict (node: local clustering coefficient)
        Local clustering coefficient for each node on the network
    '''
    clustering_dicts = nx.algorithms.cluster.clustering(G)
    avgClusteringCoefficient = nx.average_clustering(G)
    return avgClusteringCoefficient, clustering_dicts

def compareNeighbourDegree(G):
    '''Compares average degree with average degree for each neighbour'''
    k_nn = dict(nx.neighbor_degree.average_neighbor_degree(G,weight='weight'))
    k = dict(nx.degree(G))
    
    #Values
    k_nn_list = list(k_nn.values())
    k_list = list(k.values())

    #Define average function
    av = lambda x: sum(x)/len(x)
    
    #Average
    k_nn_av = av(k_nn_list)
    k_av = av(k_list)
    print("Average of neighbour degree:{}, average degree: {}".format(k_nn_av,k_av))
    
#Plot distribution
def plot_distribution(d,name,n=1000):
    '''Plots loglog frequency and cumulative distributions for a quantity
    PARAMETERS
    ---
    d: dictionary
        Dictionary of values to be histogrammed
    name: string
        Name of the quantity represented by the list of values
    n: int
        Number of bins
    ''' 
#    log_max_degree = np.log10(max(d.values()))
    n=len(d)
    bin_edges = np.linspace(0,max(d.values()),n-1)
    bin_edges = list(bin_edges)
    bin_edges.insert(0,0.)
    #print(bin_edges)
    
    #TODO: Loop through and create a dictionary {degree: frequency}
    
    plt.figure()
    start = time.time()
    degree_dist,bins = np.histogram(list(d.values()),bins=bin_edges)
    end = time.time()
    print('Time to perform histogramming: {} s'.format(end-start))
    bin_centres = [sum(bin_edges[i:i+1]) for i in range(0,len(bin_edges)-1)]
    plt.loglog(bin_centres,degree_dist,'+')
    plt.xlim(1,1e4)
    plt.grid()
    plt.title('{} distribution'.format(name.capitalize()))
    plt.xlabel('log({})'.format(name))
    plt.ylabel('log(Frequency)')
    
#    plt.figure()
#    degree_dist,degrees,patches = plt.hist(d.values(),bins=bin_edges,cumulative=True)
#    plt.title('Cumulative {} distribution'.format(name))
#    plt.xlabel(name)
#    plt.ylabel('Cumulative frequency')