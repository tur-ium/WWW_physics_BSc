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
import networkx_extended as nx
from measure_new import computeLCS, getDegreeDist, computeClusteringCoefficient
from matplotlib import pyplot as plt
import random
import datetime
import numpy as np


#%% PARAMETERS

#TIMESLICE PARAMETERS
dataDirectory = "C:/Users/admin/Documents/Physics/year 3/WWWPhysics-PC/empirical/Data/TimeSlicedDataNew/TimeSlicedData"

YEAR = '2008'
MONTH = 'DEC'
ENDYEAR = '2009'   
ENDMONTH = 'JAN' #End at the BEGINNING of this month

#THERMODYNAMIC MODELLING PARAMETERS
stepsize =  100  #Number of edges to add between calculations
calcThresh = 1  #Number of edges to add before beginning calculations
#Order of addition
CHRONOLOGICAL = 1
RANDOM = 2
order = CHRONOLOGICAL

#SAVING DATA PARAMETERS
saveFile = 'incoming_results/empirical_{}_{}_step_{}.csv'.format(YEAR,MONTH,stepsize)

#%% PREPARE FOR WRITING DATA
try:
    f = open(saveFile,'w')
except IOError:
    print("Problem opening file,adding a number to the end")
    f= open(saveFile+'1','w')


#%% LOAD DATA

#weightedGraph = ts.loadGEXF("C:/Users/admin/Documents/Physics/year 3/WWWPhysics-PC/empirical/Data/WeightedNetwork/2008_DEC_WeightedGraph.gexf")

beginTime = ts.TIME_DICT[YEAR][MONTH]  #NOTE Time at beginning of month
endTime = ts.TIME_DICT[ENDYEAR][ENDMONTH] #NOTE Time at beginning of month

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
                    print("Step: {}, LCS = {}, ACC = {:.3g}, mean_degree = {:.3g}".format(n,lcs,acc,mean_degree))
        
    return G_model,t_list, lcs_list,acc_list

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
    
    edge_list = list(G_model.edges(data='weight'))

    weighted_degree = dict(G.degree(weight='weight')).values()
    V = sum(weighted_degree)/2
    while V > Vmin:
        edge_idx = random.choice(range(len(edge_list)))  #Edge index
        edge = edge_list[edge_idx]
        
        from_user = edge[0]
        to_user = edge[1]
        
        if G_model[from_user][to_user]['weight']>1:
            G_model[from_user][to_user]['weight']-=1
        else:
            edge_list.pop(edge_idx)
            G_model.remove_edge(from_user,to_user)
        V-=1
        
        if V % step == 0:
            m_list.append(V)
            lcs,acc = takeMeasurement(G_model,verbose)
            lcs_list.append(lcs)
            acc_list.append(acc)            
            if verbose==True:
                print("Step: {}, LCS = {}, ACC = {:.3g}".format(V,lcs,acc))
    return G_model, m_list, lcs_list,acc_list
#%% ADD AND REMOVE MESSAGES
print("ADDING EDGES")
G,t_list,lcs_list,acc_list = addMessages(G_A,stepsize,beginTime,endTime,order=order,calcThresh=calcThresh,verbose=True)
V = 66626
N = len(G.nodes())

print("REMOVING EDGES")
G,m_list,lcs_list_r,acc_list_r = removeMessages(G,stepsize,0,verbose=True)

edgesAdded = len(lcs_list)  #Number of edges added

#    Add results for removal to end of lists    
t_list.extend(m_list)
lcs_list.extend(lcs_list_r)
acc_list.extend(acc_list_r)
lcs_unc = np.zeros_like(lcs_list)   #TODO: repeat random removal
acc_unc = np.zeros_like(acc_list)   #TODO: Calculate ACC
#%% SAVE RESULTS TO FILE

datestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
f.write('EDGES={}, DATE={}, STEPSIZE={}\n'.format(V,datestamp,stepsize))
f.write('Number of edges,Largest component size,Average Clustering Coefficient\n')
for i in range(len(t_list)):
    f.write('{},{},{},{},{}\n'.format(t_list[i],lcs_list[i],lcs_unc[i],acc_list[i],acc_unc[i]))
f.close()

#%% PLOT LCS AND ACC

#DATA COLLAPSE
iterations = 100
label = "LCS"

lcs_normalised = [lcs/N for lcs in lcs_list]
t_normalised = [t/V for t in t_list]

#%%PLOT
import AR_cycle
label="LCS"
AR_cycle.plot(label,t_normalised,lcs_normalised,np.zeros(len(t_list)),V,N,stepsize,1,edgesAdded,False,"Empirical")
label="ACC"
AR_cycle.plot(label,t_normalised,acc_list,np.zeros(len(t_list)),V,N,stepsize,1,edgesAdded,False,"Empirical")