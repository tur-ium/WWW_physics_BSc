# -*- coding: utf-8 -*-
"""
Created on Wed Mar 14 12:56:04 2018

@author: admin
"""
import AR_cycle   #This contains the plotting function

V = 66626  #Parameters for loading data
N = 23396  #Parameters for loading data

filePath_empirical = 'results/empirical_activity/raw/empirical_2008_DEC_step_100.csv'
models =['erdos-renyi','configurational','R_model','BA']

#SHORT CODES FOR EACH model
ER = 0
CONFIG = 1
R = 2
BA = 3

model = models[CONFIG]

filePath_model = 'results/{}/raw/{}_ResultsV={}N={}.csv'.format(model,model,V,N)

def loadData(filePath,empirical):
    '''Load data from filePath
    If empirical, use emprical=True
    NOTE THERE ARE NO UNCERTAINTIES WHEN ADDING EDGES CHRONOLOGICALLY
    
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
            m = int(line[0])
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
            if empirical:
                DATE = line[1]
                print("DATA COLLECTED: {}".format(DATE))
            else:
                MESSAGES = line[0]
                ITERATIONS = line[1]
                DATE = line[2]
                print("DATA COLLECTED ON: {}\nNUMBER OF MESSAGES: {}\nITERATIONS: {}".format(DATE,MESSAGES,ITERATIONS))
        if n < 10:
            print(line)
        n+=1
    return m_list,lcs_list,lcs_unc_list,acc_list,acc_unc_list
#%%EXAMPLE
m,lcs,lcs_unc,acc,acc_unc=loadData(filePath_model,False)
#m,lcs,lcs_unc,acc,acc_unc=loadData(filePath_empirical,False)   #Uncomment for empirical

#%%

#Plot model
AR_cycle.plot('LCS',m,lcs,lcs_unc,'','','','',int(len(lcs)*.5),plotUncertainty=True,model_name=model)
AR_cycle.plot('ACC',m,acc,acc_unc,'','','','',int(len(acc)*.5),plotUncertainty=True,model_name=model)
#Plot empirical
#AR_cycle.plot('LCS',m,lcs,lcs_unc,'','','','',int(len(lcs)*.5),plotUncertainty=False,model_name="EMPIRICAL")
#AR_cycle.plot('ACC',m,acc,acc_unc,'','','','',int(len(acc)*.5),plotUncertainty=False,model_name="EMPIRICAL")