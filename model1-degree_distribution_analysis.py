# -*- coding: utf-8 -*-
"""
Created on Fri Jan 26 15:44:44 2018

@author: admin
"""

import clustering_toolkit as ctk
import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
import time

def plot_distribution(d,name,n=1000):
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
#    log_max_degree = np.log10(max(d.values()))
    n=len(d)
    bin_edges = np.linspace(0,max(d.values()),n-1)
    bin_edges = list(bin_edges)
    bin_edges.insert(0,0.)
    #print(bin_edges)
    
    #TODO: Loop through and create a dictionary {degree: frequency}
    
    plt.figure()
    start = time.time()
    degree_dist,bins = np.histogram(list(d.values()),bins=bin_edges)
    end = time.time()
    print('Time to perform histogramming: {} s'.format(end-start))
    bin_centres = [sum(bin_edges[i:i+1]) for i in range(0,len(bin_edges)-1)]
    plt.loglog(bin_centres,degree_dist,'+')
    plt.xlim(1,1e4)
    plt.grid()
    plt.title('{} distribution'.format(name.capitalize()))
    plt.xlabel('log({})'.format(name))
    plt.ylabel('log(Frequency)')
    
#    plt.figure()
#    degree_dist,degrees,patches = plt.hist(d.values(),bins=bin_edges,cumulative=True)
#    plt.title('Cumulative {} distribution'.format(name))
#    plt.xlabel(name)
#    plt.ylabel('Cumulative frequency')
    
startTime = time.time()

activityNetworkFile = "Data/activity_network_multidigraph.gexf"
socialNetworkFile = "Data/social_network.gexf"

#isNetworksLoaded = False
if not isNetworksLoaded:
    G_A = ctk.loadNetworkFromFilePath(activityNetworkFile)
    G_S = ctk.loadNetworkFromFilePath(socialNetworkFile)
    isNetworksLoaded = True

timeToLoadNetworksGEXF = time.time()-startTime
print("Network loaded in {}s".format(timeToLoadNetworksGEXF))

people = list(G_A.nodes())

degree_dict = dict(nx.degree(G_A))   #Total # of posts sent AND received (undirected) as a dict
in_degree_dict = dict(G_A.in_degree())   #Total # of posts received
out_degree_dict = dict(G_A.out_degree())   #Total # of posts sent


#%%
#VALIDATION
#Check first few degrees
print(list(G_A.degree())[:10])
print([degree_dict[i] for i in people[:10]])

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
#plot_distribution(degree_dict,'degree')
#plot_distribution(in_degree_dict,'in degree')
#plot_distribution(out_degree_dict,'out degree')

#%%
#Check if the network is scale-free
#If you get a Divide By Zero Runtime Error: see https://github.com/jeffalstott/powerlaw/issues/28
# "That "error" is being caused by the fitting process trying to find a fit for 
# the power law function to your data. As it explores many different fits, some 
# will be beyond numerical accuracy, yielding divide by zero errors."

import powerlaw   #Can be installed by doing pip install powerlaw

degree_vals = list(degree_dict.values())
fit_activity = powerlaw.Fit(degree_vals,discrete=True)
print('\n')
print('COMPARING LIKELIHOODS OF TRUNCATED POWER LAW VS. LOGNORMAL FITS')
print('ACTIVITY NETWORK:')
R,p = fit_activity.distribution_compare('truncated_power_law','lognormal')

#If ratio of likelihoods is positive and larger than the threshold 0.1 
if R > 0 and p>0.1:
    print('Probably a truncated power law fit: exponent, α = {:.3g}, lambda = {:.3g}, prob vs. lognormal={:.3g}'.format(fit_activity.truncated_power_law.parameter1,fit_activity.truncated_power_law.parameter2, p))
else:
    print('Probably a lognormal fit: mean = {}, stdev = {}, p = {}'.format(fit_activity.lognormal.mu,fit_activity.lognormal.sigma,p))
fig1 = plt.figure()
ax1 = fig1.add_subplot(111)
fit_activity.truncated_power_law.plot_pdf(ax=ax1)
fit_activity.plot_pdf(original_data=True,ax=ax1)
ax1.set_xlabel('Degree')
ax1.set_ylabel('Probability')
ax1.set_title('Activity degree distribution vs. truncated power law fit')
fig1.savefig('activity_degree_dist_w_truncated_power_law.png')

#Check scale-free for the social network
print('\n')
print('SOCIAL NETWORK')
fit_social = powerlaw.Fit(list(dict(G_S.degree).values()))
R, p = fit_social.distribution_compare('truncated_power_law','lognormal')

if R > 0 and p>0.1:
    print('Probably a truncated power law fit: exponent, α = {:.3g}, lambda = {:.3g}, prob vs. lognormal={:.3g}'.format(fit_social.truncated_power_law.parameter1,fit_social.truncated_power_law.parameter2, p))
else:
    print('Probably a lognormal fit: mean = {}, stdev = {}, p = {}'.format(fit_social.lognormal.mu,fit_social.lognormal.sigma,p))#

fig1 = plt.figure()
ax1 = fig1.add_subplot(111)
fit_social.power_law.plot_pdf(ax=ax1,color='green')
#fit_social.plot_pdf(data=list(dict(G_S.degree).values()),ax=ax1,color='red')
fit_social.plot_pdf(original_data=False,ax=ax1,color='black')
ax1.set_xlabel('Degree')
ax1.set_ylabel('Probability')
ax1.set_title('Social degree distribution vs. truncated power law fit')
fig1.savefig('social_degree_dist_w_truncated_power_law.png')