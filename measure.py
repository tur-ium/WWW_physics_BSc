# -*- coding: utf-8 -*-
"""
measure.py

Any measurements of quantities on the network

"""
import networkx_extended as nx

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