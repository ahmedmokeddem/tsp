from BB import *
import tsplib95
import time
import numpy as np

# ? Tested benchmarks : br17.atsp, ft53.atsp, ftv33.atsp, ftv38.atsp

#? Fonction pour chargement des benchmark de tsplib 
def load_benchmark(file_name):
    problem = tsplib95.load(file_name)
    tmp = problem.edge_weights
    G = []
    for i in range(len(tmp)):
        for j in range(len(tmp[i])):
            G.append(tmp[i][j])
    G = np.array(G).reshape((-1, problem.dimension))
    print(f"\nProblem size {problem.dimension}  G.shape={G.shape}  \n G = {G}")
    return G


#? Test 

G = load_benchmark("./benchmarks/ft53.atsp")
n = 10      #* Nombre de sommets a utiliser du graph  G
A = 0       #* Le point de départ
start = time.time()
print(f" Les résultats de la recherche : {BB(G[:n][:n], A, n)}")
end = time.time()
print("\nLe temps d'éxecution est : "+str(end - start)+"s")
