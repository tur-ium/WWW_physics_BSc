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
import matplotlib.pyplot as plt
import numpy as np
from scipy import optimize


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

#FUNCTION DEFINITIONS
#V = len(list(G_A.edges())) #Desired volume of the network
Vmax = 500000

def calcDelta(network, V=Vmax,mstep=1000):
    '''
        V: in
            Maxm number of edges to add
        mstep:
            Number of edges to add between calculations of maxm component size
        network: nx.Graph / nx.DiGraph / nx.MultiDiGraph 
            Network to draw nodes from
        '''
    N = len(network.nodes())
    node_list = list(network.nodes())
    print('Network size: {}'.format(N))
    '''Calculate Delta from paper ["Explosive Percolation in Random Networks"]'''
    threshold1 = int(N**.5)
    threshold2 = int(.5*N)
    print('Threshold 1: {}'.format(threshold1))
    print('Threshold 2: {}'.format(threshold2))
    
    model1_ccs = list()   #Log of clustering coefficients over time
    model1_ncs = list()   #Log of number of connected components over time
    model1_acs = list()   #Log of average components sizes
    
    #ADD EDGES
    m = 0   #Number of edges added
    t0 = 0   #Time to reach threshold 1
    t1 = 0   #Time to reach threshold 2
    while m < V:
        #A user sends a message to any other user in the network with equal probability
        from_user = random.choice(node_list)
        to_user = random.choice(node_list)
        network.add_edge(from_user,to_user)
        m+=1
        if m % mstep == 0:
            print('m: {}'.format(m))
            #print('ORDER PARAMETER CANDIDATES:')
            
            #Number of SCCs, Av. SCC size
            SCCs = list(nx.strongly_connected_components(network))   #Strongly Connected Components at time n

            sum_comp_size = 0
            n_comp = 0
            for SCC in SCCs:
                sum_comp_size+=len(SCC)
                n_comp+=1
            av_comp_size=sum_comp_size/N
            model1_ncs.append(n_comp)
            model1_acs.append(av_comp_size)
            
            #Size of maxm component
            C = len(max(SCCs,key=len))
            
            if C > threshold1 and t0 == 0:
                #Past threshold 1 for the first time
                t0 = m - 1
                print("PAST THRESHOLD 1, m={}".format(m))
            if C > threshold2 and t0 > 0:
                #Past threshold 1 and threshold 2 for the first time
                t1 = m
                print("PAST THRESHOLD 2, m={}".format(m))
                break
            
            #PRINT STATS
            print("Largest component size: {}".format(C))
            #print('Number of strongly-connected components: {}'.format(N))
            #print('Av. size of strongly-connected components: {}'.format(av_comp_size))
    
    #        model1_c_d, model1_c = ctk.calculateClusteringCoeffPerNode(network)
    #        av_c = sum(model1_c)/len(model1_c)
    #        model1_ccs.append(av_c)
    print('FINISHED N={}'.format(N))
    if t0 == 0:
        print("WARNING: Didn't reach C>N**0.5 with V={}".format(V))
    if t1 == 0:
        print("WARNING: Didn't reach C>0.5*N with V={}".format(V))
    return t1-t0


#REMOVE NODES
#while n > 0:
#    #Pick a message at random, and erase it from the social network history
#    edge_to_remove = random.randint(0,n-1)
#    from_user = list(network.edges)[edge_to_remove][0]
#    to_user = list(network.edges)[edge_to_remove][1]
#    network.remove_edge(from_user,to_user)
#    
#    n-=1
#    if n % 100 == 0:
#        print('Calculating coefficients. Number of messages: {}'.format(n))
#        print('ORDER PARAMETER CANDIDATES:')
#        #Number of SCCs, Av. SCC size
#        SCCs = list(nx.strongly_connected_components(network))   #Strongly Connected Components at time n
#        
#        C = len(max(SCCs,key=len))   #Size of largest component
#        
#        print("Largest component size is: {}".format(C))
#        sum_comp_size = 0
#        N = 0
#        for SCC in SCCs:
#            sum_comp_size+=len(SCC)
#            N+=1
#        av_comp_size=sum_comp_size/N
#        model1_ncs.append(N)
#        model1_acs.append(av_comp_size)
#        print('Number of strongly-connected components: {}'.format(N))
#        print('Av. size of strongly-connected components: {}'.format(av_comp_size))
#
#print('FINISHED REMOVING NODES')

##PLOT
#fig = plt.figure()
#ax1 = fig.add_subplot(211)
#ax2 = fig.add_subplot(212)
#ax1.plot(range(len(model1_ncs)),model1_ncs,label='Number of components')
#ax2.plot(range(len(model1_acs)),model1_acs,label='Average component size')
#ax1.set_xlabel('x100 wall posts')
#ax2.set_xlabel('x100 wall posts')
#ax1.set_ylabel('Number of components')
#ax2.set_ylabel('Average component size')

#%%
def test_phase_transition_type(Nlist,Vmax=500000,mstep=1000):
    #Is the phase transition first order?
    delta_list= list()
    for N in Nlist:
        print("test_phase_transition_type says: current N={}".format(N))
        node_list = list(range(N))   #Create an imaginary network
        network = nx.MultiDiGraph()
        network.add_nodes_from(node_list)
    
        #nodes_list = list(G_A.nodes())[:N]   #Take only a subset of 10000 nodes from the activity network
        #network = nx.MultiDiGraph()
        #network.add_nodes_from(nodes_list)
        delta = calcDelta(network,mstep=mstep)
        delta_list.append(delta)
        N += 10000

    #PLOT DATA
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(N_list,delta_list,'b-',label='Results')

    #FIT CURVE
    print('FITTING')
    def linear(x,a,b):
        return a*x+b
    
    #LINEAR
    lopt, lcov = optimize.curve_fit(linear,N_list,delta_list)
    l_a, l_b = lopt[0],lopt[1]   #Values of fit
    
    #ERRORS
    a_err = lcov[0,0]**.5
    b_err = lcov[1,1]**.5
    print('Fit params for ax+b: a={:.3g}±{:.3g}, b={:.3g}±{:.3g}'.format(l_a,a_err,l_b,b_err))
    ax.plot(N_list,linear(np.asarray(N_list),l_a,l_b),'g--',label='Linear fit')
    ax.set_title('Delta vs. network size, N')
    ax.set_xlabel('N')
    ax.set_ylabel(u'Δ')
    plt.show()
#%%
N_list = list(map(int,np.arange(1000,10000,500)))   #Network sizes to try
test_phase_transition_type(N_list,500)