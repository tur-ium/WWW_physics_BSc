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

#%% Load Erdos-Renyi model
from erdos_renyi import Erdos_Renyi

#PARAMETERS
#RUN
iterations = 10
stepsize = 1000

#NETWORK (DON'T CHANGE)
V = 66626   #Total number of wall posts made DEC 2008
N = 23396   #Number of active users DEC 2008

saveFile = 'empirical/Results/erdos-renyi_ResultsV={}N={}.csv'.format(V,N)
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
from measure import plot_distribution, getDegreeDist, computeLCS, computeClusteringCoefficient

lcs_av = list()
lcs_std = list()

def addMessages(G_model,step,V):
    '''Expand network `G_model` up to a volume V.'''    
    n_list = list()
    lcs_list = list()  #Largest component
    acc_list = list()  #Average clustering coefficient
    
    n = 0
    while n < V:
        G_model.iterate()
        
        #n = len(list(G_model.G.edges()))
        if n % step == 0:
            n_list.append(n)
            lcs = computeLCS(G_model.G)   #Largest component size
            acc,lccs = computeClusteringCoefficient(G_model.G)   #Calculate average clustering coefficient and local clustering coefficients
            lcs_list.append(lcs)
            acc_list.append(acc)
            #print("-")
            
            print("Step: {}, LCS = {}".format(n,lcs))
        n+=1
    return G_model,n_list, lcs_list,acc_list

import random
def removeMessages(G_model,step,Vmin):
    '''Expand network `G_model` down to a volume V.'''    
    n_list = list()
    lcs_list = list()  #Largest component
    acc_list = list()  #Average clustering coefficient
    
    n = len(list(G_model.G.edges()))

    while n > Vmin:
        edge = random.choice(list(G_model.G.edges()))
        from_node = edge[0]
        to_node = edge[1]
        G_model.G.remove_edge(from_node,to_node)
        
        n = len(list(G_model.G.edges()))
        if n % step == 0:
            n_list.append(n)
            lcs = computeLCS(G_model.G)   #Largest component size
            acc,lccs = computeClusteringCoefficient(G_model.G)   #Calculate average clustering coefficient and local clustering coefficients
            lcs_list.append(lcs)
            acc_list.append(acc)            
            print("Step: {}, LCS = {}".format(n,lcs))
    return G_model, n_list, lcs_list,acc_list

#%% Perform the equivalent of a thermodynamic cycle on the network
import time
import numpy as np
import matplotlib.pyplot as plt

#Test run
print("RUNNING TEST RUN")
s = time.time()
G_model = Erdos_Renyi(node_list)
G_model,n_list, lcs_list, acc_list = addMessages(G_model,stepsize,V)
e = time.time()
print("TIME: {:.2g} s".format(e-s))
print("DONE")
print("---")

#Largest component size
n = 2*len(n_list) #Number of items in n_list
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
    G_model = Erdos_Renyi(node_list)
    #Increase number of edges
    G_model,n_list, lcs_list, acc_list = addMessages(G_model,stepsize,V)
    edges_added = len(list(G_model.G.edges()))
    print('POSTS ADDED:{}'.format(edges_added))
    
    print("ITERATION: {} REMOVING EDGES".format(i+1))
    G_model,n_list_r, lcs_list_r, acc_list_r = removeMessages(G_model,stepsize,0)
    edges_removed = edges_added-len(G_model.G.edges)
    print('POSTS REMOVED:{}'.format(edges_removed))
    
    #Add results for removal to end of lists
    n_list.extend(n_list_r)
    lcs_list.extend(lcs_list_r)
    acc_list.extend(acc_list_r)
    
    #Calculate averages and errors on LCS and ACC as a fct of time
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
##%% SAVE RESULTS TO FILE
#
#datestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
#f.write('EDGES={}, ITERATIONS={},DATE={}'.format(V,iterations,datestamp))
#f.write('Number of edges,Largest component size,LCS uncertainty,Average Clustering Coefficient,ACC uncertainty\n')
#for i in range(len(n_list)):
#    f.write('{},{},{},{},{}\n'.format(n_list[i],lcs_av[i],lcs_unc[i],acc_av[i],acc_unc[i]))
#f.close()
#
##%%LOAD DATA
#dataPath = 'empirical/Results/erdos-renyi_ResultsV=1000N=333.csv'
#try:
#    f = open(dataPath,'r')
#except IOError:
#    print("Could not open file")
#
#rawData = open(dataPath).read().splitlines()
#unformattedData = []
#headers = rawData.pop(0)
#n_list = []
#lcs_list = []
#lcs_unc = []
#for line in rawData:
#    l = [float(i) for i in line.split(',')]
#    n_list.append(l[0])
#    lcs_list.append(l[1])
#    lcs_unc.append(l[2])
#
    
#%%PLOT

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
    ax2.set_title("Erdos-Renyi: V={} {}".format(V,label))
    ax2.set_xlabel("Wall posts, m")
    ax2.set_ylabel("{}".format(label))
    print(l_av)
    ax2.errorbar(n_list[:-c+1],l_av[:-c+1],l_unc[:-c+1],label="Adding nodes")
    ax2.errorbar(n_list[-c:],l_av[-c:],l_unc[-c:],label="Removing nodes")
    ax2.legend()
    ax3 = fig.add_subplot(212)
    ax3.set_title("Erdos-Renyi: V={} {} Standard Deviation".format(V,label))
    ax3.set_xlabel("Wall posts, m")
    ax3.set_ylabel(r"$\sigma$ LCS")
    ax3.plot(n_list,l_unc)
    fig.tight_layout()
    fig.show()
#n_list, lcs_list, acc_list = removeMessages(G_model,10,0)

c = len(lcs_list_r)  #Point in the list of calculated edges at which to stop
plot('Largest Component Size',n_list,lcs_av,lcs_unc,V,N,c)

fig2 = plt.figure()
ax2 = fig2.add_subplot(211)
ax2.set_title("Erdos-Renyi: V={} Average Clustering Coefficient".format(V))
ax2.set_xlabel("Wall posts, m")
ax2.set_ylabel("acc")
ax2.errorbar(n_list[:-c+1],acc_av[:-c+1],acc_unc[:-c+1],label="Adding nodes")
ax2.errorbar(n_list[-c:],acc_av[-c:],acc_unc[-c:],label="Removing nodes")
ax2.legend()

ax3 = fig2.add_subplot(212)
ax3.set_title("Erdos-Renyi: V={} ACC Standard Deviation".format(V))
ax3.set_xlabel("Wall posts, m")
ax3.set_ylabel(r"$\sigma$ acc")
ax3.plot(n_list,acc_unc)
fig2.tight_layout()
fig2.show()