import tsplib95
import time
import numpy as np
import pandas as pd
import csv
from greedy import greedy
import pandas as pd
import matplotlib.pyplot as plt
import itertools
from RS import tspSimulatedAnnealing ,tspSimulatedAnnealing_recording_delta
from RAI import RAI
from PPV import PPV
from NI import NI
# ? Tested benchmarks : br17.atsp, ft53.atsp, ftv33.atsp, ftv38.atsp
from RS import constructPathForGreedy,calculatePathDistance
import random

INF = 99999999 #* math.inf

#? Fill the inexisting arcs with INF 
def transform_garph(G,accept_zeros = True):
    n = len(G)
    for i in range(n):
        for  j in range(n):
            if(G[i][j]==0 and not accept_zeros): 
                G[i][j] = INF
            if i==j:
                G[i][j] = INF

#? Load a tsplib benchmark 
def load_benchmark(file_name):
    problem = tsplib95.load(file_name)
    tmp = problem.edge_weights
    G = []
    for i in range(len(tmp)):
        for j in range(len(tmp[i])):
            G.append(tmp[i][j])
    G = np.array(G).reshape((-1, problem.dimension))
    # print(f"\nProblem size {problem.dimension}  G.shape={G.shape}  \n G = {G}")
    return G,problem.dimension



def test_algorithm(aglorithm,initial_temperature, cooling_rate, num_iterations, max_nodes=1000,nb_executions=1,filename='./results/results.csv'):
    """
        algorithm : The algorithm to Test 
        max_nodes : the maximum size of a graph
        nb_executions : number of execution of the algorithm on each bechmark  
        filename : where to store the results 
    """
    #? Loading the tsplib benchmarks list 
    benchs = pd.read_csv('../../Heuristics/Benchs/ref.csv')

    #? File to save the results
    results = open(filename, 'w',newline='')
    writer = csv.writer(results)
    headers = ["Benchmark name","Size","OPT","average result","average %","min result","nb opt","average execution time (s)"]
    writer.writerow(headers)

    for bench_name,bench_size,bench_opt in zip(benchs["name"],benchs["nb_nodes"],benchs["OPT"]):
        if(bench_size<=max_nodes):
            try:
                G,n = load_benchmark(f"../../Heuristics/Benchs/{bench_name}.atsp")
            except:
                print(f"Unable to load {bench_name}")
                continue
            print(f" Benchmark :  {(bench_name,bench_size,bench_opt)} :",)
            A = 0  #* 
            cumul_time = 0
            cumul_result = 0
            min_result = INF 
            nb_opt = 0
            if(bench_name in ['br17',"p43",'ftv90']): #list of benchmarks that accepts 0 as cost between two nodes 
                transform_garph(G,True)
            else:
                transform_garph(G,False)
            for i in range(nb_executions): #* Executing the algorithm nb_executions times on the benchmark
                print("[{}>]".format("="*i))
                start = time.time()
                
                initial_solution, intial_cost = greedy(G)
                initial_solution = constructPathForGreedy(initial_solution)
                opt_circuit,opt_cost = aglorithm(G,initial_temperature, cooling_rate, num_iterations, initial_solution, intial_cost)
                end = time.time()
                cumul_time += end-start
                if opt_cost is not None:
                    cumul_result += opt_cost
                    if(opt_cost<min_result):
                        min_result = opt_cost
                    if(opt_cost == int(bench_opt)):
                        nb_opt+=1
            #* Writing the results to the file 
            avg_result = cumul_result / nb_executions
            avg_time = cumul_time / nb_executions
            avg_perc = abs(bench_opt-avg_result)/bench_opt *100 
            writer.writerow([bench_name,bench_size,bench_opt,avg_result,"%.3f" % avg_perc,min_result,nb_opt,"%.4f" % avg_time])


    results.close()



# test the algorithm on one becnhmark 
# provid a list for each paramter 
def test_RS(benchmark,values_initial_temperature, values_cooling_rate, values_num_iteration, values_nb_iterations_cooling ,filename='./results/results.csv',nb_executions=1):
    """
        max_nodes : the maximum size of a graph
        nb_executions : number of execution of the algorithm on each bechmark  
        filename : where to store the results 
    """
    #? Loading the tsplib benchmarks list 
    benchs = pd.read_csv('../../Heuristics/Benchs/ref.csv')

    #? File to save the results
    results = open(filename, 'w',newline='')
    writer = csv.writer(results)
    headers = ["Initiale Temperature","Cooling Rate","NB Iterations","NB Iterations cooling","average %","min result","nb opt","average execution time (s)","Average init"]
    writer.writerow(headers)

    for bench_name,bench_size,bench_opt in zip(benchs["name"],benchs["nb_nodes"],benchs["OPT"]):
        if(bench_name==benchmark):
            
            #* Loading the becnhmark
            try:
                G,n = load_benchmark(f"../../Heuristics/Benchs/{bench_name}.atsp")
            except:
                print(f"Unable to load {bench_name}")
                exit(-1)
            print(f" Benchmark :  {(bench_name,bench_size,bench_opt)} :",)
            A = 0  #* 

            if(bench_name in ['br17',"p43",'ftv90']): #list of benchmarks that accepts 0 as cost between two nodes 
                transform_garph(G,True)
            else:
                transform_garph(G,False)
            
            print(G)
            


            for tmp in list(itertools.product(values_initial_temperature, values_cooling_rate, values_num_iteration,values_nb_iterations_cooling)):
                print(tmp)
                cumul_time = 0
                cumul_result = 0
                min_result = INF 
                nb_opt = 0
                cmul_init =0 

                for i in range(nb_executions):
                    start = time.time()
                    # initial_solution, intial_cost = greedy(G)
                    # initial_solution = constructPathForGreedy(initial_solution)
                    # initial_solution, intial_cost = RAI(G,0)
                    # initial_solution, intial_cost = PPV(G) # Test 
                    # initial_solution, intial_cost = NI(G)

                    # # Random init
                    n = len(G)
                    initial_solution = random.sample(range(n), n) 
                    intial_cost = calculatePathDistance(G,initial_solution)
                    cmul_init +=intial_cost 

                    opt_circuit,opt_cost = tspSimulatedAnnealing(
                        G,
                        tmp[0],
                        tmp[1],
                        tmp[2],
                        tmp[3],
                        initial_solution,
                        intial_cost,
                    )


                    end = time.time()
                    cumul_time += end-start
                    if opt_cost is not None:
                        cumul_result += opt_cost
                        if(opt_cost<min_result):
                            min_result = opt_cost
                        if(opt_cost == int(bench_opt)):
                            nb_opt+=1

                avg_result = cumul_result / nb_executions
                avg_time = cumul_time / nb_executions
                avg_perc = abs(bench_opt-avg_result)/bench_opt *100 
                avg_init = abs(bench_opt-cmul_init / nb_executions)/bench_opt *100  
                writer.writerow([tmp[0],tmp[1],tmp[2],tmp[3],"%.3f" % avg_perc,min_result,nb_opt,"%.4f" % avg_time,"%.4f" % avg_init])




    results.close()





