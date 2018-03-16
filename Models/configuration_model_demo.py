# -*- coding: utf-8 -*-
"""
Created on Mon Mar  5 21:38:04 2018

@author: admin
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Feb 16 15:53:29 2018

@author: ad6315

#Generates LCS and ACC graphs for Configurational Model

#TODO: Plot results from 1/3/18
"""
#%%IMPORT MODULES
import random
import networkx as nx
import matplotlib.pyplot as plt
import pickle
from measure_new import plot_distribution, getDegreeDist, computeLCS, computeClusteringCoefficient
import empirical.Timeslice as ts
import numpy as np
import time
import datetime #For naming files

#%%PARAMETERS
stepsize = 100
iterations = 5  #Number of iterations used for averaging

#Timeslice to use for degree distribution

loadedGraph = ts.loadGEXF("C:/Users/admin/Documents/Physics/year 3/WWWPhysics-PC/empirical/Data/WeightedNetwork/2008_DEC_WeightedGraph.gexf")
N=23396   #Number of nodes to use from network


#%%Load empirical degree dict
degree_dict_original = getDegreeDist(loadedGraph)
node_list_original = list(degree_dict_original.keys())

#TESTING: Restrict degree dict to first 10000 nodes
#degree_dict = degree_dict_original
degree_dict = dict()
node_list = node_list_original[:N]
for node in node_list:
    degree_dict[node]=degree_dict_original[node]

V = sum(list(degree_dict.values()))/2

#%%Data path for saving
timestamp = datetime.datetime.now().strftime("%Y-%m-%d--%H-%M")
saveFile = 'incoming_results/config-model_ResultsV={}N={}I={}_{}.csv'.format(V,N,iterations,timestamp)

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
            
            if t == s:
                #Will/would add a self-loop
                self.self_loops+=1
                if self.allow_self_loops:
                    if not t in self.G[s].keys():
                        #Edge does not exist
                        self.G.add_edge(s,t)
                        self.G[s][t]['weight'] = 1
                    elif t in self.G[s].keys():
                        #Edge already exists
                        self.parallel_edges+=1
                        self.G[s][t]['weight'] += 1           
            else:
                #Edge not a self-loop
                if not t in self.G[s].keys():
                    #Edge does not exist and it is not a self-loop
                    self.G.add_edge(s,t)
                    self.G[s][t]['weight'] = 1
                elif t in self.G[s].keys():
                    #Edge already exists
                    self.parallel_edges+=1
                    self.G[s][t]['weight'] += 1
                
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


#%% PREPARE FOR WRITING DATA
try:
    f = open(saveFile,'w')
except IOError:
    exit("Problem opening file for writing")

#%%TESTING: TOY NETWORK

#G_model = Config_Network({0:1,1:2,2:1,3:1,4:1},nx.Graph())
#G_model.iterate()
#nx.draw_networkx(G_model.G)
#%% 
def takeMeasurement(network,verbose):
    '''Returns
    ---
    lcs, acc
    '''
    lcs = computeLCS(network)   #Largest component size
    acc = nx.average_clustering(network)   #Calculate average clustering coefficient
    return lcs, acc
def addMessages(G_model,step,V,verbose=True):
    '''Expand network `G_model` up to a volume V. \
If verbose=True (default: True) prints results at each calculation step 
    RETURNS
    ---
    G_model: nx Graph object
        The model network after adding edges
    t_list: list
        Times at which measurements were taken in terms of number of wall posts
    lcs_list: list
        List of largest component sizes at times in t_list
    acc_list: list
        List of average clustering coefficients at times in t_list
    '''    
    t_list = list()   #Time steps (number of messages added)
    lcs_list = list()  #Largest component
    acc_list = list()  #Average clustering coefficient
    
    stubsleft = len(G_model.stub_dict)
    n = 0   #Number of stubs joined (NOT THE NUMBER OF MESSAGES AS EDGES ARE WEIGHTED)
    while stubsleft > 0:
        G_model.iterate()
        stubsleft = len(G_model.stub_dict)
        
        if n % step == 0:
            #After adding n edges, take measurements of LCS and ACC
            t_list.append(n)
            network = G_model.G
            lcs,acc = takeMeasurement(network,verbose)  #Take measurement
            lcs_list.append(lcs)
            acc_list.append(acc)
            if verbose==True:
                print("Step: {}, LCS = {}, ACC = {:.3g}".format(n,lcs,acc))
        n+=1
    return G_model,t_list, lcs_list,acc_list

def removeMessages(G_model,step,Vmin=0,verbose=True):
    '''Remove messages until the network has a volume (number of wall posts) \
Vmin (default:0).If verbose=True (default: True) prints results at each calculation step 
    RETURNS
    ---
    G_model: nx Graph object
        The model network after adding edges
    m_list: list
        Points at which measurements were taken in terms of number of wall posts
    lcs_list: list
        List of largest component sizes at network sizes in m_list
    acc_list: list
        List of average clustering coefficients at network sizes in m_list
'''
    m_list = list()   #Number of messages in network
    lcs_list = list()  #Largest component
    acc_list = list()  #Average clustering coefficient
    
    edge_list = list(G_model.G.edges)
    message_list = list()   #List of [(s,t) ] for each wall post made
    for edge in edge_list:
        s = edge[0]   #Source node
        t = edge[1]   #Target node
        w = G_model.G[s][t]['weight']  #Number of messages sent between s and t
        if not isinstance(w,int):
            raise Exception('Number of wall posts between two users is not an int')
        for i in range(w):
            message_list.append((s,t))
    V = len(message_list)
    messagesToRemove = V-Vmin
    if messagesToRemove<=0:
        raise Exception("Vmin>=V")
    print('Messages to remove',messagesToRemove)
    random.shuffle(message_list)   #Randomly shuffle edge_list
    
    n = 0  #Number of edges removed
    while messagesToRemove > 0:
        edge = message_list.pop()  #Take the last element from the randomly shuffled edge-list
        s = edge[0]   #Source node
        t = edge[1]   #Target node
        w = G_model.G[s][t]['weight']  #Number of messages sent between s and t
        
        if w <= 1:
            G_model.G.remove_edge(s,t)
        elif w > 1:
            G_model.G[s][t]['weight']=w-1
        else:
            raise Exception("Unknown error due to strange weights on edges")
        messagesToRemove -= 1
        if n % step == 0:
            #After removing n edges take measurements of LCS and ACC
            m_list.append(V-n)   #Record number of messages still sent in this network
            network = G_model.G
            lcs,acc = takeMeasurement(network,verbose)  #Take measurement
            lcs_list.append(lcs)
            acc_list.append(acc)
            if verbose==True:
                print("Step: {}, LCS = {}, ACC = {:.3g}".format(n,lcs,acc))
        n+=1
    return G_model,m_list,lcs_list,acc_list

#%%

for i in range(iterations):
    print("ITERATION: {} ADDING EDGES".format(i+1))
    s = time.time()
    G_model = Config_Network(degree_dict,nx.Graph(),allow_self_loops=True)
    print('Number of wall posts: V={} = sum of degrees/2 = {} = length of stub_dict: {}'.format(V,sum(G_model.k_list)/2,len(G_model.stub_dict)/2))
    
    G_model,t_list,lcs_list,acc_list = addMessages(G_model,stepsize,V,verbose=False)
    print("ITERATION: {} REMOVING EDGES".format(i+1))
    G_model,m_list,lcs_list_r,acc_list_r = removeMessages(G_model,stepsize,0,verbose=False)

    edgesAdded = len(lcs_list)  #Number of edges added
    
#    Add results for removal to end of lists    
    t_list.extend(m_list)
    lcs_list.extend(lcs_list_r)
    acc_list.extend(acc_list_r)
    
    if i == 0:   #Create arrays
        print("Creating arrays")
        ndata = len(t_list)
        
        lcs_sum = np.zeros(ndata)  #Sum
        lcs_SS = np.zeros(ndata) #Sum of Squares
        lcs_av = np.zeros(ndata) #Av
        lcs_unc = np.zeros(ndata) #Uncertainty
        
        #Average clustering coefficient
        acc_sum = np.zeros(ndata)  #Sum
        acc_SS = np.zeros(ndata) #Sum of Squares
        acc_av = np.zeros(ndata) #Av
        acc_unc = np.zeros(ndata) #Uncertainty
    #Add results of iteration to sums and sums of squares 
    lcs_sum = lcs_sum+np.asarray(lcs_list)
    lcs_SS = lcs_SS+np.asarray(lcs_list)**2
    acc_sum = acc_sum+np.asarray(acc_list)
    acc_SS = acc_SS+np.asarray(acc_list)**2
    
    e = time.time()
    print("TIME: {:.2g} s".format(e-s))
    
#CALCULATE AVERAGES AND UNCERTAINTIES
lcs_av = lcs_sum*1/iterations
lcs_unc = np.sqrt(lcs_SS/iterations-lcs_av**2)
acc_av = acc_sum*1/iterations
acc_unc = np.sqrt(acc_SS/iterations-acc_av**2)
#%% SAVE DATA
import datetime
datestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
f.write('EDGES={}, ITERATIONS={},DATE={}\n'.format(V,iterations,datestamp))
f.write('Number of edges,Largest component size,LCS uncertainty,Average Clustering Coefficient,ACC uncertainty\n')
for i in range(len(t_list)):
    f.write('{},{},{},{},{}\n'.format(t_list[i],lcs_av[i],lcs_unc[i],acc_av[i],acc_unc[i]))
f.close()
#%% PLOT DATA

import AR_cycle
AR_cycle.plot('LCS',t_list,lcs_av,lcs_unc,V,N,stepsize,iterations,edgesAdded,model_name="CONFIGURATIONAL")
AR_cycle.plot('ACC',t_list,acc_av,acc_unc,V,N,stepsize,iterations,edgesAdded,model_name="CONFIGURATIONAL")