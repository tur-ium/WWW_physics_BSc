#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 30 13:56:40 2017

@author: RamanSB
"""
import numpy as np
import networkx

data_directory = 'facebook'

#Ego whose ego-network we are considering.
#Enter the ego who's network you want to consider.
ego = "107"



#Number of verticies, n in ego-network is given by the number of lines in .feat file.
no_vertex = 0
no_of_lines = 0

alters_feat = []
#Dictionary mapping alter id given in .feat file to line numbers.
dict_id_to_line = {}


feat_file = open(data_directory + "/"+ego+".feat")
for line in feat_file:
    no_vertex+=1
    data_alter_id = int(line.split(" ")[0])
    alters_feat.append(data_alter_id)
    #Mapping alter_id's labelled by data to line number. (Useful for adjancey matrix)
    dict_id_to_line[data_alter_id] = no_vertex
   

#print(alters_feat)
print("Number of alters in total:" + str(len(alters_feat)))

print("ego " + ego+" contains " +str(no_vertex) + " vertices in his/her ego-network")


#Adjancey matrix - A (nxn) - Symmetric
A = np.array([np.zeros(no_vertex) for i in range(no_vertex)])


#Edge file contains directed edges.
#Finding whether there is an edge from vertex j to i.
edges_file = open(data_directory+"/"+ego+".edges")
edges = open(data_directory+"/"+ego+".edges").read().splitlines()

alters_edge = []
#Line numbers begin at 1. Adjancey matrix begins indexing from 0.
alters_mapped = []

edge_list = []   #Create an edge list
graph = networkx.Graph()

for edge in edges:
    edge_pairs = edge.split(" ")
    alters_edge.append(int(edge_pairs[0]))
    alters_edge.append(int(edge_pairs[1]))

    #Map the ids from the paper to more helpful indices
    vertex_j = dict_id_to_line[int(edge_pairs[0])]
    vertex_i = dict_id_to_line[int(edge_pairs[1])]
        
    alters_mapped.append(vertex_j)
    alters_mapped.append(vertex_i)

    edge_list.append([vertex_i,vertex_j])   #Add to the edge list
    graph.add_edge(vertex_i,vertex_j)

    
    A[vertex_i-1, vertex_j-1] = 1

print('Nodes in graph', len(graph))
#Note: Number of nodes in graph is half the length of the edge list as expected,
# since the edge_list contains an edge in each direction, whereas Graph
# objects are undirected

print(len(set(alters_edge)))
print(len(set(alters_mapped)))
print("Max Alter Mapped Id:" + str(max(alters_mapped)))
print("Min Alter Mapped Id: " + str(min(alters_mapped)))
print("Max AlterId: " + str(max(alters_edge)))
print("Min Alter Id:" + str(min(alters_edge)))

print('ADJACENCY MATRIX:')
print(A)

#Finding the transpose matrix
A_T = np.transpose(A)
#print(A_T)


#Checking whether transpose == normal matrix, as adjancency matricies must be symmetric.
print('Matrix is symmetric' if np.all(A==A_T) else 'Matrix is not symmetric')


print('Calculating Eigenvector centrality')
#Calculate eigenvector centrality
evals, evecs = np.linalg.eig(A)
index = evals.argmax()
eval_max = evals[index]   #The maximum eigenvalue determines centrality
centrality = evecs[index]   #The leading eigenvector determines the limiting centrality

print('Maximum eigenvalue of adjacency matrix: {}'.format(eval_max))

#Check using Ch.7 eq. (7.6) Newmann 'Networks: An Introduction'
# Centrality = 1/eval_max * sum(A_ij * x_j)
i = 0
RHS = 0
for j in range(no_vertex):
    RHS += 1/eval_max * A[i,j] * centrality[j]
#TODO: The centrality doesn't match up with eq. (7.6)
#TODO: This doesn't agree with networkx

print(centrality)

#VALIDATION    
#Check against Networkx
print('Calculating Eigenvector centrality using Networkx')
centrality_nx = networkx.eigenvector_centrality(graph)

print('Centralities:\n',centrality_nx)

alters = list(centrality_nx.keys())
#Check that we have the same keys for the alters (the line numbers)
print('Same keys? ',set(centrality_nx.keys())==set(alters_mapped))
test_node = alters_mapped[1]   #Choose an arbitrary id to test
test_centrality = centrality_nx[test_node]
#See if any of the elements are equal using float comparison
equal = (abs(centrality - test_centrality)<2**-10)  
index = False
for diff in equal:
    if diff:
        break
    index+=1
print('Match found for centrality calculated: ', index, centrality[index])
i = 0
RHS = 0
for j in range(len(centrality_nx)):
    key = list(centrality_nx.keys())[j]
    RHS += 1/eval_max * A[i,j] * centrality_nx[key]
#Problem: Not every node in features is in the edges file 
# Therefore indices in centrality_nx do not correspond to those in the adjacency matrix