# -*- coding: utf-8 -*-
"""
Created on Fri Feb  2 18:33:25 2018

@author: Ramandeep Singh
@author: Artur Donaldson

#TODO: Add functionality for adding DiGraphs
#TODO: Add functionality for adding MultiDiGraphs
#TODO: Use this to make timslices
"""
from networkx import *
import random 

class Graph(Graph):
    def __add__(self,other):
        '''Add two graphs'''
        new_network = Graph()
        if not (is_weighted(self) and is_weighted(other)):
            raise Exception("Adding a weighted graph to an unweighted graph is not implemented")
        if is_weighted(self) and is_weighted(other):
            new_network.add_weighted_edges_from(self.edges(data=True))
            new_network.add_weighted_edges_from(other.edges(data=True))   #Note to Ramandeep: use .edges(data=True) to get the edge weights
        else:
            new_network.add_edges_from(self.edges())
            new_network.add_edges_from(other.edges())
        return new_network
    
#TEST#
G1 = Graph()
G2 = Graph()
G1.add_edges_from([(1,2),(2,1),(3,1)])
G2.add_edges_from([(3,1), (4,1), (5,3)])

allEdges = list(G1.edges()) + list(G2.edges())

for edge in G1.edges():
    G1[edge[0]][edge[1]]['weight']= random.choices([1,2,3,4,5], [0.2,0.2,0.2,0.2,0.2])
    
for edge in G2.edges():
    G2[edge[0]][edge[1]]['weight'] = random.choices([1,2,3,4,5],[0.2,0.2,0.2,0.2,0.2])

