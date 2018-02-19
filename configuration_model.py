# -*- coding: utf-8 -*-
"""
Created on Fri Feb 16 15:53:29 2018

@author: ad6315
#NOTE: Model produces a weighted network. No self-loops are allowed (i.e. does \
    not account for users posting on their own wall)
#TODO: Degree distribution
"""
#IMPORT MODULES
import random
import networkx as nx
import matplotlib.pyplot as plt
import pickle

#PARAMETERS
# Choose degree distribution
dataPath = 'C:/Users/admin/Documents/Physics/year 3/WWWPhysics-PC/empirical/Results'
no_of_iterations = 100

def load_empirical_degree_dist(dataPath):
    degree_dict_original = pickle.load(open('{}/2008_DEC_Weighted-degree_dict.pkl'.format(dataPath),'rb'))
    degree_dict = dict()
    nodes_to_use = dict(degree_dict_original).keys()
    for n in nodes_to_use:
        degree_dict[n] = degree_dict_original[n]
    return degree_dict

def generateConfigNetwork(degree_dict,network=nx.Graph(),self_loops=False):
    '''Generate a configurational network based on a dictionary of degrees (keys\
= node, values = degree of node.
    PARAMETERS
    ---
    degree_dict: dict (node_label: degree)
    
    network: networkx graph object (default: networkx.Graph)
        If defined, use add edges to the network `network`
    RETURNS
    ---
    F: networkx graph object
'''
    node_list = list(degree_dict.keys())
    k_list = list(degree_dict.values())   #Degree of each node, is returned in same order as keys
    
    if sum(k_list) % 2 != 0:
        raise Exception("Sum of degree distribution must be an even number")
    
    s = 0   #Index of current stub
    stub_dict = dict()   #Stub -> node on which the stub can be found
    #ADD STUBS TO EACH NODE
    for n, k in degree_dict.items():
        #Add k stubs to the dict of stubs for k, n in degree_dict.items():
        i = 0
        while i < k:
            stub_dict[s] = n  #Assign key of node, n, to the stub s
            s += 1   #Move onto the next stub
            i += 1
    
    #print(stub_dict)
    
    F = network  #Create a network representing Facebook activity network
    F.add_nodes_from(node_list)   #Add the nodes
    
    #JOIN STUBS TO FORM EDGES
    while len(stub_dict) > 1:
        stub_idx, s = stub_dict.popitem()  #Label of source node
        #print(stub_dict)
        #print(s)
        t_stub_idx = random.choice(list(stub_dict.keys()))   #Choose target stub index
        t = stub_dict.pop(t_stub_idx)
        #print(t)
        
        if t==s:
            if self_loops:
                if not t in F[s].keys():
                    F.add_edge(s,t)
        if not t in F[s].keys() and t != s:
            F.add_edge(s,t)
            F[s][t]['weight'] = 1
        elif t in F[s].keys():
            F[s][t]['weight'] += 1
            print("DOUBLE EDGE")
        elif t == s:
            print('SELF-LOOP')
            #This is a problem as the node will have one greater degree than it should
            # but for large networks the probability of a self-loop on a random graph\
            # will be small
        else:
            raise Exception("Unknown error")
    return F

#TESTING: LIMIT TO ONLY LAST N nodes
degree_dict_original = pickle.load(open('{}/G_A-degree_dict.pkl'.format(dataPath),'rb'))
degree_dict = load_empirical_degree_dist(dataPath)

#TESTING: PRINT DEGREE DIST
#if len(degree_dict) < 100:
#    print('DEGREE DICT: {}'.format(degree_dict))




