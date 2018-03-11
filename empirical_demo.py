# -*- coding: utf-8 -*-
"""
Created on Thu Mar  8 10:56:42 2018
ANALYSIS OF ACTIVITY NETWORK

@author: admin
"""
#%%
dataLoaded = False
#%%
import empirical.Timeslice as ts
import time
import networkx_extended as nx
from measure_new import computeLCS, getDegreeDist
from matplotlib import pyplot as plt
import random
import datetime

from AR_cycle import plot

#%% PARAMETERS
dataDirectory = "C:/Users/admin/Documents/Physics/year 3/WWWPhysics-PC/empirical/Data/TimeSlicedDataNew/TimeSlicedData"


YEAR = '2008'
MONTH = 'DEC'
ENDYEAR = '2009'   
ENDMONTH = 'JAN' #End at the BEGINNING of this month

beginTime = ts.TIME_DICT[YEAR][MONTH]  #NOTE Time at beginning of month
endTime = ts.TIME_DICT[ENDYEAR][ENDMONTH] #NOTE Time at beginning of month
#%% LOAD DATA

#weightedGraph = ts.loadGEXF("C:/Users/admin/Documents/Physics/year 3/WWWPhysics-PC/empirical/Data/WeightedNetwork/2008_DEC_WeightedGraph.gexf")

dataLoaded = False
if not dataLoaded:
    #READ ORIGINAL EDGE_LIST FOR WHOLE NETWORK
    edgeList = ts.readEdgelistFromPath('empirical/Data/activity_network_edge_list.txt',isWeighted=True)
    
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

node_list = list(G_A.nodes())
class Empirical:
    def __init__(self):
        pass

stepsize = 100
#%% CONVERT TO CHRONOLOGY
#Chronology is a dictionary of lists of wall posts sent at a given millisecond
chronology = dict()  #{time: ((sender, target),(sender,target))}

#def convertMultiDiGraphToChronology(multiDiGraph,beginTime,endTime):
#    for edge in multiDiGraph.edges(data='weight'):
#        timestamp = edge[2]
#        if timestamp >= beginTime and timestamp <= endTime:
#            s = edge[0]
#            t = edge[1]
#            #print('s: {}, t: {}, timestamp: {}'.format(s,t,timestamp))
#            if timestamp not in chronology:
#                chronology[timestamp] = list()
#            chronology[timestamp].append((s,t))
#    return chronology
def convertMultiDiGraphToChronology(multiDiGraph):
    '''Converts graph object into a dictionary with weights as keys'''
    times = set()
    for edge in multiDiGraph.edges(data='weight'):
        timestamp = edge[2]
        times.add(timestamp)
        s = edge[0]
        t = edge[1]
        if timestamp not in chronology.keys():
            chronology[timestamp] = list()
        chronology[timestamp].append((s,t))
    print('Unique times: ',len(times))
    return chronology
#VALIDATE
print("FOUND ALL WALL POSTS SENT IN {} {}".format(MONTH, YEAR))

#%% Take measurements
def takeMeasurement(network,verbose):
    '''Returns
    ---
    lcs, acc
    '''
    lcs = computeLCS(network)   #Largest component size
    acc = nx.average_clustering(network)   #Calculate average clustering coefficient
    return lcs, acc

def addMessages(G_empirical,step,beginTime,endTime,order=1,calcThresh=1,verbose=True):
    '''Add all messages from an actual network of Facebook messages sent between beginTime and endTime (Unix timestamps). \
If verbose=True (default: True) prints results at each calculation step 
    PARAMETERS
    ---
    G_empirical: nx MultiDiGraph object
        The network from which to draw messages as a multidigraph
    order: int
        1 for chronological (increasing time)
        2 for random
    calcThresh: int
        Critical threshold (in number of edges) at which to begin calculations
    RETURNS
    ---
    G_model: nx Graph object
        The network after adding messages
    t_list: list
        Times at which measurements were taken in terms of number of wall posts
    lcs_list: list
        List of largest component sizes at times in t_list
    acc_list: list
        List of average clustering coefficients at times in t_list
    '''
    #CONVERT GRAPH TO DICTIONARY OF MESSAGES WITH TIMES AS KEYS (THE CHRONOLOGY)
    chronology = convertMultiDiGraphToChronology(G_empirical)  #{time: (sender, target)}
    node_list = list(G_empirical.nodes())
    
    #SORT TIMES
    times = list(chronology.keys())
    if order==1:
        print("ORDER OF EDGE ADDITION: CHRONOLOGICAL")
        times.sort()   #Sort times chronologically
    elif order==2:
        print("ORDER OF EDGE ADDITION: RANDOM")
        random.shuffle(times)
    else:
        raise Exception("Unknown order")
    #VALIDATE
    print("FOUND ALL WALL POSTS SENT IN {} {}".format(MONTH, YEAR))    

    #DEFINE LISTS
    t_list = list()   #Time steps (number of messages added)
    lcs_list = list()  #Largest component
    acc_list = list()  #Average clustering coefficient
    
    G_model = nx.Graph()   #Empty graph
    V = len(G_empirical.edges())
    print("WALL POSTS TO ADD {}".format(V))
    G_model.add_nodes_from(node_list)   #Add nodes (so as to make sure that the average degree is averaged over all users who were active in the month)
    n = 0  #Edges added
    while n < V:
        timestamp = times.pop()
        messages = chronology[timestamp]
        #Add each message sent at a certain time
        for message in messages:
            from_user = message[0]
            to_user = message[1]
            
            if not G_model.has_edge(from_user,to_user):
                G_model.add_edge(from_user,to_user,weight=1)
            else:
                G_model[from_user][to_user]['weight']+=1
            n+=1
            #TODO: Temporary correction for looking for phase transition
            if n > calcThresh and n % step == 0:
                t_list.append(n)
                lcs,acc = takeMeasurement(G_model,verbose)
                lcs_list.append(lcs)
                acc_list.append(acc)
                node_weights = dict(G_model.degree(weight='weight')).values()
                #print(node_weights)
                mean_degree = sum(dict(nx.degree(G_model)).values())/len(G_model)
                if verbose==True:
                    print("Step: {}, LCS = {}, ACC = {:.3g}, mean_degree = {}".format(n,lcs,acc,mean_degree))
        
    return G_model,t_list, lcs_list,acc_list

#%%
stepsize = 100

CHRONOLOGICAL = 1
RANDOM = 2

calcThresh = 1

order = CHRONOLOGICAL
G,t_list,lcs_list,acc_list = addMessages(G_A,stepsize,beginTime,endTime,order=order,calcThresh=calcThresh,verbose=True)#
V = 66626
N = len(G.nodes())

#%% PREPARE FOR WRITING DATA
saveFile = 'empirical/Results/empirical_{}_{}_s{}.csv'.format(YEAR,MONTH,stepsize)
try:
    f = open(saveFile,'w')
except IOError:
    print("Problem opening file,adding a number to the end")
    f= open(saveFile+'1','w')
    
#%% SAVE RESULTS TO FILE

datestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
f.write('EDGES={}, ITERATIONS={},DATE={}\n'.format(V,iterations,datestamp))
f.write('Number of edges,Largest component size,Average Clustering Coefficient\n')
for i in range(len(t_list)):
    f.write('{},{},{}\n'.format(t_list[i],lcs_list[i],acc_list[i]))
f.close()

#%% PLOT LCS AND ACC
iterations = 100
label = "LCS"

fig = plt.figure()
ax2 = fig.add_subplot(111)
ax2.set_title("Empirical: V={}, N={}, s={}, I={} {}".format(V,N,stepsize,iterations,label))
ax2.set_xlabel("Wall posts, m")
ax2.set_ylabel("{}".format(label))
ax2.grid()
ax2.set_xticks(np.arange(0,max(t_list),10000))

ax2.plot(t_list,lcs_list)

label = "ACC"
fig = plt.figure()
ax2 = fig.add_subplot(111)
ax2.set_title("Empirical: V={}, N={}, s={}, I={} {}".format(V,N,stepsize,iterations,label))
ax2.set_xlabel("Wall posts, m")
ax2.set_ylabel("{}".format(label))
ax2.grid()
ax2.set_xticks(np.arange(min(t_list),max(t_list),10000))
ax2.plot(t_list,acc_list,"orange")

#ax2.plot('LCS',t_list,lcs_list,np.zeros(len(t_list)),V,N,stepsize,1,len(t_list))
#ax2.plot('ACC',t_list,acc_list,np.zeros(len(t_list)),V,N,stepsize,1,len(t_list))