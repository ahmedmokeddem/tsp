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



def plot_line(x,y,xlabel,ylabel,title,pngfile,show = False):
    plt.plot(x, y)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.savefig(pngfile)
    if(show):
        plt.show()


# Line plot :  Performances variation as function of one paramter  

def test_RD(
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
            print(f" Benchmark :  {(bench_name,bench_size,bench_opt)} : ")
            
            plot_data[bench_name] = {
                "x" : [],
                "y" : []
            }

            for combination in combinations:
                (N,delta,y,alpha,beta,nb_iteration,algo_generation,initialTemperature,coolingRate,nbIterationsRS,nbIterationsHC,nbIterationsCooling,selectionAlgorithme) = combination
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
            
            # ? Plotting for the benchmark 
            if(plot):
                plot_line(plot_data[bench_name]["x"],plot_data[bench_name]["y"],param_name,"Bench :"+bench_name+" Result (%)",f"Result = f ({param_name})",plot_name+"_"+bench_name+".png",show=False)

    print(plot_data)

    results.close()
    
    return 


# Contour Plot   :  evolution of two parameters 


BENCHMARKS_NAMES  = []


if  __name__ == "__main__" :
    benchmarks = ["ftv33","ftv38","ftv44","ftv47","ft53","ftv55","ftv70","ftv90","ftv170"]
    params = {
            "N" : [50,100],          # Population size 
            "delta" : [0.4],       # Percentage of males  
            "y"  : [0.3],              # Percentage of commanders
            "alpha" : [0.5],          # Percentage of crossover within the harem 
            "beta": [0.3],           # Percentage of crossover with others the harem 
            "nb_iteration" : [200],   # Number of iterations  
            "algo_generation" : [PPV],  # Algo of generation of initiale solution 
            "initialTemperature" : [1150],  # RS Param : initiale Temperature 
            "coolingRate" : [0.92],        # RS Param :  cooling rate
            "nbIterationsRS":[200],    # RS Param : number of iterations 
            "nbIterationsHC": [200],    # Number of itertions Hill climbing 
            "nbIterationsCooling" : [1],  # RS Param : Number of itertion with the same cooling rate 
            "selectionAlgorithme" : [SEL_ELITISTE], # Selection algorithm
    }

    test_RD(benchmarks,params,'./results/RD_test_ouss.csv',1,"N",True,'./results/RD_test_ouss_plot')









    # benchmark = "ft53"
    # p_values = [0.66 for i in range(50)]
    # values_cooling_rate = [ 0.65]
    # values_initial_temperature = [-AVG_DELTA/math.log(p) for p in p_values]
    # values_num_iteration =[200000]
    # values_nb_iterations_cooling =[1]


    # #! change file name 
    # filename = './results/ouss/Opt_test_rand.csv'
    # test_RS(benchmark,values_initial_temperature, values_cooling_rate, values_num_iteration, values_nb_iterations_cooling ,filename,nb_executions=5)
    # # plot_line('NB Iterations','average %',filename,'./results/ouss/plots/Test_NB_iter_0.66_0.65.png')
    # # contour_plot('Initiale Temperature','Cooling Rate','average %',filename,'./results/ouss/plots/Step1_test_8.png')


