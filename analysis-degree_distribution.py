# -*- coding: utf-8 -*-
"""
Created on Sat Jan 13 12:46:06 2018

@author: admin

%time loadActivityData('Data/',True)
Wall time: 24.5 s

"""

import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

def loadActivityData(dataFolder,directed):
    '''Loads activity network from the gexf file into a networkx graph'''
    if not directed:
        return nx.gexf.read_gexf(dataFolder+'activity_network_undirected.gexf')
    else:
        return nx.gexf.read_gexf(dataFolder+'activity_network_multidigraph.gexf')

def plot_distribution(d,name,n=100):
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
    log_max_degree = np.log10(max(d.values()))
    bin_edges = np.logspace(0,log_max_degree,n-1)
    bin_edges = list(bin_edges)
    bin_edges.insert(0,0.)
    print(bin_edges)
    
    plt.figure()
    degree_dist,bins = np.histogram(list(d.values()),bins=bin_edges)
    bin_centres = [sum(bin_edges[i:i+1]) for i in range(0,len(bin_edges)-1)]
    plt.loglog(bin_centres,degree_dist,'+')
    plt.xlim(1,1e4)
    plt.grid()
    plt.title('{} distribution'.format(name.capitalize()))
    plt.xlabel('log({})'.format(name))
    plt.ylabel('log(Frequency)')
    plt.figure()
    
    degree_dist,degrees,patches = plt.hist(d.values(),bins=bin_edges,cumulative=True)
    plt.title('Cumulative {} distribution'.format(name))
    plt.xlabel(name)
    plt.ylabel('Cumulative frequency')
#activity_data_undirected= loadActivityData('Data/',False)

activity_data_multigraph= loadActivityData('Data/',True)

degree_dict = dict(nx.degree(activity_data_multigraph))   #Total # of posts sent AND received (undirected) as a dict
in_degree_dict = dict(activity_data_multigraph.in_degree())   #Total # of posts received
out_degree_dict = dict(activity_data_multigraph.out_degree())   #Total # of posts sent
#%%
#Check
N = len(degree_dict.values())
print(N)
print('Degree of node 1: {}'.format(degree_dict['1']))

#%%
#Basic stats
print('### BASIC STATS')
degree_av = sum(degree_dict.values())/N
print('Average degree: {:.3g}'.format(degree_av))
in_degree_av = sum(in_degree_dict.values())/N
print('Average in degree: {:.3g}'.format(in_degree_av))
out_degree_av = sum(out_degree_dict.values())/N
print('Average out degree: {:.3g}'.format(out_degree_av))
#Plot degree distribution
plot_distribution(degree_dict,'degree')
plot_distribution(in_degree_dict,'in degree')
plot_distribution(out_degree_dict,'out degree')
