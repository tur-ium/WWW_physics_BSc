# -*- coding: utf-8 -*-
"""
Created on Fri Mar  9 18:39:06 2018

@author: admin
"""
import empirical.Timeslice as ts

from matplotlib import pyplot as plt
#PLOT FORMATTING
font= {'family': 'Arial',
        'weight': 'bold',
        'size': 14}
plt.rc('font',**font)
plt.rcParams.update({'axes.titlesize':'large',
                     'axes.labelsize': 'large'})
#PARAMETERS
edgeListFilePath = '../Data/activity_network_edge_list.txt'

#%%
#PARAMETERS
dataLoaded = False   #Comment this out if rerunning the code in interactive shell to save time

YEAR = '2008'
MONTH = 'DEC'
ENDYEAR = '2009'   
ENDMONTH = 'JAN' #End at the BEGINNING of this month

beginTime = ts.TIME_DICT[YEAR][MONTH]  #NOTE Time at beginning of month
endTime = ts.TIME_DICT[ENDYEAR][ENDMONTH] #NOTE Time at beginning of month

#%%
#LOAD WEIGHT NETWORK TIMESLICE
#Undirected network of wall posts sent within DEC 2008
#Nodes: users
#Edges: wall posts (undirected)
#Weights: number of wall posts in timeslice
loadedGraph = ts.loadGEXF("../Data/WeightedNetwork/{}_{}_WeightedGraph.gexf".format(YEAR,MONTH))

#%%
label="Number of users"
N = len(loadedGraph.nodes())
print(label,N)
#%%
label="Number of self-loops (wall posts on own wall)"
def number_of_self_loops(G):
    self_edges = 0
    n = 0
    for edge in G.edges():
        s = edge[0]
        t = edge[1]
        n+=1
        if s == t:
            self_edges+=1
     #       print("SELF-EDGE")
    #print("{} edges checked".format(n))
    return self_edges
self_edges=number_of_self_loops(loadedGraph)
print(label,self_edges)
#%%
label="Number of pairs of users who interacted"
edges = len(loadedGraph.edges())
interactions = edges-self_edges
print(label,interactions)
#%% MESSAGES
#%%
label="Total number of wall posts sent"
#Number of messages sent by each user = weighted degree of each node
node_weights = dict(loadedGraph.degree(weight='weight'))
V = .5*sum(node_weights.values())
print(label,V)
#%%
label="Average number of wall posts per user in December"
m = V/len(node_weights)
print('{}: {:.3g}'.format(label,m))#

#%% EVOLUTION OVER TIME
#%%
#Load timestamped data
import networkx_extended as nx
dataLoaded = False
if not dataLoaded:
    #READ ORIGINAL EDGE_LIST FOR WHOLE NETWORK
    edgeList = ts.readEdgelistFromPath(edgeListFilePath,isWeighted=True)
    
    #TAKE THE TIMESLICE FOR THE DESIRED MONTH
    #format 1: ((source,target),timestamp)
    edgeListSlice_format1 = ts.timeSliceEdges(edgeList,beginTime,endTime,retainWeights=True)
    
    #CHANGE FORMAT FOR NETWORKX
    edgeListSlice = list()   #(source,target,timestamp)
    
    for edge in edgeListSlice_format1:
        edgeListSlice.append((edge[0][0],edge[0][1],int(edge[1])))
    
    #Create a nx Graph object
    G_A = nx.MultiDiGraph()
#    dataPath = 'empirical/Data/TimeSlicedDataNew/TimeSlicedData/'
#    G_A = ts.loadGEXF("{}/GEXF/{}/{}_{}_MultiDiGraph.gexf".format(dataPath,YEAR, YEAR, MONTH))
    G_A.add_weighted_edges_from(edgeListSlice)
    dataLoaded = True  
#%%

label = "Number of coincident interactions occurred (same second)"
def convertMultiDiGraphToChronology(multiDiGraph):
    '''Converts graph object into a dictionary with UNIX timesteamps as keys'''
    chronology = dict()
    e = 0
    for edge in multiDiGraph.edges(data='weight'):
        timestamp = edge[2]
        s = edge[0]
        t = edge[1]
        if timestamp not in chronology.keys():
            chronology[timestamp] = list()
        chronology[timestamp].append((s,t))
        e+=1
    return chronology

#Dictionary {UNIX time 1: ((s,t),(s,t),...), ...}
chronology = convertMultiDiGraphToChronology(G_A)

print(label,int(V-len(chronology)))

label = "Frequency of interactions across whole network {} {}".format(YEAR, MONTH)
interactions_per_sec = dict()
interaction_times = list()
for sec in chronology:
    m = len(chronology[sec])
    for n in range(m):
        interaction_times.append(sec)
    #print(chronology[sec])
    interactions_per_sec[sec] = len(chronology[sec])
#%%
label="Frequency of Interaction {} {}".format(MONTH, YEAR)

plt.figure(figsize=(10,5))
plt.title(label)
#plt.xlabel('Day of the month')
plt.ylabel('Interaction count')

labels = range(1,31*24)

TIME_ARRAY = list()


xTicks = list(range(1,31*24+1)) # Days of the month
hist, bin_edges, patches = plt.hist(interaction_times,bins=31*24)

plt.xticks(bin_edges[:-1], xTicks)
plt.xlim(xmax=bin_edges[24])
print("DONE")

label="Frequency of Interaction {} {}".format(MONTH, YEAR)

#%%
import numpy as np #For histogramming and averaging

label="Hourly interaction over a day"
#Do people use Facebook at work?
plt.figure(figsize=(10,5))
plt.title(label)
#plt.xlabel('Day of the month')
plt.ylabel('Interaction count')

#Average number of interactions per hour
#AVERAGE OVER ALL DAYS
sublabel="Average over all days"
#hourly_interactions_sum[day] = sum number of interactions in day of the week
hourly_interactions_sum = np.ndarray(24)
#hist_hour[i] = number of messages in the ith hour of the month
hist_hour, hour_bin_edges = np.histogram(interaction_times,bins=31*24)

#SIMPLE AVERAGE OVER ALL DAYS IN MONTH
n=0
MONDAY = 1
days = 31

#Day 1 = MONDAY
for count in hist_hour:
    n+=1
    day = n % 7
    hourly_interactions_sum[day] += count
hourly_interactions_av = hourly_interactions_sum/days
#TODO: VERIFY
#TODO: PLOT

#TIME_ARRAY = list()
#
#
#xTicks = list(range(1,31*24+1)) # Days of the month
#hist, bin_edges, patches = plt.hist(interaction_times,bins=31*24)
#
#plt.xticks(bin_edges[:-1], xTicks)
#plt.xlim(xmax=bin_edges[24])
print("DONE")

#%%
label = "Largest Component Size"
from measure_new import computeLCS
lcs = computeLCS(loadedGraph)
print("{} {:.3g}".format(label, lcs))
#%%
label = "Average Clustering Coefficient"
acc = nx.average_clustering(loadedGraph)
print("{} {:.3g}".format(label, acc))