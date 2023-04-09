#from Benchmark import *
import random
INF = 99999999


def NN(G, A, S):  # le plus proche voisin de A parmi les noeuds sauf les noeud de S dans le Graphe G
    #  G : le graph
    #  A : le point de départ
    #  S : l'ensemble des points exclu
    min_cost = INF
    nearest_neighbor = -1
    for neighbor in range(len(G[A])):
        if neighbor not in S and G[A][neighbor] < min_cost:
            min_cost = G[A][neighbor]
            nearest_neighbor = neighbor
    return min_cost, nearest_neighbor


def PPV(G):
    # ? G : le graph
    # ? A : le point de départ
    first_node = random.randint(0, len(G)-1)
    S = [first_node]
    print(first_node)
    cost_to_neighbor = -1
    nearest_neighbor = -1
    min_cost = 0
    min_path = []
    min_path.append(first_node)
    while len(min_path) < len(G):
        cost_to_neighbor, nearest_neighbor = NN(G, min_path[-1], S)
        S = min_path[:]
        if cost_to_neighbor < INF:     # Cas de l'existance d'un chemin
            min_cost += cost_to_neighbor
            min_path.append(nearest_neighbor)

        else:    # Cas ou le chemin n'existe pas
            if len(min_path) < 2:
                min_cost = -1
                min_path = []
                break  # pas de solution
            S = min_path[:]
            S.remove(S[-2])
            min_cost = min_cost - G[min_path[-2]][min_path[-1]]
            min_path.pop()

        if len(min_path) == len(G):
            if G[min_path[-1]][first_node] < INF:
                min_cost += G[min_path[-1]][first_node]
                min_path.append(first_node)
            else:
                min_path.pop()
                S = min_path[:]
                S.remove(S[-2])
                min_cost = min_cost - G[min_path[-2]][min_path[-1]]
                min_path.pop()
    return min_path, min_cost


G = [[INF, 1, INF, 3],
     [INF, INF, 1, INF],
     [3, INF, INF, INF],
     [INF, 100, INF, INF]]

min_path, min_cost = PPV(G)
print(f"{min_path} --------- {min_cost}")
