#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 16 15:01:45 2018

@author: RamanSB
"""

#import RModelDataLoader as RLoader
import BAModelDataLoader as BALoader
from matplotlib import pyplot as plt
import numpy as np

p = [0.5, 0.75, 1] #Get p=0 and 0.25


def showRModelCollapse(p, showLCS=True, showACC=True):
    
    for P in p:
        plt.figure()
        plt.title("Data Collapsed R Model")
        plt.xlabel("Normalized - Number of Wall Posts, w/W")
        plt.grid()
        LCS_ADD_R, LCS_REMOVE_R, ACC_ADD_R, ACC_REMOVE_R = RLoader.collateData(P, collateLCS=True, collateACC=True, noOfFiles=20)
        avg_lcs_add_R, std_lcs_add_R, avg_lcs_remove_R, std_lcs_remove_R, avg_acc_add_R, std_acc_add_R, avg_acc_remove_R, std_acc_remove_R = RLoader.processData(LCS_ADD_R, LCS_REMOVE_R, ACC_ADD_R, ACC_REMOVE_R)
        normalizedX_R, normalizedXr_R, normalized_LCS_ADD_R, normalized_LCS_REMOVE_R, normalized_ACC_ADD_R, normalized_ACC_REMOVE_R = RLoader.dataCollapse(avg_lcs_add_R, avg_lcs_remove_R, avg_acc_add_R, avg_acc_remove_R, P)
        if(showLCS):
            plt.ylabel("Normalized LCS")
            plt.grid()
            plt.plot(normalizedX_R, normalized_LCS_ADD_R, color='r', label="p={}, Wall-posts Addition".format(P))
            plt.plot(normalizedXr_R, normalized_LCS_REMOVE_R, color='b', label="p={}, Wall-posts Removal".format(P))
            plt.legend()
            plt.show()
        if(showACC):
            plt.ylabel("Normalized ACC")
            plt.grid()
            plt.plot(normalizedX_R, normalized_ACC_ADD_R, color='r', label="p={}, Wall-posts Addition".format(P))
            plt.plot(normalizedXr_R, normalized_ACC_REMOVE_R, color='b', label="p={}, Wall-posts Removal".format(P))
            plt.legend()
            plt.show()
        


def showBAModelCollapse(showLCS=True, showACC=True):
    plt.figure()
    plt.title("Data Collapsed BA Model")
    plt.xlabel("Normalized - Number of Wall Posts, w/W")
    plt.ylabel("Normalized LCS")
    plt.grid()
    plt.plot()
    LCS_ADD_BA, LCS_REMOVE_BA, ACC_ADD_BA, ACC_REMOVE_BA = BALoader.collateData(collateLCS=True, collateACC=True, noOfFiles=20)
    avg_lcs_add_BA, std_lcs_add_BA, avg_lcs_remove_BA, std_lcs_remove_BA, avg_acc_add_BA, std_acc_add_BA, avg_acc_remove_BA, std_acc_remove_BA = BALoader.processData(LCS_ADD_BA, LCS_REMOVE_BA, ACC_ADD_BA, ACC_REMOVE_BA)
    normalizedX_BA, normalizedXr_BA, normalized_LCS_ADD_BA, normalized_LCS_REMOVE_BA, normalized_ACC_ADD_BA, normalized_ACC_REMOVE_BA = BALoader.dataCollapse(avg_lcs_add_BA, avg_lcs_remove_BA, avg_acc_add_BA, avg_acc_remove_BA)
    if(showLCS):
        plt.plot(normalizedX_BA, normalized_LCS_ADD_BA, color='r', label="Wall-posts Addition")
        plt.plot(normalizedXr_BA, normalized_LCS_REMOVE_BA, color='b', label="Wall-posts Removal")
        plt.legend()
        plt.show()
    if(showACC):
        plt.plot(normalizedX_BA, normalized_ACC_ADD_BA, color='r', label="Wall-posts Addition")
        plt.plot(normalizedXr_BA, normalized_ACC_REMOVE_BA, color='b', label="Wall-posts Removal")
        plt.legend()
        plt.show()
    


showBAModelCollapse(p)