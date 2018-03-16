#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  9 18:37:28 2018

@author: RamanSB
"""

#Intend to calculate - Largest Component Size as a function of edges attached.
import measure_new
import networkx as nx
from matplotlib import pyplot as plt
import numpy as np

generatedDataFilePath = "/Users/RamanSB/Documents/University/3rd-Year Physics/3rd Year Project/GeneratedData/BA/"
class Analysis():
    
    
    def __init__(self):
        print("Initiated Analysis")
        self.LCSa = []
        self.ACCa = []
        self.LCSr = []
        self.ACCr = []
        self.avgShortTestPath = []
        self.finalDegreeDistribution = []
        
    
    def computeLCS(self, G, iteration, removal=False, addition=False):
        LCS = len(max(nx.connected_components(G)))
        if(removal):
            self.LCSr.append(LCS)
            self.writeDataToFile(generatedDataFilePath+str(iteration)+"LCS-BA-REMOVE", LCS)
        elif(addition):
            self.LCSa.append(LCS)
            self.writeDataToFile(generatedDataFilePath+str(iteration)+"LCS-BA-ADD", LCS)
            
            
    def computeACC(self, G, iteration, removal=False, addition=False):
        ACC = nx.average_clustering(G)
        if(removal):
            self.ACCr.append(ACC)
            self.writeDataToFile(generatedDataFilePath+str(iteration)+"ACC-BA-REMOVE", ACC)
        elif(addition):
            self.ACCa.append(ACC)
            self.writeDataToFile(generatedDataFilePath+str(iteration)+"ACC-BA-ADD", ACC)
            
    def writeDataToFile(self, fileName, data):
        try:
            file = open(fileName, mode='a+')
            file.writelines("{}\n".format(data))
        except:
            file = open(fileName, mode='w')
            file.writelines("{}\n ".format(data))
        file.close()    
    
    def computeSPAndDiameter(self, G):
        nx.shortest_path()
        nx.diameter(G)
        
        

    def plotOrderParameterWithEdges(self, plotLCS=True, plotACC=True):
        if(plotLCS):
            plt.figure()
            plt.title("Order parameter against edges (LCS)")
            plt.xlabel("Number of weights, W (Mulitples of 50)")
            plt.ylabel("Largest Component Size")
            plt.grid()
            xData = list(range(len(self.LCSa)))
            xDataR = list(range(len(self.LCSr)))[::-1]
            print("Xr {}".format(len(xDataR)))
            plt.plot(xData, self.LCSa, color='r', label="Addition of Wall-posts")
            plt.legend()
            plt.plot(xDataR, self.LCSr, color='b', label="Removal of Wall-posts")
            plt.legend()
            
            
        if(plotACC):
            plt.figure()
            plt.title("Order parameter against Wall-posts (ACC)")
            plt.xlabel("Number of Wall-posts, W (Mulitples of 50)")
            plt.ylabel("Average Clustering Coefficient")
            plt.grid()
            xData = list(range(len(self.ACCa)))
            xDataR = list(range(len(self.ACCr)))[::-1]
            plt.plot(xData, self.ACCa, color='r', label="Addition of Wall-posts")
            plt.plot(xDataR, self.ACCr, color='b', label="Removal of Wall-posts")
            plt.legend()
            

    
        