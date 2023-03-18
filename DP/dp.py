import itertools
import random
import sys

import tsplib95
import time
import numpy as np

def heldKarp(dists):
    n = len(dists)  # Get the number of nodes
    print(n)
    C = {}  # Create an empty dictionary to store the results

    # Calculate the cost of traveling from node 0 to node k for all k
    for k in range(1, n):
        C[(1 << k, k)] = (dists[0][k], 0)
    # print(C)
    # Calculate the cost of traveling to each subset of nodes of size 2 to n-1
    for subset_size in range(2, n):
        for subset in itertools.combinations(range(1, n), subset_size):
            # print(subset)
            bits = 0
            for bit in subset:
                bits |= 1 << bit  # Create a bit mask for the subset of nodes
            # print(bin(bits))
            # Find the lowest cost to get to this subset
            for k in subset:
                prev = bits & ~(1 << k)

                res = []
                for m in subset:
                    if m == 0 or m == k:
                        continue
                    res.append((C[(prev, m)][0] + dists[m][k], m))
                C[(bits, k)] = min(res)  # Store the lowest cost in the dictionary

    bits = (2**n - 1) - 1

    res = []
    for k in range(1, n):
        res.append((C[(bits, k)][0] + dists[k][0], k))
    opt, parent = min(res)

    # Find the optimal path by backtracking through the results
    path = []
    for i in range(n - 1):
        path.append(parent)
        new_bits = bits & ~(1 << parent)
        _, parent = C[(bits, parent)]
        bits = new_bits

    path.append(0)

    return opt, list(reversed(path))

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


if __name__ == '__main__':
    G = load_benchmark("./benchmarks/ft53.atsp")
    n = 13      #* Nombre de sommets a utiliser du graph  G
    start = time.time()
    print(f" Les résultats de la recherche : {heldKarp(G[:n][:n])}")
    end = time.time()
    print("\nLe temps d'éxecution est : "+str(end - start)+"s")

