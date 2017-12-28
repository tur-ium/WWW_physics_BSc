# -*- coding: utf-8 -*-
"""
Breadth-First Search
"""
import numpy as np
import network_toolkit as nt   #I'm putting our tools for network analysis here
import networkx
epsilon = 2**-10               #Small value for float comparison

adjMatrix = [[]]
def shortestPath(vertices,adjMatrix,root,j=None):
    '''Finds the shortest path length from i to node `j` in the network. If `j` is\
None returns a list of the shortest path lengths for every node in the network
    PARAMETERS
    ---
    vertices: list 
        List of labels for each vertex. The order must be the same as the order\
columns in the adjacency matrix
    adjMatrix: np.ndarray
        Adjacency Matrix
    root: int
        index of the node from which we are measuring distances
    j: int (default: None)
        Node we are measuring distances to. If None return a list containing \
the shortest path lengths for every node in the network
    RETURNS
    ---
    shortestPathTree: list of tuples
        A representation of the shortest path FROM each node in the network TO\
the root node
'''
    #SANITATION:
    #TODO:
    
    #MAIN METHOD:
    n = adjMatrix.shape[0]   #Number of nodes in network    
    distances = [-1 for i in range(n)]   #Create fixed length array of length n. -1 indicates distance is no known path from that node
    buffer = [None for i in range(n)]   #Buffer, each element is a label of a node in the network
    shortestPathTree = list()   #Returned as a list of tuples [(from, to)]
    
    buffer[0] = vertices.index(root)   #Place the index of the root vertex in the buffer
    read_posn = 0   #Set the read pointer to it
    write_posn = 1   #Set the write pointer to the second element in the buffer
    distances[0] = 0   #Set the distance of the root vertex to 0
    
    d = 0  #Current distance from i
    while write_posn != read_posn:
        #When the write position is the same as the read position, we are finished
        
        k = buffer[read_posn]   #Index of current node of consideration
        klabel = vertices[k]   #Label of current node of consideration
        d = distances[k]   #Current distance of k from root
        print(k)
        if klabel==14:
            raise Exception('Non-existent vertex. Buffer: {}'.format(buffer))
            break
        for m in range(n):   #Get each edge in the network
            #m is the INDEX of the vertex under consideration
#            print('k:{}, m: {}'.format(k,m))
#            print('Write posn: {}'.format(write_posn))
#            print('Distances: {}'.format(distances))
            mlabel = vertices[m]   #LABEL of the vertex under consideration
            edge_weight = adjMatrix[k,m]
            if abs(edge_weight - 1) < epsilon:
                #There is a path from k to m
                if distances[m]==-1:
                    distances[m] = d+1
                    buffer[write_posn] = m
                    shortestPathTree.append((mlabel,klabel))
                    write_posn += 1
                
#                if distances[k]==d:
                    #Code for shortest path logging here
                    #TOD0
#                    print('Something different would happen here if you wanted the shortest paths themselves')
                if edge_weight not in [0,1]:
                    raise NotImplemented("Weighted networks are not considered")
        #Update variables
        read_posn += 1
        
        
    return (shortestPathTree, distances)
#%%
#TESTING
#Fig. 10.1 example in Newmann
def readData(path,verbose=False):
    lineCounter = 0
    finalData = []
    data = open(path,'r')
    
    print('Loading network of figure 10.1 from Mark Newmans book')
    for line in data:
        
        line = line.replace('\n','')
        line = line.split(",")
        print(line)
        line_data = [int(val) for val in line]
        finalData.append(line_data)
        lineCounter+=1
    
    if verbose:
        print('# of edges: {}'.format(lineCounter))
    
    data.close()   #Close the file
    
    return finalData

dataPath = 'network_fig10-1.csv'


edgeList = readData(dataPath,True)
labelSet, n = nt.getNodeSet(edgeList)  #List of labels on edges
labelList = list(labelSet)
adjMatrix = nt.getAdjacencyMatrix(labelList,edgeList)
sPaths, sPathLengths = shortestPath(labelList,adjMatrix,0)
print('Shortest paths from node `0` are: {}'.format(sPaths))

G = networkx.Graph()
G.add_edges_from(sPaths)
labelDict = dict()
for i in range(len(labelList)):
    labelDict[i] = labelList[i]
networkx.draw(G,labels=labelDict)
