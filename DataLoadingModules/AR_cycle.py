# -*- coding: utf-8 -*-
"""
Created on Fri Mar  9 17:15:46 2018
UPDATED
@author: admin
"""
import empirical.Timeslice as ts
import matplotlib.pyplot as plt
import networkx_extended as nx
from measure_new import computeLCS
#%% 
def takeMeasurement(network,verbose):
    '''Returns
    ---
    lcs, acc
    '''
    lcs = computeLCS(network)   #Largest component size
    acc = nx.average_clustering(network)   #Calculate average clustering coefficient
    return lcs, acc

def plot(label,n_list,l_av,l_unc,V,N,stepsize,iterations,c,plotUncertainty=True,model_name=""):
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
    stepsize: Step size
    iterations: Iterations
    c: Point in the list of calculated edges at which the removal begins
    plotUncertainty: boolean
        If True plot uncertainty on separate axes
    modelName: str
        Name of the model
    '''
    
    fig = plt.figure()
    if plotUncertainty:
        layout = 211
    else:
        layout = 111
    
    ax2 = fig.add_subplot(layout)
    ax2.set_title("{}: V={}, N={}, s={}, I={} {}".format(model_name,V,N,stepsize,iterations,label))
    ax2.set_xlabel("Wall posts, m")
    ax2.set_ylabel("{}".format(label))
    ax2.plot(n_list[:-c+1],l_av[:-c+1],label="Adding messages")
    ax2.plot(n_list[-c:],l_av[-c:],label="Removing messages")
    ax2.set_xlim(left=0,right=max(n_list))
    ax2.legend()
    if plotUncertainty:
        ax3 = fig.add_subplot(212)
        ax3.set_title("{}: V={}, N={}, s={}, I={} {} s.d.".format(model_name,V,N,stepsize,iterations,label))
        ax3.set_xlabel("Wall posts, m")
        ax3.set_ylabel(r"{} standard deviation".format(label))
        ax3.plot(n_list[:-c+1],l_unc[:-c+1],label="Adding messages")
        ax3.plot(n_list[-c:],l_unc[-c:],label="Removing messages")
        ax3.set_xlim(left=0,right=max(n_list))
        ax3.legend()
    fig.tight_layout()
    fig.show()