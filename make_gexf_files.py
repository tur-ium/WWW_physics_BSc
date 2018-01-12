# -*- coding: utf-8 -*-
"""
Created on Fri Jan 12 21:19:47 2018

@author: Artur

#Note on runtime:
#Reason for using gexf to store network is that it is slightly quicker to load
# than reading the edge file directly
[In]  %timeit a_network = nx.read_weighted_edgelist(dataPath)
6.45 s ± 103 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)

#Reading gexf is quicker by a factor of about 1.5
[In] %timeit a_network = nx.gexf.read_gexf('Data/activity_network')
4.43 s ± 74.1 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)

"""
#LOAD MODULES
import networkx as nx

#Load wall post data
dataPath = 'Data/activity_network_edge_list.txt' #Source: http://socialnetworks.mpi-sws.org/data-wosn2009.html

def saveActivityData(graph,gexfPath):
    '''Saves a networkx Graph object to a gexf file `[gexfPath]'''
    nx.gexf.write_gexf(activity_network,gexfPath)

def readData():
    '''Read data from dataPath into an array of values'''
    rawData = open(dataPath).read().splitlines()
    unformattedData = []
    for lines in rawData:
        unformattedData.append(lines.split())
    
    return unformattedData

#UNDIRECTED GRAPH
print('Making undirected graph')
activity_network = nx.read_weighted_edgelist(dataPath,create_using=nx.Graph())
#SAVE GEXF for future use
print('Saving gexf file')
saveActivityData(activity_network,'Data/activity_network_multidigraph.gexf')

#MULTIDIGRAPH
print('Making multidigraph')
activity_network = nx.read_weighted_edgelist(dataPath,create_using=nx.MultiDiGraph())
#SAVE GEXF for future use
print('Saving gexf file')
saveActivityData(activity_network,'Data/activity_network_multidigraph.gexf')

#VALIDATION
print('VALIDATION')
#Checking the networkx graph representation
activityNetworkNodes = len(activity_network)
#Read data directly from edge list file to compare
activity_data = readData()
print('First few edges in activity network: {}'.format(activity_data[0:5]))

print('Number of nodes in activity network: {}'.format(activityNetworkNodes))
print('Wall posts made by user 1:\n {}'.format(activity_network['1']))


#SAVE GEXF for future use
print('Saving gexf file')
saveActivityData(activity_network,'Data/activity_network_multidigraph.gexf')



##Information about social network
#social_network_node_count = 63731
#
