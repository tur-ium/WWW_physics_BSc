# -*- coding: utf-8 -*-
"""
Created on Wed Mar 14 12:56:04 2018

@author: admin
"""
import AR_cycle   #This contains the plotting function

V = 66626  #Parameters for loading data
N = 23396  #Parameters for loading data
s = 100
iterations = 20

models =['erdos-renyi','configurational','R_model','BA']

#SHORT CODES FOR EACH model
ER = 0
CONFIG = 1
R = 2
BA = 3

model = models[CONFIG]
data_dir = '../results/'

filePath_model = data_dir+'/{}/raw/{}_ResultsV={}N={}.csv'.format(model,model,V,N)
filePath_ER = data_dir+'erdos-renyi/raw/erdos-renyi_Results_stepsize100_combined.csv'

def loadData(filePath,empirical):
    '''Load data from filePath
    If empirical, use empirical=True
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
m,lcs,lcs_unc,acc,acc_unc=loadData(filePathAddition,True)
filePathRemoval = data_dir+'empirical_activity/raw/empirical_removing_2008_DEC_step_100.csv'
m_r,lcs_r,lcs_unc_r,acc_r,acc_unc_r=loadData(filePathRemoval,True)
#m,lcs,lcs_unc,acc,acc_unc=loadData(filePath_empirical,False)   #Uncomment for empirical

#%%
m.extend(m_r)
lcs.extend(lcs_r)
acc.extend(acc_r)
lcs_unc.extend(lcs_unc_r)
acc_unc.extend(acc_unc_r)
model = 'empirical'
#Plot model
AR_cycle.plot('LCS',m,lcs,lcs_unc,V,N,s,iterations,int(len(lcs)*.5),plotUncertainty=True,model_name='Erdos-Renyi')
AR_cycle.plot('ACC',m_r,acc_r,acc_unc_r,V,N,s,iterations,int(len(acc)*.5),plotUncertainty=True,model_name='Erdos-Renyi')
