# -*- coding: utf-8 -*-
"""
Created on Fri Apr 20 15:43:42 2018

@author: admin
"""

data_dir = '../results/configurational/raw/'
filepath_Config = '{}config-model_Results_stepsize50_combined.csv'.format(data_dir)

def loadConfigurationalData(filePath):
    '''Load data from filePath
    
    RETURNS m_list,lcs,lcs_unc,acc,acc_unc
    ----
    m_list: list of number of messages (sum of edge weights) in the network at the time of measurement
    lcs,lcs_unc,acc,acc_unc: lists of the Largest Component Size (LCS), Average Clustering Coefficient (ACC) at the measurement times in m_list'''

    f = open(filePath,'r')
    
    n = 0  #Line counter
    
    m_list = list()
    acc_list = list()
    acc_unc_list = list()
    lcs_list= list()
    lcs_unc_list = list()
    
    for raw_line in f:
        raw_line = raw_line.replace('\n','')
        line = raw_line.split(sep=',')
    
        if n > 1:
            m = int(float(line[0]))
            lcs = float(line[1])
            lcs_unc = float(line[2])
            acc = float(line[3])
            acc_unc = float(line[4])     
            
            m_list.append(m)
            lcs_list.append(lcs)
            acc_list.append(acc)
            lcs_unc_list.append(lcs_unc)
            acc_unc_list.append(acc_unc)
        elif n==0:
            print("METADATA FOR THIS FILE:")
            print("{}\n".format(line))
        elif n < 10:
            print(line)
        n+=1
    return m_list,lcs_list,lcs_unc_list,acc_list,acc_unc_list
t_list, lcs, lcs_unc, acc, acc_unc = loadConfigurationalData(filepath_Config)

#c: Point in the list of calculated edges at which the removal begins
c = int(len(t_list)/2)

t_list_add = t_list[:-c]
lcs_add = lcs[:-c]
lcs_unc_add = lcs_unc[:-c]
acc_add = acc[:-c]
acc_unc_add = acc_unc[:-c]

t_list_remove = t_list[-c+1:]
lcs_remove = lcs[-c+1:]
lcs_unc_remove = lcs_unc[-c+1:]
acc_remove = acc[-c+1:]
acc_unc_remove = acc_unc[-c+1:]