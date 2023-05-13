
from Benchmark import test_algorithm
from RS import tspSimulatedAnnealing
if  __name__ == "__main__" :

    initial_temperature = 1000.0
    cooling_rate = 0.9
    num_iterations = 100000
    num_iterations_for_cooling = 10


    #? Call this function to test your algorithm on all the tsplib benchmarks 
    caller = lambda G, initial_temperature, cooling_rate, num_iterations, initial_solution, intial_cost : tspSimulatedAnnealing(G,
        initial_temperature,
        cooling_rate,
        num_iterations,
        num_iterations_for_cooling,
        initial_solution,
        intial_cost)

    #! This function will test the algorithm only on the benchmarks that contain less than max_nodes node
    test_algorithm(caller,initial_temperature, cooling_rate, num_iterations,max_nodes=200,nb_executions=10,filename='./results/Default_RS_TMP_1000.csv')

