#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 26 17:50:01 2018

@author: RamanSB
"""

import measure_new as mn
import networkx as nx
import numpy as np
from matplotlib import pyplot as plt

def loadGEXF(gexfFile):
    return nx.gexf.read_gexf(gexfFile)


BA_FilePath = "/Users/RamanSB/Documents/University/3rd-Year Physics/3rd Year Project/GeneratedData/GEXFs/BA/1GEXF.gexf"
R_0_FilePath = "/Users/RamanSB/Documents/University/3rd-Year Physics/3rd Year Project/GeneratedData/GEXFs/p=0/1GEXF"
R_025_FilePath = "/Users/RamanSB/Documents/University/3rd-Year Physics/3rd Year Project/GeneratedData/GEXFs/p=0.25/0GEXF"
R_05_FilePath = "/Users/RamanSB/Documents/University/3rd-Year Physics/3rd Year Project/GeneratedData/GEXFs/p=0.5/0GEXF.gexf"
R_075_FilePath = "/Users/RamanSB/Documents/University/3rd-Year Physics/3rd Year Project/GeneratedData/GEXFs/p=0.75/0GEXF"
R_1_FilePath = "/Users/RamanSB/Documents/University/3rd-Year Physics/3rd Year Project/GeneratedData/GEXFs/p=1/0GEXF"
C_FilePath = "/Users/RamanSB/Documents/University/3rd-Year Physics/3rd Year Project/GeneratedData/GEXFs/Configurational/configuration.gexf"

R_0_G = loadGEXF(R_0_FilePath)
R_025_G = loadGEXF(R_025_FilePath)
R_05_G = loadGEXF(R_05_FilePath)
R_075_G = loadGEXF(R_075_FilePath)
R_1_G = loadGEXF(R_1_FilePath)
C_G = loadGEXF(C_FilePath)
BA_G = loadGEXF(BA_FilePath)
ER_G = loadGEXF("/Users/RamanSB/Documents/University/3rd-Year Physics/3rd Year Project/Github Repository/WWW_Physics BSc/WWW_physics_BSc/results/erdos-renyi/final_network_files/erdos-renyi_GraphV=66626N=23396-0.gexf")
ActivityFilePath = "/Users/RamanSB/Documents/University/3rd-Year Physics/3rd Year Project/Real Data/TimeSlicedData/WeightedNetwork/WeightedNetwork/2008/2008_DEC_WeightedGraph.gexf"
AN = loadGEXF(ActivityFilePath)

ER_DegreeDict = mn.getDegreeDist(ER_G)
AN_DegreeDict = mn.getDegreeDist(AN)
C_DegreeDict = mn.getDegreeDist(C_G)
R_0_DegreeDict = mn.getDegreeDist(R_0_G)
R_025_DegreeDict = mn.getDegreeDist(R_025_G)
R_05_DegreeDict = mn.getDegreeDist(R_05_G)
R_075_DegreeDict = mn.getDegreeDist(R_075_G)
R_1_DegreeDict = mn.getDegreeDist(R_1_G)
BA_DegreeDict = mn.getDegreeDist(BA_G)

mn.plot_distribution(AN_DegreeDict, C_DegreeDict, "Configurational")

