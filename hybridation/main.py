from Benchmark import *
import time
import numpy as np
import sys


from hyb import *

if __name__ == "__main__":

    N = 50
    delta = 0.5
    y = 0.5
    alpha = 0.5
    beta = 0.3
    nb_iteration = 1000
    algo_generation = PPV
    cooling_rate = 0.9
    initialTemperature = 80.0
    coolingRate = 0.9
    nbIterationsRS = 200
    nbIterationsHC = 200
    nbIterationsCooling = 10
    selectionAlgorithme = SEL_ELITISTE

    def callerHYB(
        graph,
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
    ): return RED_DEERS_RS(
        graph,
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

    test_algorithm(callerHYB,
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
                   max_nodes=200, nb_executions=1,
                   filename='./results/RED_DEERS_RS_result.csv')
