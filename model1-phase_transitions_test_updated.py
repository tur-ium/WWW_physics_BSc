# -*- coding: utf-8 -*-
"""
Created on Tue Feb  6 18:31:50 2018

@author: admin
"""

def calcDelta(network, V=Vmax,mstep=1000):
    N = len(network.nodes())
    node_list = list(network.nodes())
    
    #t0 = last step for which C<√n 
    threshold1 = int(N**.5)
    #t_1   = first step for which C>1/2 n
    threshold2 = int(.5*N)
  
    #ADD EDGES
    m = 0   #Number of edges added
    t0 = 0   #Time to reach threshold 1
    t1 = 0   #Time to reach threshold 2
    while m < V:
        #Draw a directed edge, choosing the start and end nodes according to a 
        # uniform random distribution. Posts made by users on their own wall 
        # appear as self-loops. Multi-edges are allowed.
        from_user = random.choice(node_list)
        to_user = random.choice(node_list)
        network.add_edge(from_user,to_user)
        m+=1
        if m % mstep == 0:
            print('m: {}'.format(m))
            #Find Strongly Connected Components
            SCCs = list(nx.strongly_connected_components(network))   #Strongly Connected Components at time n
            #Calc. size of maxm component
            C = len(max(SCCs,key=len))
            
            if C > threshold1 and t0 == 0:
                #Past threshold 1 for the first time
                t0 = m - 1
                print("PAST THRESHOLD 1, m={}".format(m))
            if C > threshold2 and t0 > 0:
                #Past threshold 1 and threshold 2 for the first time
                t1 = m
                print("PAST THRESHOLD 2, m={}".format(m))
                break
            
            #PRINT STATS
            print("Largest component size: {}".format(C))       
    #Return Delta = t0-tq
    return t1-t0

def test_phase_transition_type(Nlist,Vmax=500000,mstep=1000):
    '''Tests whether the network experiences a continuous or discontinuous phase transition as edges are added
    Nlist: list of ints
        List of Network sizes to use
    Vmax: int (default: 500000)
        Maxm number of edges to add
    msteps: int (default: 1000)
        Number of steps between evalutation of order parameter'''
    delta_list= list()
    for N in Nlist:
        #Begin with an unconnected multidigraph of N nodes. Nodes represent 
        # people and edges represent a wall post by one user on another user’s 
        # wall (edge is from the writer to the user on whose wall the post is 
        # made)
        
        node_list = list(range(N))
        network = nx.MultiDiGraph()
        network.add_nodes_from(node_list)
        
        # Calculate Δ= t_1-t_0 for a range of n
        delta = calcDelta(network,mstep=mstep)
        delta_list.append(delta)
        N += 10000

    #FIT CURVE
    print('FITTING')
    def linear(x,a,b):
        return a*x+b
    
    #LINEAR
    #If Δ is linear in n, System has a 2nd order (continuous) phase transition
    lopt, lcov = optimize.curve_fit(linear,N_list,delta_list)
    l_a, l_b = lopt[0],lopt[1]   #Values of fit
    
    #ERRORS
    a_err = lcov[0,0]**.5
    b_err = lcov[1,1]**.5
    
    #Print fit parameters
    print('Fit params for ax+b: a={:.3g}±{:.3g}, b={:.3g}±{:.3g}'.format(l_a,a_err,l_b,b_err))
    
    #PLOT RESULTS
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(N_list,delta_list,'b-',label='Results')
    ax.plot(N_list,linear(np.asarray(N_list),l_a,l_b),'g--',label='Linear fit')
    ax.set_title('Delta vs. network size, N')
    ax.set_xlabel('N')
    ax.set_ylabel(u'Δ')
    plt.show()