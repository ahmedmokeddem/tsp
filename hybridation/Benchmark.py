import tsplib95
import time
import numpy as np
import pandas as pd
import csv

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


def test_algorithm(aglorithm, N,
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
                   max_nodes=200, nb_executions=1,
                   filename='./results/RED_DEERS_RS_result.csv'):
    """
        algorithm : The algorithm to Test 
        max_nodes : the maximum size of a graph
        nb_executions : number of execution of the algorithm on each bechmark  
        filename : where to store the results 
    """
    # ? Loading the tsplib benchmarks list
    benchs = pd.read_csv('./Benchs/ref.csv')

    # ? File to save the results
    results = open(filename, 'w', newline='')
    writer = csv.writer(results)
    headers = ["Benchmark name", "Size", "OPT", "average result",
               "average %", "min result", "nb opt", "average execution time (s)"]
    writer.writerow(headers)
    results_path = open("path.csv", 'w', newline='')
    writer_path = csv.writer(results_path)
    headers_path = ["Bench Name", "Path", "Cost", "Path_Length"]
    writer_path.writerow(headers_path)

    for bench_name, bench_size, bench_opt in zip(benchs["name"], benchs["nb_nodes"], benchs["OPT"]):
        if (bench_size <= max_nodes):
            try:
                G, n = load_benchmark(
                    f"./Benchs/{bench_name}.atsp")
            except:
                print(f"Unable to load {bench_name}")
                continue
            print(f" Benchmark :  {(bench_name,bench_size,bench_opt)} :",)
            A = 0  # *
            cumul_time = 0
            cumul_result = 0
            min_result = INF
            min_opt = []
            nb_opt = 0
            # list of benchmarks that accepts 0 as cost between two nodes
            if (bench_name in ['br17', "p43", 'ftv90']):
                transform_garph(G, True)
            else:
                transform_garph(G, False)
            # * Executing the algorithm nb_executions times on the benchmark
            for i in range(nb_executions):
                print("[{}>]".format("="*i))
                start = time.time()
                opt_circuit, opt_cost = aglorithm(
                    G, N,
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
                    selectionAlgorithme)
                end = time.time()
                cumul_time += end-start
                if opt_cost is not None:
                    cumul_result += opt_cost

                    if (opt_cost < min_result):
                        min_opt = opt_circuit.copy()
                        min_result = opt_cost
                    if (opt_cost == int(bench_opt)):
                        nb_opt += 1
            # * Writing the results to the file
            avg_result = cumul_result / nb_executions
            avg_time = cumul_time / nb_executions
            avg_perc = abs(bench_opt-avg_result)/bench_opt * 100
            writer.writerow([bench_name, bench_size, bench_opt, avg_result,
                            "%.3f" % avg_perc, min_result, nb_opt, "%.4f" % avg_time])
            writer_path.writerow(
                [bench_name, min_opt, min_result, len(min_opt)])

    results.close()
