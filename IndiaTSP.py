"""
Data: 08 Sep 2019
Author: Vinay Chourasiya
File: IndiaTSP
"""


#"Require packages"

import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import subprocess
import os
import time



#"Basic Data collection"

df = pd.read_csv('Districts.csv',encoding='ISO-8859-1')
print(df.head())
lat = df['Lat']
long = df['Long']
city = df['District']



#"Data file Preparaion"
def WriteDataFile():
    """
    We try to prepare standard data file
    which is used for directly input for concorde
    solver
    """

    with open("india.tsp",'w') as datafile:
        datafile.write("NAME: IndiaTSP \n")
        datafile.write("TYPE: TSP \n")
        datafile.write("COMMENT: India TSP (district of all states covered) \n")
        datafile.write("DIMENSION: "+str(len(city))+"\n")
        datafile.write("EDGE_WEIGHT_TYPE: GEO \n")
        datafile.write("DISPLAY_DATA_TYPE: COORD_DISPLAY \n")
        datafile.write("NODE_COORD_SECTION \n")
        for i in range(len(city)):
            datafile.write(str(i))
            datafile.write(" "+str(lat[i]))
            datafile.write(" "+str(long[i]))
            datafile.write("\n")




#"TSP tour generation using concorde solver"
def GenerateTour():
    cmd = "LINKERN/linkern  -Q -o india.out india.tsp"
    results = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
    # Pausing for running the LINKERN algo 
    time.sleep(2)




def Read_n_Plot():
    #--------reading out file--------  
    with open("india.out") as f:
        data = []
        for l in f:
            temp1 = l.split()
            data.append([int(i) for i in temp1])
    if len(data[0])<3:
        del data[0]
    datanp = np.array(data)
    Edges = datanp[:,:-1] 
    # -------"ploting"-----------
    
    D = nx.DiGraph()
    for i in range(len(city)):
        D.add_node(i,pos = (lat[i],long[i]))
    for e in Edges:
        D.add_edge(*e)

    plt.figure(figsize=(15, 13))
    pos=nx.get_node_attributes(D,'pos')
    nx.draw(D,pos,node_size=10,node_color="black", edge_color="blue")
    plt.savefig("indiatspmap1.png")




def Cleaning():
    """
    Removing temporary files that generate 
    during the execution
    """
    os.remove("india.out")
    os.remove("india.tsp")


def MainAlgo():
    """
    Running the complete programme
    """
    WriteDataFile()
    GenerateTour()
    Read_n_Plot()
    Cleaning()

MainAlgo()

