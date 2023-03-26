from RAI import * 
from Benchmark import *
import time
import numpy as np
import sys
from greedy import construct_tour


if  __name__ == "__main__" :
    
    #? Call this function to test your algorithm on all the tsplib benchmarks 
    caller = lambda G : RAI(G) #* put the call to ur algorithm here
    callerG = lambda G : construct_tour(G)
    #! This function will test the algorithm only on the benchmarks that contain less than max_nodes node 
    #test_algorithm(caller,max_nodes=200,nb_executions=10,filename='./results/RAI_Benchmarks_MAX_200_nodes.csv') 
    test_algorithm(callerG,max_nodes=200,nb_executions=10,filename='./results/Greedy_Benchmarks_MAX_200_nodes.csv') 

    # #! For test : Don't modify the call for G 
    # G,n = load_benchmark("./Benchs/br17.atsp")
    # # n = 13      #* Size of graph G
    # A = 0       #* Starting point 
    # start = time.time()
    # transform_garph(G,True) #* To replace all the zeros in the graph with math.inf
    # #! np.set_printoptions(threshold=sys.maxsize) 
    # print(G[:n,:n])
    # print(f" Les résultats de la recherche : {RAI(G[:n,:n])}")
    # end = time.time()
    # print("\nLe temps d'éxecution est : "+str(end - start)+"s")
