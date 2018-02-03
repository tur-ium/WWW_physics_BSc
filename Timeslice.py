#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 26 15:25:51 2018

@author: RamanSB
"""

import networkx as nx
import numpy as np
import time
from matplotlib import pyplot as plt


activityEdgelistPath = "/Users/RamanSB/Documents/University/3rd-Year Physics/3rd Year Project/Real Data/activity_network_edge_list.txt"

EPOCH_MIN = 1095135831 #"Tuesday, 14 September 2004 04:23:51"
EPOCH_MAX = 1232598691 #"Thursday, 22 January 2009 04:31:31"

filePath_text = "/Users/RamanSB/Documents/University/3rd-Year Physics/3rd Year Project/Real Data/TimeSlicedData/TextEdgeList/"
filePath_gexf = "/Users/RamanSB/Documents/University/3rd-Year Physics/3rd Year Project/Real Data/TimeSlicedData/GEXF/"

#Could be more succinct, but would depend on users naming convention - multiple variables for filePaths avoids dependancy on naming conventions.
filePath_text_2004 = filePath_text+"2004/"
filePath_text_2005 = filePath_text+"2005/"
filePath_text_2006 = filePath_text+"2006/"
filePath_text_2007 = filePath_text+"2007/"
filePath_text_2008 = filePath_text+"2008/"
filePath_text_2009 = filePath_text+"2009/"

filePath_gexf_2004 = filePath_gexf+"2004/"
filePath_gexf_2005 = filePath_gexf+"2005/"
filePath_gexf_2006 = filePath_gexf+"2006/"
filePath_gexf_2007 = filePath_gexf+"2007/"
filePath_gexf_2008 = filePath_gexf+"2008/"
filePath_gexf_2009 = filePath_gexf+"2009/"

#Generated via time.mktime( (year, month, day, 0,0,0,0,0,0 ) ) - Verified times using: https://www.epochconverter.com
TIME_DICT =  {
         "2004":{"JAN":1072915200, "FEB":1075593600, "MAR":1078099200, "APR":1080777600, "MAY":1083369600, "JUN":1086048000, "JUL":1088640000, "AUG":1091318400, "SEP":1093996800, "OCT":1096588800, "NOV":1099267200, "DEC":1101859200}
        ,"2005":{"JAN":1104537600, "FEB":1107216000, "MAR":1109635200, "APR":1112313600, "MAY":1114905600, "JUN":1117584000, "JUL":1120176000, "AUG":1122854400, "SEP":1125532800, "OCT":1128124800, "NOV":1130803200, "DEC":1133395200}
        ,"2006":{"JAN":1136073600, "FEB":1138752000, "MAR":1141171200, "APR":1143849600, "MAY":1146441600, "JUN":1149120000, "JUL":1151712000, "AUG":1154390400, "SEP":1157068800, "OCT":1159660800, "NOV":1162339200, "DEC":1164931200}
        ,"2007":{"JAN":1167609600, "FEB":1170288000, "MAR":1172707200, "APR":1175385600, "MAY":1177977600, "JUN":1180656000, "JUL":1183248000, "AUG":1185926400, "SEP":1188604800, "OCT":1191196800, "NOV":1193875200, "DEC":1196467200}
        ,"2008":{"JAN":1199145600, "FEB":1201824000, "MAR":1204329600, "APR":1207008000, "MAY":1209600000, "JUN":1212278400, "JUL":1214870400, "AUG":1217548800, "SEP":1220227200, "OCT":1222819200, "NOV":1225497600, "DEC":1228089600}
        ,"2009":{"JAN":1230768000, "FEB":1233446400, "MAR":1235865600, "APR":1238544000, "MAY":1241136000, "JUN":1243814400, "JUL":1246406400, "AUG":1249084800, "SEP":1251763200, "OCT":1254355200, "NOV":1257033600, "DEC":1259625600}     
        }

YEARS = TIME_DICT.keys()
MONTHS = TIME_DICT['2004'].keys()

TIME_ARRAY = []
for year in YEARS:
        for month in MONTHS:
            TIME_ARRAY.append("{}-{}".format(year, month))


def readEdgelistFromPath(edgelistFilePath, isWeighted=False):
    edgelist_data = open(edgelistFilePath, mode='r')
    if(isWeighted):
        weighted_edgelist = []
        
        for line in edgelist_data:   
            edge_data = line.split()
            #Edge_data[0] - from node, #Edge_data[1] - to node, #Edge-data[2]- weight
            weighted_edgelist.append([(edge_data[0], edge_data[1]), edge_data[2]])
         
        return weighted_edgelist
    
    else:
        edge_list = []
        for line in edgelist_data:
            edge_list.append(line.split())
        
        
        return edge_list
        
    
def timeSliceEdges(edgeList, startTime=EPOCH_MIN, cutOffTime=EPOCH_MAX, retainWeights=False):
    
    if(startTime < EPOCH_MIN or cutOffTime > EPOCH_MAX):
        raise TypeError("Start time must be greater than or equal to EPOCH_MIN.\nCut-off time must be less than or equal to EPOCH_MAX")
    
    timeSlicedEdgeList = []
    epoch_times = []
    for edges in edgeList:
        epoch_times.append(int(edges[1]))
        
    for i in range(len(edgeList)):
        #Note cutOffTime is inclusive.
        if(epoch_times[i] >= startTime and epoch_times[i] <= cutOffTime):
            if(retainWeights):
                timeSlicedEdgeList.append(edgeList[i])
            else:
                timeSlicedEdgeList.append(edgeList[i][0])
    #Implement date time functionality in to this, would be nice to have dates here.
    #time.localtime
    st = time.localtime(startTime)
    ct = time.localtime(cutOffTime)
    print("\nGenerated time sliced edge list from: {}/{}/{} to {}/{}/{}".format(st.tm_mday, st.tm_mon, st.tm_year, ct.tm_mday, ct.tm_mon, ct.tm_year))
    return timeSlicedEdgeList


def generateTimeSliceGraph(timeSlicedEdgeList, isWeighted=False):
    G = nx.MultiDiGraph()
    G.add_edges_from(timeSlicedEdgeList)
    return G
        
        
def writeEdgeListToFile(edgeList, filePath, fileName):
    edgeListFile = open(filePath+fileName, mode='w')
    edgeListFile.write('\n'.join('{} {}'.format(edge[0], edge[1]) for edge in edgeList))       
    edgeListFile.close()
    

def createGEXFFromGraph(graph, filePath, fileName):
    nx.gexf.write_gexf(graph, filePath+fileName)
    print("GEXF created: " + str(fileName))
            
    
def loadGEXF(GEXF_filePath):
    return nx.gexf.read_gexf(GEXF_filePath)

#Start Period - [Year, Month] - (Not Inclusive) [Year, Month]
def plotInteractionsPerMonth(startPeriod, endPeriod):
    
    noOfInteractions = []
   
    startIndex = TIME_ARRAY.index("{}-{}".format(startPeriod[0], startPeriod[1]))
    endIndex = TIME_ARRAY.index("{}-{}".format(endPeriod[0], endPeriod[1]))
   
    xAxis = list(range(endIndex-startIndex))
    xTicks = TIME_ARRAY[startIndex:endIndex]
    
   
    for date in xTicks:
        monthYear = date.split('-')
        year = monthYear[0]
        month = monthYear[1]
        interactionCount = len(open(filePath_text+str(year)+"/{}_{}.txt".format(year, month), mode='r').readlines())
        noOfInteractions.append(interactionCount)

    fig = plt.figure(figsize=(12, 5))
    
    plt.grid()
    plt.title("Interactions per Month")
    plt.xticks(xAxis, xTicks, rotation=90)
    plt.xlabel("Time period, $T$")
    plt.ylabel("Number of interactions, $N$")
    plt.plot(xAxis, noOfInteractions, 'o')
    plt.show()


#StartPeriod - [Year, Month], cutOffPeriod - [Year, Month] - Not Done
def plotClusterSize(startTime, cutOffTime):
    startIndex = TIME_ARRAY.index("{}-{}".format(startPeriod[0], startPeriod[1]))
    endIndex = TIME_ARRAY.index("{}-{}".format(endPeriod[0], endPeriod[1]))




'''
#EXTREMELY IMPORTANT TO NOT TAMPER WITH COMMENTED CODE BELOW AS IT MAY OVERWRITE EXISTING TIME SLICED DATA.
'''
#edgeList = readEdgelistFromPath(activityEdgelistPath, isWeighted=True)
#timeSlicedEdgeList = timeSliceEdges(edgeList, TIME_DICT["2009"]["JAN"], 1232598691, retainWeights=False)
#G = generateTimeSliceGraph(timeSlicedEdgeList)
#createGEXFFromGraph(G, filePath_gexf_2009, "2009_JAN-22_MultiDiGraph.gexf")
#writeEdgeListToFile(timeSlicedEdgeList, filePath_text_2009, "2009_JAN-22.txt")


#plotInteractionsPerMonth([2004, 'OCT'],[2009, 'JAN'])
#G_OCT_2004 = loadGEXF(filePath_gexf_2004+"2004_OCT_MultiDiGraph.gexf")
    





'''

jabberwocky ignore - don't delete though. 

activityNetworkFilePath = "/Users/RamanSB/Documents/University/3rd-Year Physics/3rd Year Project/Real Data/activity_network_multi_directed.gexf"
isNetworkLoaded = False

def loadNetworkFromGEXF(GEXF_file_path):
        return nx.gexf.read_gexf(GEXF_file_path)
    


G_A = loadNetworkFromGEXF(activityNetworkFilePath) #Loads MultiDiGraph for Activity Network


edges = nx.edges(G_A)


for edge in nx.edges(G_A):
    print(G_A.get_edge_data(edge[i][0], edge[i][1]))
    if(i==200):
        break

for i in range(len()):
    print("\n\n\n")
    print(G_A.get_edge_data(edges[i][0], edges[i][1]))
'''

'''
for i in range(3):
    print("\n\n\n\n")
    edge_dict = G_A.get_edge_data(edges[i][0], edges[i][1])
    print(edge_dict)
'''