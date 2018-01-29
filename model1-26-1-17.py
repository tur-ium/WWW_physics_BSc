# -*- coding: utf-8 -*-
"""
Created on Tue Jan 23 09:54:37 2018

@author: admin


#TODO: Plot order param
#TODO: Remove edges
#TODO: Read theory
"""

import clustering_toolkit as ctk
import networkx as nx
import random
import time

socialNetworkFile = "Data/social_network.gexf"
activityNetworkFile = "Data/activity_network_undirected.gexf"
#rootPath = "/Users/RamanSB/Documents/University/3rd-Year Physics/3rd Year Project/Real Data/"

startTime = time.time()

#isNetworksLoaded = False
if(not isNetworksLoaded):
    G_A = ctk.loadNetworkFromFilePath(activityNetworkFile)
    G_S = ctk.loadNetworkFromFilePath(socialNetworkFile)
    isNetworksLoaded = True

timeToLoadNetworksGEXF = time.time()-startTime
print("Network loaded in {}s".format(timeToLoadNetworksGEXF))

nodes_list = list(G_A.nodes())

model1_network = nx.MultiDiGraph()
model1_network.add_nodes_from(nodes_list)

#Order parameter

V = len(list(G_A.edges()))#Desired volume of the network
n = 0 #Number of edges added
model1_ccs = list()   #Log of clustering coefficients over time
model1_ncs = list()   #Log of number of connected components over time

while n < V:
    #A user sends a message to any other user in the network with equal probability
    from_user = random.choice(nodes_list)
    to_user = random.choice(nodes_list)
    model1_network.add_edge(from_user,to_user)
    n+=1
    if n % 1000 == 0:
        print('Calculating coefficients. Iteration: {}'.format(n))
        print('ORDER PARAMETER CANDIDATES:')
        #Number of SCCs, Av. SCC size
        SCCs = nx.strongly_connected_components(model1_network)   #Strongly Connected Components at time n
        
        av_comp_size = 0
        N =0
        for SCC in SCCs:
            av_comp_size+=len(SCC)
            N+=1
        av_comp_size=av_comp_size/N
        model1_ncs.append(N)
        
        print('Number of strongly-connected components: {}'.format(N))
        print('Av. size of strongly-connected components: {}'.format(av_comp_size))

#        model1_c_d, model1_c = ctk.calculateClusteringCoeffPerNode(model1_network)
#        av_c = sum(model1_c)/len(model1_c)
#        model1_ccs.append(av_c)
        print('Finished calculation')
#ctk.plotClusteringHist(model1_c)

