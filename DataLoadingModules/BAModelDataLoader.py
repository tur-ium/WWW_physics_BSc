#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 16 16:08:26 2018

@author: RamanSB
"""
'''
1) set generatedDataFilePath to the filePath containing .../BA/
'''

import numpy as np
from matplotlib import pyplot as plt


generatedDataFilePath = "/Users/RamanSB/Documents/University/3rd-Year Physics/3rd Year Project/GeneratedData/BAData/"
stepSize = 50        


def collateData(collateLCS=True, collateACC=True, noOfFiles=10):
    LCS_all_add = [[] for i in range(noOfFiles)]
    ACC_all_add = [[] for i in range(noOfFiles)]
    
    LCS_all_remove = [[] for i in range(noOfFiles)]
    ACC_all_remove = [[] for i in range(noOfFiles)]
    
    if(collateLCS):
        for i in range(noOfFiles):
            lcs_file = open(generatedDataFilePath+str(i)+"LCS-BA-ADD", mode='r')
            for line in lcs_file:
                data = line.replace("\n", "")
                LCS_all_add[i].append(data)
        print("LCS values for adding wall-posts have been collected")
        
        for i in range(noOfFiles):
            lcs_file = open(generatedDataFilePath+str(i)+"LCS-BA-REMOVE", mode='r')
            for line in lcs_file:
                data = line.replace("\n", "")
                LCS_all_remove[i].append(data)
        print("ACC values for removing wall-posts have been collected")
    
    if(collateACC):
        for i in range(noOfFiles):
            acc_file = open(generatedDataFilePath+str(i)+"ACC-BA-ADD", mode='r')
            for line in acc_file:
                data = line.replace("\n", "")
                ACC_all_add[i].append(data)
        print("ACC values for adding wall-posts have been collected")
        
        for i in range(noOfFiles):
            acc_file = open(generatedDataFilePath+str(i)+"ACC-BA-REMOVE", mode='r')
            for line in acc_file:
                data = line.replace("\n", "")
                ACC_all_remove[i].append(data)
        print("ACC values for removing wall-posts have been collected")
    
   
        
        
    return LCS_all_add, LCS_all_remove, ACC_all_add, ACC_all_remove
       
def processData(LCS_ADD, LCS_REMOVE, ACC_ADD, ACC_REMOVE):
    
    avg_lcs_add = []
    std_lcs_add = []
    
    avg_lcs_remove = []
    std_lcs_remove = []
    
    avg_acc_add = []
    std_acc_add = []
    
    avg_acc_remove = []
    std_acc_remove = []
    
    for i in range(len(LCS_ADD[0])):
        LCS_ADD_vals = []
        
        for j in range(len(LCS_ADD)):
            LCS_ADD_vals.append(LCS_ADD[j][i])
         
        LCS_ADD_vals = np.asarray(LCS_ADD_vals, dtype='float64')
        avg_lcs_add.append(np.mean(LCS_ADD_vals))
        std_lcs_add.append(np.std(LCS_ADD_vals))
        
    
    for i in range(len(LCS_REMOVE[0])):
        LCS_REMOVE_vals = []
        for j in range(len(LCS_REMOVE)):
            LCS_REMOVE_vals.append(LCS_REMOVE[j][i])
        LCS_REMOVE_vals = np.asarray(LCS_REMOVE_vals, dtype='float64')
        avg_lcs_remove.append(np.mean(LCS_REMOVE_vals))
        std_lcs_remove.append(np.std(LCS_REMOVE_vals))
        
  
        
    for i in range(len(ACC_ADD[0])):
        ACC_ADD_vals = []
        for j in range(len(ACC_ADD)):
            ACC_ADD_vals.append(ACC_ADD[j][i])
        ACC_ADD_vals = np.asarray(ACC_ADD_vals, dtype='float64')
        avg_acc_add.append(np.mean(ACC_ADD_vals))
        std_acc_add.append(np.std(ACC_ADD_vals))

    for i in range(len(ACC_REMOVE[0])):
        ACC_REMOVE_vals = []
        for j in range(len(ACC_REMOVE)):
            ACC_REMOVE_vals.append(ACC_REMOVE[j][i])
        ACC_REMOVE_vals = np.asarray(ACC_REMOVE_vals, dtype='float64')
        avg_acc_remove.append(np.mean(ACC_REMOVE_vals))
        std_acc_remove.append(np.std(ACC_REMOVE_vals))
        
   
    return avg_lcs_add, std_lcs_add, avg_lcs_remove, std_lcs_remove, avg_acc_add, std_acc_add, avg_acc_remove, std_acc_remove


def plotData(plotACC=True, plotLCS=True, plotErrors=True, plotSTD=True):
    
    
     x = (np.array(list(range(len(AVG_LCS_ADD))))+1)*stepSize #1-1332 (Multiples of 50 (edges added))
     xr = list(x)[::-1]
     xLabel = "Number Of Wall Posts"
     title = "Order Parameter Evolution with varying number of wall-posts"
     
     if(plotLCS):
  
        plt.figure()
        plt.grid()
        plt.xlabel(xLabel)
        plt.ylabel("Average largest component size")
        plt.title(title)
        plt.plot(x, AVG_LCS_ADD, color='r', label="adding wall-posts")
        plt.legend()
        plt.plot(xr, AVG_LCS_REMOVE, color='b', label="removing wall-posts")
        plt.legend()
        plt.show()

     if(plotLCS and plotErrors):

        plt.figure()
        plt.grid()
        plt.xlabel(xLabel)
        plt.ylabel("Average largest component size")
        plt.title(title)
        plt.errorbar(x, AVG_LCS_ADD, yerr=STD_LCS_ADD, color='r', label="adding wall-posts")
        plt.legend()
        plt.errorbar(xr, AVG_LCS_REMOVE, yerr=STD_LCS_REMOVE, color='b', label="removing wall-posts")
        plt.legend()
        plt.show()
        
     if(plotACC):
        plt.figure()
        plt.grid()
        plt.xlabel(xLabel)
        plt.ylabel("Average clustering coefficient")
        plt.title(title)
        plt.plot(x, AVG_ACC_ADD, color='r', label="adding wall-posts")
        plt.legend()
        plt.plot(xr, AVG_ACC_REMOVE, color='b', label="removing wall-posts")
        plt.legend()
        plt.show()
    
     if(plotACC and plotErrors):
        plt.figure()
        plt.grid()
        plt.xlabel(xLabel)
        plt.ylabel("Average clustering coefficient")
        plt.title(title)
        plt.errorbar(x, AVG_ACC_ADD, yerr=STD_ACC_ADD, color='r', label="adding wall-posts")
        plt.legend() 
        plt.errorbar(xr, AVG_ACC_REMOVE, yerr=STD_ACC_REMOVE, color='b', label="removing wall-posts")
        plt.legend()
        plt.show()
    
     if(plotSTD):
         if(plotACC):
            plt.figure()
            plt.grid()
            plt.xlabel("Number of Wall-posts, W")
            plt.ylabel("$\sigma_{ACC}$")
            plt.plot(x, STD_ACC_ADD, color='r', label="STD Adding wall-posts")
            plt.legend()
            plt.plot(xr, STD_ACC_REMOVE, color='b',  label="STD Removing wall-posts")
            plt.legend()
            plt.show()
            
         if(plotLCS):
            plt.figure()
            plt.grid()
            plt.xlabel("Number of Wall-posts, W")
            plt.ylabel("$\sigma_{LCS}$")
            plt.plot(x, STD_LCS_ADD, color='r', label="STD Adding wall-posts")
            plt.legend()
            plt.plot(xr, STD_LCS_REMOVE, color='b', label="STD Removing wall-posts")
            plt.legend()
            plt.show()
        
     
    
    
    

    
LCS_ADD, LCS_REMOVE, ACC_ADD, ACC_REMOVE = collateData(noOfFiles=10)
AVG_LCS_ADD, STD_LCS_ADD, AVG_LCS_REMOVE, STD_LCS_REMOVE, AVG_ACC_ADD, STD_ACC_ADD, AVG_ACC_REMOVE, STD_ACC_REMOVE = processData(LCS_ADD, LCS_REMOVE, ACC_ADD, ACC_REMOVE)
plotData()