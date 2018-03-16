# -*- coding: utf-8 -*-
"""
Created on Thu Mar  1 15:05:20 2018

@author: admin
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Feb 23 16:30:26 2018

@author: admin
"""
import datetime
import networkx_extended as nx
#%% Load Erdos-Renyi model
from erdos_renyi import Erdos_Renyi

#PARAMETERS
#RUN
iterations = 5
stepsize = 100

#NETWORK (DON'T CHANGE)
V = 66626   #Total number of wall posts made DEC 2008
N = 23396   #Number of active users DEC 2008

timestamp = datetime.datetime.now().strftime("%Y-%m-%d--%H-%M")
saveFile = 'incoming_results/erdos-renyi_ResultsV={}N={}I={}_{}.csv'.format(V,N,iterations,timestamp)

node_list = list(range(N))   #List of labels for each node

print("Volume of network (number of Facebook wall posts): {}".format(V))
print("Number of users: {}".format(N))

#%% PREPARE FOR WRITING DATA

try:
    f = open(saveFile,'w')
except IOError:
    print("Problem opening file,adding a number to the end")
    f= open(saveFile+'1','w')

#%% Erdos-Renyi Model
from measure_new import plot_distribution, getDegreeDist, computeLCS, computeClusteringCoefficient

lcs_av = list()
lcs_std = list()

def addMessages(G_model,step,V,verbose=False):
    '''Expand network `G_model` up to a volume V. V=Number of messages send = sum of weights on each node'''    
    t_list = list()
    lcs_list = list()  #Largest component
    acc_list = list()  #Average clustering coefficient
    
    n = 0  #Number of messages added
    while n < V:
        G_model.iterate()
        
        #n = len(list(G_model.G.edges()))
        if n % step == 0:
            t_list.append(n)
            lcs = computeLCS(G_model.G)   #Largest component size
            acc,lccs = computeClusteringCoefficient(G_model.G)   #Calculate average clustering coefficient and local clustering coefficients
            lcs_list.append(lcs)
            acc_list.append(acc)
            #print("-")
            if verbose==True:
                print("Step: {}, LCS = {}, ACC = {:.3g}".format(n,lcs,acc))
            
        n+=1
    return G_model,t_list, lcs_list,acc_list
def takeMeasurement(network,verbose):
    '''Returns
    ---
    lcs, acc
    '''
    lcs = computeLCS(network)   #Largest component size
    acc = nx.average_clustering(network)   #Calculate average clustering coefficient
    return lcs, acc
import random
def removeMessages(G_model,step,Vmin,verbose=False):
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
    m_list = list()
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

#%% Perform the equivalent of a thermodynamic cycle on the network
import time
import numpy as np
import matplotlib.pyplot as plt

for i in range(iterations):
    print("ITERATION: {} ADDING EDGES".format(i+1))
    s = time.time()
    G_model = Erdos_Renyi(node_list)
    #Increase number of edges
    G_model,t_list, lcs_list, acc_list = addMessages(G_model,stepsize,V,verbose=False)
    edges_added = len(list(G_model.G.edges()))
    print('POSTS ADDED:{}'.format(edges_added))
    
    print("ITERATION: {} REMOVING EDGES".format(i+1))
    G_model,m_list_r, lcs_list_r, acc_list_r = removeMessages(G_model,stepsize,0,verbose=False)
    edges_removed = edges_added-len(G_model.G.edges)
    print('POSTS REMOVED:{}'.format(edges_removed))
    
    edgesAdded = len(lcs_list)  #Number of edges added
    
    #Add results for removal to end of lists
    t_list.extend(m_list_r)
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
    
#%% CALCULATE AVERAGES AND UNCERTAINTIES
lcs_av = lcs_sum*1/iterations
lcs_unc = np.sqrt(lcs_SS/iterations-lcs_av**2)
acc_av = acc_sum*1/iterations
acc_unc = np.sqrt(acc_SS/iterations-acc_av**2)
#print('max lcs unc: {}\nmax acc unc: {}'.format(max(lcs_unc),max(acc_unc)))
#%% SAVE RESULTS TO FILE

datestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
f.write('EDGES={}, ITERATIONS={},DATE={}'.format(V,iterations,datestamp))
f.write('Number of edges,Largest component size,LCS uncertainty,Average Clustering Coefficient,ACC uncertainty\n')
for i in range(len(t_list)):
    f.write('{},{},{},{},{}\n'.format(t_list[i],lcs_av[i],lcs_unc[i],acc_av[i],acc_unc[i]))
f.close()

#%%LOAD DATA
#dataPath = 'empirical/Results/erdos-renyi_ResultsV=1000N=333.csv'
#try:
#    f = open(dataPath,'r')
#except IOError:
#    print("Could not open file")
#
#rawData = open(dataPath).read().splitlines()
#unformattedData = []
#headers = rawData.pop(0)
#t_list = []
#lcs_list = []
#lcs_unc = []
#for line in rawData:
#    l = [float(i) for i in line.split(',')]
#    t_list.append(l[0])
#    lcs_list.append(l[1])
#    lcs_unc.append(l[2])
#

##%% PLOT DATA
#def plot(label,n_list,l_av,l_unc,V,N,stepsize,iterations,c):
#    '''Plot results for the addition and removal of edges on the network
#    label: str
#        Name of quantity represented
#    n_list: list
#        Number of edges in the network at each point of calculation
#    l_av: list
#        Averages
#    l_unc: list
#            Uncertainties
#    V: Total number of edges
#    N: Number of nodes
#    stepsize: Step size
#    iterations: Iterations
#    c: Point in the list of calculated edges at which the removal begins
#    '''
#    
#    fig = plt.figure()
#    ax2 = fig.add_subplot(211)
#    ax2.set_title("Erdos-Renyi Model: V={}, N={}, s={}, I={} {}".format(V,N,stepsize,iterations,label))
#    ax2.set_xlabel("Wall posts, m")
#    ax2.set_ylabel("{}".format(label))
#    ax2.errorbar(n_list[:-c+1],l_av[:-c+1],l_unc[:-c+1],label="Adding nodes")
#    ax2.errorbar(n_list[-c:],l_av[-c:],l_unc[-c:],label="Removing nodes")
#    ax2.legend()
#    ax3 = fig.add_subplot(212)
#    ax3.set_title("Erdos-Renyi Model: V={}, N={}, s={}, I={} {} s.d.".format(V,N,stepsize,iterations,label))
#    ax3.set_xlabel("Wall posts, m")
#    ax3.set_ylabel(r"$\sigma$ LCS")
#    ax3.plot(n_list[:-c+1],l_unc[:-c+1],label="Adding nodes")
#    ax3.plot(n_list[-c:],l_unc[-c:],label="Removing nodes")
#    ax3.set_xlim(left=0,right=max(n_list))
#    ax3.legend()
#    fig.tight_layout()
#    fig.show()

import AR_cycle
AR_cycle.plot('LCS',t_list,lcs_av,lcs_unc,V,N,stepsize,iterations,edgesAdded,model_name=r"ERDŐS-RÉNYI")
AR_cycle.plot('ACC',t_list,acc_av,acc_unc,V,N,stepsize,iterations,edgesAdded,model_name=r"ERDŐS-RÉNYI")

