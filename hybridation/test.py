# from Benchmark import test_RS
# from RS import tspSimulatedAnnealing
import math 
from hyb import *
import itertools
import tsplib95
import time
import numpy as np
import pandas as pd
import csv
import matplotlib.pyplot as plt

INF = 99999999  # * math.inf

# ? Fill the inexisting arcs with INF


def transform_garph(G, accept_zeros=True):
    n = len(G)
    for i in range(n):
        for j in range(n):
            if (G[i][j] == 0 and not accept_zeros):
                G[i][j] = INF
            if i == j:
                G[i][j] = INF

# ? Load a tsplib benchmark
def load_benchmark(file_name):
    problem = tsplib95.load(file_name)
    tmp = problem.edge_weights
    G = []
    for i in range(len(tmp)):
        for j in range(len(tmp[i])):
            G.append(tmp[i][j])
    G = np.array(G).reshape((-1, problem.dimension))
    # print(f"\nProblem size {problem.dimension}  G.shape={G.shape}  \n G = {G}")
    return G, problem.dimension





# Line plot :  Performances variation as function of one paramter  
def plot_line(x,y,xlabel,ylabel,title,pngfile,show = False):
    plt.clf()
    plt.plot(x, y)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.savefig(pngfile)
    if(show):
        plt.show()

def test_RD_plot_line(
        benchmarks ,  # List of benchmarks to test on 
        params, # Parameters values 
        file_name ,
        nb_executions =1,  # NB exectuion with the same combination
        param_name = "N",  # Parameter Name 
        plot=False,  # Generate a line plot 
        plot_name = './results/plot'
    ):

    combinations = list(itertools.product( params["N"], params["delta"], 
                                        params["y"],params["alpha"],params["beta"],
                                        params["nb_iteration"],params["algo_generation"],params["initialTemperature"],
                                        params["coolingRate"],params["nbIterationsRS"],params["nbIterationsHC"],
                                        params["nbIterationsCooling"],params["selectionAlgorithme"]))
    
    # ? File to write the results on 
    # ? File to save the results
    results = open(file_name, 'w', newline='')
    writer = csv.writer(results)
    headers = ["Benchmark name","N","delta", 
                "y","alpha","beta",
                "nb_iteration","algo_generation","initialTemperature",
                "coolingRate","nbIterationsRS","nbIterationsHC",
                "nbIterationsCooling","selectionAlgorithme",
                "Average %","Min result","NB opt","Average execution time (s)"]
    writer.writerow(headers)
    
    # ? For line plotting 
    plot_data = {}


    # ? Loading the tsplib benchmarks list
    benchs = pd.read_csv('./Benchs/ref.csv')
    for bench_name, bench_size, bench_opt in zip(benchs["name"], benchs["nb_nodes"], benchs["OPT"]):
        if bench_name in benchmarks:

            # ? Loading the benchmark  
            try:
                G, n = load_benchmark(f"./Benchs/{bench_name}.atsp")
            except:
                print(f"Unable to load {bench_name}")
                continue
            
            transform_garph(G, True)
            print(f"\n Benchmark :  {(bench_name,bench_size,bench_opt)} : ")
            
            plot_data[bench_name] = {
                "x" : [],
                "y" : []
            }

            for combination in combinations:
                (N,delta,y,alpha,beta,nb_iteration,algo_generation,initialTemperature,coolingRate,nbIterationsRS,nbIterationsHC,nbIterationsCooling,selectionAlgorithme) = combination
                print("      Params : ",end =' ')
                print((N,delta,y,alpha,beta,nb_iteration,algo_generation.__name__,initialTemperature,coolingRate,nbIterationsRS,nbIterationsHC,nbIterationsCooling,selectionAlgorithme.__name__))     
                cumul_time = 0
                cumul_result = 0
                min_result = INF 
                nb_opt = 0

                for i in range(nb_executions):
                    start = time.time()
                    opt_circuit,opt_cost  = RED_DEERS_RS(
                                G,
                                N,
                                delta,
                                y,
                                alpha,
                                beta,
                                nb_iteration,
                                algo_generation,
                                initialTemperature,
                                coolingRate,
                                nbIterationsRS,
                                nbIterationsHC,
                                nbIterationsCooling,
                                selectionAlgorithme,
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
                writer.writerow([bench_name,N,delta,y,alpha,beta,nb_iteration,algo_generation.__name__,initialTemperature,coolingRate,nbIterationsRS,nbIterationsHC,nbIterationsCooling,selectionAlgorithme.__name__,"%.3f" % avg_perc,min_result,nb_opt,"%.4f" % avg_time])

                if (param_name == 'selectionAlgorithme'):
                    plot_data[bench_name]["x"].append(locals()[param_name].__name__)
                else:
                    plot_data[bench_name]["x"].append(locals()[param_name])
                plot_data[bench_name]["y"].append(avg_perc)

                print("      Results : ",end=' ')
                print((avg_result,avg_time,avg_perc))
                print(" ")
            
            # ? Plotting for the benchmark 
            if(plot):
                plot_line(plot_data[bench_name]["x"],plot_data[bench_name]["y"],param_name,"Bench :"+bench_name+" Result (%)",f"Result = f ({param_name})",plot_name+"_"+bench_name+".png",show=False)

    print(plot_data)

    results.close()
    
    return 




BENCHMARKS_NAMES  = ["ftv33","ftv38","ftv44","ftv47","ft53","ftv55","ftv70","ftv90","ftv170","rbg443","rbg403","rbg358","rbg323","kro124p","ftv170"]
SELECTION_METHODS = [SEL_ROULETTE,SEL_RANKING,SEL_ELITISTE,SEL_TOURNAMENT,SEL_RANDOM]
#! SEL_RANDOM : not working correctly 
# -AVG_DELTA/math.log(p)
AVG_DELTA = {
    "krop124p": 4500,
    "ftv170":500
}



if  __name__ == "__main__" :
    
    benchmarks = ["rbg443","rbg403","rbg358","rbg323","kro124p","ftv170"]
    params = {
            "N" : [100],          # Population size 
            "delta" : [0.25],       # Percentage of males  
            "y"  : [0.7],              # Percentage of commanders
            "alpha" : [0.7],          # Percentage of crossover within the harem 
            "beta": [0.5],           # Percentage of crossover with others the harem 
            "nb_iteration" : [500],   # Number of iterations  
            "algo_generation" : [RAI],  # Algo of generation of initiale solution 
            "initialTemperature" : [10000],  # RS Param : initiale Temperature 
            "coolingRate" : [0.92],        # RS Param :  cooling rate
            "nbIterationsRS":[200],    # RS Param : number of iterations 
            "nbIterationsHC": [100],    # Number of itertions Hill climbing 
            "nbIterationsCooling" : [1],  # RS Param : Number of itertion with the same cooling rate 
            "selectionAlgorithme" : [SEL_ELITISTE], # Selection algorithm
    }

    #? For a line plot (perfs = f(param_name)) 
    #? Only the concerned param should have multpile values , other parameters must have a single value in the params object 
    test_RD_plot_line(benchmarks,params,file_name = './results/RD_test_ouss.csv',nb_executions = 1,
            param_name = "N",plot = True,plot_name='./results/RD_test_ouss_plot')
