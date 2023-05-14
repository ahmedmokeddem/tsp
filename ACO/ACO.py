import numpy as np
import random
from Benchmark import INF
import math


G = np.array([
    [INF,   6,   INF,  22,   8,   INF,  14,  20],
    [17,   INF,  11,  27,  24,   7,  15,   INF],
    [INF,  16,   INF,  29,   INF,  23,  19,  10],
    [18,  31,  23,   INF,  15,  26,   INF,  12],
    [INF,  14,  24,  16,   INF,  18,  13,   5],
    [INF,  19,  11,  18,  16,   INF,   9,  11],
    [22,  19,  17,   INF,  14,  18,   INF,  12],
    [9,   INF,  22,  17,  13,  14,  10,   INF]])


def Decision(k, i, G, Sigma, alpha, beta, filter):
    g = G[i].copy()
    g[i] = INF
    g[filter] = INF     # eliminer les villes déja selectionné
    if np.min(g) == INF:    # cas de chemin inexistant
        return -1
    new_filter = (g == INF)
    sigma = (Sigma[i]).copy()
    sigma[filter] = 0
    sigma[i] = 0
    tmp = (sigma ** alpha) * ((1/g) ** beta)
    tmp = tmp / np.sum(tmp)
    tmp[new_filter] = -1
    return np.argmax(tmp)


def Evaporation(Delta, Sigma, P):
    Sigma *= (1-P)
    Sigma += Delta
    Delta *= 0.0


def calc_path_cost(G, C):
    # ? G : Graphe
    # ? C : chemin
    tmp = 0
    if (len(C) > 1):
        for i in range(len(C)-1):
            tmp += G[C[i]][C[i+1]]
    return tmp


def ACO(G, sigma0, alpha, beta, q, p, nb_iter):
    nb_town = len(G)
    m = max(4, int(nb_town/10))
    Best_cost = INF
    Best_Path = []
    Sigma = np.full((nb_town, nb_town), sigma0)
    filter = (G == INF)
    Sigma[filter] = 0
    Paths = [[] for i in range(m)]
    Delta = np.full((nb_town, nb_town), 0.0)
    filter = np.zeros(len(G), dtype=bool)
    for t in range(nb_iter):
        for k in range(m):
            Paths[k].append(random.randint(0, nb_town-1))
            filter[Paths[k][-1]] = True
            while (len(Paths[k]) < nb_town):
                Next_Town = Decision(
                    k, Paths[k][-1], G, Sigma, alpha, beta, filter)
                if (Next_Town == -1):
                    Paths[k] = []
                    break
                else:
                    Paths[k].append(Next_Town)
                    filter[Paths[k][-1]] = True
            if (len(Paths[k]) == nb_town):
                if (G[Paths[k][-1]][Paths[k][0]] != INF):
                    Paths[k].append(Paths[k][0])
                    filter[Paths[k][-1]] = True
                    cost = calc_path_cost(G, Paths[k])
                    if (cost < Best_cost):
                        Best_cost = cost
                        Best_Path = Paths[k].copy()
                    for i in range(nb_town):
                        Delta[Paths[k][i]][Paths[k][i+1]] += q/cost
            filter *= False
            Paths[k] = []
        Evaporation(Delta, Sigma, p)
    return Best_Path, Best_cost
