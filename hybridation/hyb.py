from typing import List, Tuple
from HillClimbing import HillClimbing
from RS import RS
from greedy import greedy
from PPV import PPV
from NI import NI
from RAI import RAI
from CI import CI
from math import floor
from selection import *
import random
INF = 99999999


def calc_path_cost(G, C):
    # ? G : Graphe
    # ? C : chemin
    tmp = 0
    if (len(C) > 1):
        for i in range(len(C)-1):
            tmp += G[C[i]][C[i+1]]
    return tmp


def print_pop(population: List[List[Tuple[List[int], int]]]):
    for i in population:
        print(i)


def path_resemblance(
    path1: List[int],
    path2: List[int]
):
    count = sum(x == y for x, y in zip(path1, path2))
    return count


def mate(
        stag: List[int],
        hind: List[int]
):
    mask = [random.randint(0, 1) for i in range(len(stag)-2)]
    new_deer1 = []
    new_deer2 = []
    changed1 = []
    changed2 = []
    new1 = []
    original1 = []
    new2 = []
    original2 = []

    new_deer1.append(hind[0])
    new_deer2.append(hind[0])
    for i in range(len(mask)):
        if mask[i]:
            new_deer1.append(hind[i+1])
            new_deer2.append(stag[i+1])
            new2.append(stag[i+1])
            original2.append(hind[i+1])
        else:
            new_deer1.append(stag[i+1])
            new_deer2.append(hind[i+1])
            new1.append(stag[i+1])
            original1.append(hind[i+1])
    new_deer1.append(hind[-1])
    new_deer2.append(stag[-1])

    changed1 = [x for x in original1 if x not in new1]
    changed2 = [x for x in original2 if x not in new2]
    start = 1
    for i in changed1:
        for j in new_deer1[start:-1]:
            if j == new_deer1[0] or new_deer1.count(j) == 2:
                index = new_deer1[start:-1].index(j)
                new_deer1[start + index] = i
                start = start + index + 1
                break

    for i in changed2:
        for j in new_deer2[start:-1]:
            if j == new_deer2[0] or new_deer2.count(j) == 2:
                index = new_deer2[start:-1].index(j)
                new_deer2[start + index] = i
                start = start + index + 1
                break

    return new_deer1, new_deer2


def RED_DEERS_RS(
    graph: List[List[int]],
    N: int,                  # taille de la population
    delta: int,               # pourcentages des males
    y: int,                   # pourcentage des commanders
    alpha: int,               # pourcentage de crossover avec son Harem
    beta: int,                # pourcentage de crossover avec un autre Harem
    nb_iteration: int,        # nombre d'iteration maximale
    algo_generation,
    initialTemperature: float,
    coolingRate: float,
    nbIterationsRS: int,
    nbIterationsHC: int,
    nbIterationsCooling: int,
    selectionAlgorithme,
):
    best_path = []
    best_cost = INF
    Nb_males = round(N * delta)
    Nb_commanders = round(y * Nb_males)
    Nb_stags = Nb_males - Nb_commanders
    Nb_hinds = N - Nb_males

    #print("Nb_Males :" + str(Nb_males))
    #print("Nb_Commanders :" + str(Nb_commanders))
    #print("Nb_stags :" + str(Nb_stags))
    #print("Nb_hinds :" + str(Nb_hinds))

    # Génération de la population initiale
    population = [list(algo_generation(graph)) for i in range(N)]
    #print("1. Population initiale: ")
    # print()
    # print_pop(population)
    # print()
    # Séparation des mâles et des femelles
    #print("2. Population triée: ")
    # print()
    for inter in range(nb_iteration):
        population.sort(key=lambda x: int(x[1]))
        # print_pop(population)
        # print()

        #print("3. Population apres ROARING")
        # print()
        # ROARING
        for i in range(Nb_males):
            population[i] = list(RS(graph, initialTemperature, coolingRate, nbIterationsRS, nbIterationsCooling,
                                    population[i][0][:-1], population[i][1])).copy()
            population[i][0].append(population[i][0][0])

        # Séparation des commanders et des stags
        population = sorted(population[:Nb_males], key=lambda x: int(
            x[1])).copy() + population[Nb_males:].copy()
        # print_pop(population)
        # print()
        # Fighting between commanders and stags
        #print("4. Population apres fight")
        # print()
        for i in range(Nb_commanders):
            New1 = list(HillClimbing(graph, nbIterationsHC,
                                     population[i][0][:-1], population[i][1]))
            New1[0].append(New1[0][0])

            stag_num = random.randint(0, Nb_stags)
            New2 = list(HillClimbing(graph, nbIterationsHC,
                                     population[Nb_commanders + stag_num][0][:-1], population[Nb_commanders + stag_num][1]))
            New2[0].append(New2[0][0])

            if (population[i][1] > New1[1]):
                population[i] = New1.copy()

            if (population[i][1] > New2[1]):
                population[i] = New2.copy()

        # print_pop(population)
        # print()

        # Constitution des harems
        sum_p = 0
        hind_num = 0
        hinds_restant = Nb_hinds
        harems = []

        tmp_population = population.copy()

        for i in range(Nb_commanders):
            sum_p = sum_p + population[i][1]
        for i in range(Nb_commanders):
            tmp = []
            for j in range(round(population[i][1] * Nb_hinds / sum_p)):
                if hinds_restant != 0:
                    if(hinds_restant>1):
                        hind_num = random.randint(0, hinds_restant-1)
                    else:
                        hind_num=0
                    tmp.append(tmp_population[Nb_males + hind_num])
                    del tmp_population[Nb_males + hind_num]
                    hinds_restant = hinds_restant - 1
            harems.append(tmp)
        while hinds_restant != 0:
            for i in range(Nb_commanders):
                if(hinds_restant>1):
                        hind_num = random.randint(0, hinds_restant-1)
                else:
                        hind_num=0
                harems[i].append(population[Nb_males + hind_num])
                hinds_restant -= 1
                if (hinds_restant == 0):
                    break

        # for i in range(Nb_commanders):
        #     print(harems[i])
        #     print()

        for i in range(Nb_commanders):

            tmp_harems = harems[i].copy()
            hinds_restant = len(harems[i])
            # Mate commander of a harem with a percent of hinds in his harem
            for j in range(round(len(harems[i])*alpha)):
                if(hinds_restant>1):
                        hind_num = random.randint(0, hinds_restant-1)
                else:
                        hind_num=0
                new_deer1, new_deer2 = mate(
                    population[i][0], tmp_harems[hind_num][0])
                population.append(
                    [new_deer1, calc_path_cost(graph, new_deer1)])
                population.append(
                    [new_deer2, calc_path_cost(graph, new_deer2)])
                hinds_restant = hinds_restant - 1
                del tmp_harems[hind_num]

            # Mate commander of a harem with a percent of hinds in an other harem
            other_harem = random.randint(0, Nb_commanders-1)
            while other_harem == i:
                other_harem = random.randint(0, Nb_commanders-1)

            tmp_harems = harems[other_harem].copy()
            hinds_restant = len(harems[other_harem])
            for j in range(round(len(harems[other_harem])*beta)):
                if(hinds_restant>1):
                    hind_num = random.randint(0, hinds_restant-1)
                else:
                    hind_num=0
                new_deer1, new_deer2 = mate(
                    population[i][0], tmp_harems[hind_num][0])
                population.append(
                    [new_deer1, calc_path_cost(graph, new_deer1)])
                population.append(
                    [new_deer2, calc_path_cost(graph, new_deer2)])
                hinds_restant = hinds_restant - 1
                del tmp_harems[hind_num]

        # Mate stag with the nearest hind
        for i in range(Nb_stags):
            nearest_hind = population[Nb_males].copy()
            resemblance = len(graph)+1

            for j in range(Nb_hinds):
                new_resemblance = path_resemblance(
                    population[Nb_commanders + i][0], population[Nb_males + j][0])
                if (new_resemblance < resemblance):
                    nearest_hind = population[Nb_males + j].copy()
                    resemblance = new_resemblance

            new_deer1, new_deer2 = mate(population[i][0], nearest_hind[0])
            population.append([new_deer1, calc_path_cost(graph, new_deer1)])
            population.append([new_deer2, calc_path_cost(graph, new_deer2)])

        # print_pop(population)
        # print()

        # Selection of the new population
        population = selectionAlgorithme(population, N)

        # print_pop(population)
        for sol in population:
            if sol[1] < best_cost:
                best_path = sol[0].copy()
                best_cost = sol[1]

    return best_path, best_cost


if __name__ == "__main__":

    initial_temperature = 80.0
    cooling_rate = 0.9
    num_iterations = 1000
    num_iterations_for_cooling = 10

    graph = [
        [INF, 2, 9, 10, 6, 4, 8, 5, 7, 3, 1, 11],
        [2, INF, 11, 9, 8, 3, 1, 7, 4, 10, 5, 6],
        [9, 11, INF, 6, 7, 8, 10, 2, 1, 4, 5, 3],
        [10, 9, 6, INF, 2, 11, 3, 8, 5, 1, 7, 4],
        [6, 8, 7, 2, INF, 5, 4, 9, 10, 3, 11, 1],
        [4, 3, 8, 11, 5, INF, 6, 10, 1, 2, 9, 7],
        [8, 1, 10, 3, 4, 6, INF, 7, 2, 9, 11, 5],
        [5, 7, 2, 8, 9, 10, 7, INF, 6, 11, 4, 1],
        [7, 4, 1, 5, 10, 1, 2, 6, INF, 8, 3, 11],
        [3, 10, 4, 1, 3, 2, 9, 11, 8, INF, 7, 6],
        [1, 5, 5, 7, 11, 9, 11, 4, 3, 7, INF, 10],
        [11, 6, 3, 4, 1, 7, 5, 1, 11, 6, 10, INF]
    ]
    print("Final solution : ")
    print(RED_DEERS_RS(graph, 15, 0.5, 0.5, 0.5, 0.3, 10, PPV, initial_temperature,
                       cooling_rate, num_iterations, 100, num_iterations_for_cooling, SEL_TOURNAMENT))