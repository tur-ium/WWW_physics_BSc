#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 11 20:35:03 2018


@author: RamanSB

Data Analysis on Activity Network
"""

import networkx as nx
import Timeslice as ts
import random
import time 
import numpy as np
from matplotlib import pyplot as plt

startTime = time.time()
print("Code Started")

def componentSizes(G):
    Max_SCCSize = len(max(nx.strongly_connected_components(G), key=len))
    MAX_WCCSize = len(max(nx.weakly_connected_component_subgraphs(G),key=len))
    return Max_SCCSize, MAX_WCCSize


#Enter Periods as [YEAR, 'MONTH'] - i.e. [2005, 'JAN'] to [2007, 'DEC']
def plotGCSTimeSeries(startPeriod, endPeriod, log=False):
    startIndex = ts.TIME_ARRAY.index(str(startPeriod[0])+"-{}".format(startPeriod[1]))
    endIndex = ts.TIME_ARRAY.index(str(endPeriod[0])+"-{}".format(endPeriod[1]))
    
    xAxis = list(range(endIndex-startIndex))
    xTicks = ts.TIME_ARRAY[startIndex:endIndex]
    
    SCCSs = []
    WCCSs = []
    for period in xTicks:
        yearMonth = period.split("-")
        year = yearMonth[0]
        month = yearMonth[1]
        loadedNetworkPeriod = ts.loadGEXF(ts.cumulative_filePath_gexf+"{}/C{}_{}_MultiDiGraph.gexf".format(year, year, month))
        networkSCCS, networkWCCS = componentSizes(loadedNetworkPeriod)
        SCCSs.append(networkSCCS)
        WCCSs.append(networkWCCS)
    
    
    fig = plt.figure(figsize=(12, 5))
    plt.grid()
    plt.title("Giant Component Size Time Series")
    plt.xticks(xAxis, xTicks, rotation=90)
    plt.xlabel("Time, $T$")
    plt.ylabel("Component Size, $GCS$")
    if(not log):
        plt.plot(xAxis, SCCSs, 'x', label="Largest SCC Size")
        plt.plot(xAxis, WCCSs, 'x', label="Largest WCC Size")
    if(log):
        plt.plot(np.log10(xAxis), np.log10(SCCSs), 'x', label="Log-Log Max SCC Size")
        plt.plot(np.log10(xAxis), np.log10(WCCSs), 'x', label="Log-Log Max WCC Size")
   
    plt.legend()
    

    
    
plotGCSTimeSeries([2004, 'OCT'], [2009, 'JAN'], log=True)





endTime = time.time()

print("Code completed in {}s".format(endTime-startTime))