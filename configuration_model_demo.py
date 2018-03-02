# -*- coding: utf-8 -*-
"""
Created on Fri Feb 16 15:53:29 2018

@author: ad6315

#Generates LCS and ACC graphs for Configurational Model

#TODO: Plot results from 1/3/18
"""
#IMPORT MODULES
import random
import networkx as nx
import matplotlib.pyplot as plt
import pickle
from measure import plot_distribution, getDegreeDist, computeLCS, computeClusteringCoefficient
import empirical.Timeslice as ts
import numpy as np
import time

#PARAMETERS
iterations = 1

# Choose degree distribution
dataPath = 'C:/Users/admin/Documents/Physics/year 3/WWWPhysics-PC/empirical/Results'

def load_empirical_degree_dist(dataPath):
    degree_dict_original = pickle.load(open('{}/2008_DEC_Weighted-degree_dict.pkl'.format(dataPath),'rb'))
    degree_dict = dict()
    nodes_to_use = dict(degree_dict_original).keys()
    for n in nodes_to_use:
        degree_dict[n] = degree_dict_original[n]
    return degree_dict

#%%
class Config_Network():
    def __init__(self,degree_dict,network=nx.Graph(),allow_self_loops=False):
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
        self.node_list = list(degree_dict.keys())
        self.k_list = list(degree_dict.values())   #Degree of each node, is returned in same order as keys
        self.self_loops = 0   #Number of self-edges
        self.parallel_edges = 0   #Number of parallel edges
        self.allow_self_loops = allow_self_loops
        
        if sum(self.k_list) % 2 != 0:
            raise Exception("Sum of degree distribution must be an even number")
        
        s = 0   #Index of current stub
        self.stub_dict = dict()   #Stub -> node on which the stub can be found
        #ADD STUBS TO EACH NODE
        for n, k in degree_dict.items():  #n=node label, k = degree
            #Add k stubs to the dict of stubs for k, n in degree_dict.items():
            i = 0
            while i < k:
                self.stub_dict[s] = n  #Assign key of node, n, to the stub s
                s += 1   #Move onto the next stub
                i += 1
        
        #print(stub_dict)
        self.G = network  #Create a network representing Facebook activity network
        self.G.add_nodes_from(self.node_list)   #Add the nodes
    def iterate(self):
        '''JOIN A SINGLE PAIR OF STUBS'''
        if len(self.stub_dict)>1:
            stub_idx, s = self.stub_dict.popitem()  #Label of source node
            #print(stub_dict)
            #print(s)
            t_stub_idx = random.choice(list(self.stub_dict.keys()))   #Choose target stub index
            t = self.stub_dict.pop(t_stub_idx)
            #print(t)
            
            if not t in self.G[s].keys() and t != s:
                #Edge does not exist and it is not a self-loop
                self.G.add_edge(s,t)
                self.G[s][t]['weight'] = 1
            elif t in self.G[s].keys():
                #Edge does not exist
                self.parallel_edges+=1
                self.G[s][t]['weight'] += 1
            else:
                #Self-loop
                self.self_loops+=1
                if self.allow_self_loops:
                    if not t in self.G[s].keys():
                        self.G.add_edge(s,t)
                #raise Exception("Unknown error")
        else:
            print("No stubs left")
            
        return self.G
    def iterate_recursively(self,allow_self_loops=False):
        '''JOIN STUBS TO FORM EDGES'''
        while len(self.stub_dict) > 1:
            stub_idx, s = self.stub_dict.popitem()  #Label of source node
            #print(stub_dict)
            #print(s)
            t_stub_idx = random.choice(list(self.stub_dict.keys()))   #Choose target stub index
            t = self.stub_dict.pop(t_stub_idx)
            #print(t)
            
            if not t in self.G[s].keys() and t != s:
                #Edge does not exist and it is not a self-loop
                self.G.add_edge(s,t)
                self.G[s][t]['weight'] = 1
            elif t in self.G[s].keys():
                #Edge does not exist
                self.parallel_edges+=1
                self.G[s][t]['weight'] += 1
            else:
                #Self-loop
                self.self_loops+=1
                if allow_self_loops:
                    if not t in self.G[s].keys():
                        self.G.add_edge(s,t)
                #raise Exception("Unknown error")
            
            
        return self.G


#%%Load empirical degree dict
loadedGraph = ts.loadGEXF("C:/Users/admin/Documents/Physics/year 3/WWWPhysics-PC/empirical/Data/WeightedNetwork/2008_DEC_WeightedGraph.gexf")
degree_dict_original = getDegreeDist(nx.gexf.read_gexf("C:/Users/admin/Documents/Physics/year 3/WWWPhysics-PC/empirical/Data/WeightedNetwork/2008_DEC_WeightedGraph.gexf"))
node_list = list(degree_dict_original.keys())

#TESTING: Restrict degree dict to first 10000 nodes
degree_dict = degree_dict_original
#degree_dict = dict()
#for node in node_list[:1000]:
#    degree_dict[node]=degree_dict_original[node]

#%% PREPARE FOR WRITING DATA

saveFile = 'empirical/Results/config-model_ResultsV={}N={}.csv'.format(V,N)
try:
    f = open(saveFile,'w')
except IOError:
    print("Problem opening file,adding a number to the end")
    f= open(saveFile+'1','w')

#%%TESTING: TOY NETWORK

#G_model = Config_Network({0:1,1:2,2:1,3:1,4:1},nx.Graph())
#G_model.iterate()
#nx.draw_networkx(G_model.G)
#%% 
def addMessages(G_model,step,V):
    '''Expand network `G_model` up to a volume V.'''    
    n_list = list()
    lcs_list = list()  #Largest component
    acc_list = list()  #Average clustering coefficient
    
    n = 0
    while V > 0:
        G_model.iterate()
        
        V = len(G_model.stub_dict)
        #print(n)
        if (n-1) % step == 0:
            n_list.append(n)
            lcs = computeLCS(G_model.G)   #Largest component size
            acc,lccs = computeClusteringCoefficient(G_model.G)   #Calculate average clustering coefficient and local clustering coefficients
            lcs_list.append(lcs)
            acc_list.append(acc)
            #print("-")
            
            print("Step: {}, LCS = {}".format(n,lcs))
        n+=1
    return G_model,n_list, lcs_list,acc_list
#%% TESTING: ADD MESSAGES
stepsize = 100
V = sum(list(degree_dict.values()))/2
print("TOTAL NUMBER OF MESSAGES: {}".format(V))

print("RUNNING TEST RUN")
s = time.time()
G_model = Config_Network(degree_dict,nx.Graph())
G_model,n_list, lcs_list, acc_list = addMessages(G_model,stepsize,V)
e = time.time()
print("TIME: {:.2g} s".format(e-s))
print("DONE")
print("---")

#Largest component size
n = len(n_list) #Number of items in n_list
lcs_sum = np.zeros(n)  #Sum
lcs_SS = np.zeros(n) #Sum of Squares
lcs_av = np.zeros(n) #Av
lcs_unc = np.zeros(n) #Uncertainty

#Average clustering coefficient
acc_sum = np.zeros(n)  #Sum
acc_SS = np.zeros(n) #Sum of Squares
acc_av = np.zeros(n) #Av
acc_unc = np.zeros(n) #Uncertainty

for i in range(iterations):
    print("ITERATION: {} ADDING EDGES".format(i+1))
    s = time.time()
    G_model = Config_Network(degree_dict,nx.Graph())
    
    #Increase number of edges
    G_model,n_list, lcs_list, acc_list = addMessages(G_model,stepsize,V)
    edges_added = len(list(G_model.G.edges()))
    print('POSTS ADDED:{}'.format(edges_added))
    
    #print("ITERATION: {} REMOVING EDGES".format(i+1))
    #G_model,n_list_r, lcs_list_r, acc_list_r = removeMessages(G_model,stepsize,0)
    #edges_removed = edges_added-len(G_model.G.edges)
    #print('POSTS REMOVED:{}'.format(edges_removed))
    
    #Add results for removal to end of lists
    #n_list.extend(n_list_r)
    #lcs_list.extend(lcs_list_r)
    #acc_list.extend(acc_list_r)
    
    #Calculate averages and errors on LCS and ACC as a fct of time
    lcs_sum = lcs_sum+np.asarray(lcs_list)
    lcs_SS = lcs_SS+np.asarray(lcs_list)**2
    acc_sum = acc_sum+np.asarray(acc_list)
    acc_SS = acc_SS+np.asarray(acc_list)**2
    
    e = time.time()
    print("TIME: {:.2g} s".format(e-s))
#%%
#CALCULATE AVERAGES AND UNCERTAINTIES
lcs_av = lcs_sum*1/iterations
lcs_unc = np.sqrt(lcs_SS/iterations-lcs_av**2)
acc_av = acc_sum*1/iterations
acc_unc = np.sqrt(acc_SS/iterations-acc_av**2)
#%%
import datetime
datestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
f.write('EDGES={}, ITERATIONS={},DATE={}'.format(V,iterations,datestamp))
f.write('Number of edges,Largest component size,LCS uncertainty,Average Clustering Coefficient,ACC uncertainty\n')
for i in range(len(n_list)):
    f.write('{},{},{},{},{}\n'.format(n_list[i],lcs_av[i],lcs_unc[i],acc_av[i],acc_unc[i]))
f.close()
#%%
def plot(label,n_list,l_av,l_unc,V,N,c):
    '''Plot results for the addition and removal of edges on the network
    label: str
        Name of quantity represented
    n_list: list
        Number of edges in the network at each point of calculation
    l_av: list
        Averages
    l_unc: list
        Uncertainties
    V: Total number of edges
    N: Number of nodes
    c: Point in the list of calculated edges at which the removal begins
    '''
    fig = plt.figure()
    ax2 = fig.add_subplot(211)
    ax2.set_title("Configurational Model: V={} {}".format(V,label))
    ax2.set_xlabel("Wall posts, m")
    ax2.set_ylabel("{}".format(label))
    ax2.errorbar(n_list[:-c+1],l_av[:-c+1],l_unc[:-c+1],label="Adding nodes")
    ax2.errorbar(n_list[-c:],l_av[-c:],l_unc[-c:],label="Removing nodes")
    ax2.legend()
    ax3 = fig.add_subplot(212)
    ax3.set_title("Configurational Model: V={} {} Standard Deviation".format(V,label))
    ax3.set_xlabel("Wall posts, m")
    ax3.set_ylabel(r"$\sigma$ LCS")
    ax3.plot(n_list,l_unc)
    fig.tight_layout()
    fig.show()