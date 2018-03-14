#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  9 15:06:56 2018

@author: RamanSB
"""

import numpy as np
import BA
from matplotlib import pyplot as plt
import time

m=2
N=10
graphs = [BA.BA(m, N)]

startTime = time.time()

for graph in graphs:
    no = graph.getNo() #Initial number of nodes in graph.
    N = graph.getN() #Final number of nodes required
    maxTime = N - no #Time required / amount of vertices to add to obtain N vertices
    timeArray = list(range(1, maxTime+1)) #Intervals of 1.
    
    for t in timeArray:
        newNodeLabel = no + t - 1
        graph.addNewNodeToNetwork(newNodeLabel)
        graph.addEdgesViaPPA()
    
    print(len(graph.getNodeList()))
    
    print("Code completed in {}s".format(time.time()-startTime))

graphs[-1].drawNetwork()