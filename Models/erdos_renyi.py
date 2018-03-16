# Erdos-Renyi /Solomoff-Rapoport random network model

import networkx_extended as nx
import random

class Erdos_Renyi():
    '''An Erdos-Renyi / Solomonoff-Rapoport random network model'''
    def __init__(self,node_list):
        '''Initiate an Erdos-Renyi graph with a given degree distribution'''
        self.node_list = node_list
        self.G = nx.Graph()
        self.G.add_nodes_from(self.node_list)
        pass
    def iterate(self):
        from_user = random.choice(self.node_list)
        to_user = random.choice(self.node_list)
        if not self.G.has_edge(from_user,to_user):
            self.G.add_edge(from_user,to_user)
            self.G[from_user][to_user]['weight'] = 1
        else:
            self.G[from_user][to_user]['weight'] += 1