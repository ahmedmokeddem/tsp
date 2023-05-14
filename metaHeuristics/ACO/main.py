from Benchmark import test_algorithm
from ACO import ACO


if __name__ == "__main__":

    NB_ITER = 100
    SIGMA0 = 0.1
    ALPHA = 1

    BETA = 5
    Q = 50
    P = 0.5

    # ? Call this function to test your algorithm on all the tsplib benchmarks

    def caller(G, SIGMA0, ALPHA, BETA, Q, P, NB_ITER): return ACO(
        G, SIGMA0, ALPHA, BETA, Q, P, NB_ITER)

    #! This function will test the algorithm only on the benchmarks that contain less than max_nodes node
    test_algorithm(caller, SIGMA0, ALPHA, BETA, Q, P, NB_ITER,
                   max_nodes=200, nb_executions=50, filename='./results/Default_ACO.csv')
