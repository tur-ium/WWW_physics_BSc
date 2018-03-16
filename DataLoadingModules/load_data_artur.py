# -*- coding: utf-8 -*-
"""
Created on Wed Mar 14 12:56:04 2018

@author: admin
"""
#import AR_cycle   #This contains the plotting function
from matplotlib import pyplot as plt
V = 66626  #Parameters for loading data
N = 23396  #Parameters for loading data

filePath_empirical = 'results/empirical_activity/raw/empirical_2008_DEC_step_100.csv'
filePath_model = str()   #Defined later
models =['erdos-renyi','configurational']

#SHORT CODES FOR EACH model
ER = 0
CONFIG = 1

#PARAMETERS
model = models[CONFIG]   #CHOOSE MODEL HERE
dataPath = '/Users/RamanSB/Documents/University/3rd-Year Physics/3rd Year Project/Github Repository/WWW_physics_BSc/results'   #path to results directory
#####

filePath_model = '{}/{}/raw/{}_ResultsV={}N={}.csv'.format(dataPath,model,model,V,N)

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

def plot(label,n_list,l_av,l_unc,V,N,stepsize,iterations,c,plotUncertainty=True,model_name=""):
    '''Plot results for the addition and removal of edges on the network
    label: str
        Name of quantity represented
    n_list: list
        Number of edges in the network at each point of calculation
    l_av: list
        Averages
    l_unc: list
        Uncertainties
    V: Total number of edges
    N: Number of nodes
    stepsize: Step size
    iterations: Iterations
    c: Point in the list of calculated edges at which the removal begins
    plotUncertainty: boolean
        If True plot uncertainty on separate axes
    modelName: str
        Name of the model
    '''
    
    fig = plt.figure()
    
    if plotUncertainty:
        layout = 211
    else:
        layout = 111
    
    ax2 = fig.add_subplot(layout)
    ax2.set_title("") #Add Title
    ax2.set_xlabel("Wall posts, m")
    ax2.set_ylabel("{}".format(label))
    ax2.plot(n_list[:-c+1],l_av[:-c+1],label="Adding messages")
    ax2.plot(n_list[-c:],l_av[-c:],label="Removing messages")
    ax2.set_xlim(left=0,right=max(n_list))
    ax2.legend()
    ax2.grid()
    if plotUncertainty:
        ax3 = fig.add_subplot(212)
        ax3.set_title("") #Add Title
        ax3.set_xlabel("Wall posts, m")
        ax3.set_ylabel("$\sigma_{{"+str(label)+"}}$ ")
        ax3.plot(n_list[:-c+1],l_unc[:-c+1],label="Adding messages")
        ax3.plot(n_list[-c:],l_unc[-c:],label="Removing messages")
        ax3.set_xlim(left=0,right=max(n_list))
        ax3.legend()
        ax3.grid()
    fig.tight_layout()
    fig.show()
#%%EXAMPLE
m,lcs,lcs_unc,acc,acc_unc=loadData(filePath_model,False)
#m,lcs,lcs_unc,acc,acc_unc=loadData(filePath_empirical,False)   #Uncomment for empirical

#%%

#Plot model
plot('LCS',m,lcs,lcs_unc,'','','','',int(len(lcs)*.5),plotUncertainty=True,model_name=model)
plot('ACC',m,acc,acc_unc,'','','','',int(len(acc)*.5),plotUncertainty=True,model_name=model)
#Plot empirical
#AR_cycle.plot('LCS',m,lcs,lcs_unc,'','','','',int(len(lcs)*.5),plotUncertainty=False,model_name="EMPIRICAL")
#AR_cycle.plot('ACC',m,acc,acc_unc,'','','','',int(len(acc)*.5),plotUncertainty=False,model_name="EMPIRICAL")