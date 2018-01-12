# -*- coding: utf-8 -*-
"""
Created on Fri Jan 12 22:41:40 2018

@author: Artur

#Note on runtime:
#Reason for using gexf to store network is that it is slightly quicker to load
# than reading the edge file directly
[In]  %timeit a_network = nx.read_weighted_edgelist(dataPath)
6.45 s ± 103 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)

#Reading gexf is quicker by a factor of about 1.5
[In] %timeit a_network = nx.gexf.read_gexf('Data/activity_network')
4.43 s ± 74.1 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)author: admin
"""

import networkx as nx

def loadActivityData(dataFolder,directed):
    '''Loads activity network from the gexf file into a networkx graph'''
    if not directed:
        return nx.gexf.read_gexf(dataFolder+'activity_network_undirected.gexf')
    else:
        return nx.gexf.read_gexf(dataFolder+'activity_network_multidigraph.gexf')

activity_data_undirected= loadActivityData('Data/',False)
activity_data_multigraph= loadActivityData('Data/',True)