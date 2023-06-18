from math import exp
import random
from typing import List, Tuple

from greedy import greedy
import numpy as np
INF = 99999999


def tspSimulatedAnnealing(
    graph: List[List[int]],
    initialTemperature: float,
    coolingRate: float,
    nbIterations: int,
    nbIterationsCooling: int,
    currentPath: List[int],
    currentCost: int,
) -> Tuple[List[int], int]:

    N = len(graph)

    bestPath = currentPath.copy()
    bestDistance = currentCost

    temperature = initialTemperature

    for iteration in range(nbIterations):
        path = currentPath.copy()
        i = random.randint(0, N - 1)
        j = random.randint(0, N - 1)
        if i != j:
            i, j = min(i, j), max(i, j)
            currNode1, currNode2 = path[i], path[j]
            lastCurrNode1, lastCurrNode2 = path[(i-1) % N], path[(j-1) % N]
            nextCurrNode1, nextCurrNode2 = path[(i+1) % N], path[(j+1) % N]

            if i+1 == j:
                prevScore = graph[lastCurrNode1][currNode1] + \
                    graph[currNode2][nextCurrNode2] + \
                    graph[currNode1][currNode2]
                newScore = graph[lastCurrNode1][currNode2] + \
                    graph[currNode1][nextCurrNode2] + \
                    graph[currNode2][currNode1]
            elif i == 0:
                if j == N-1:
                    prevScore = graph[currNode1][nextCurrNode1] + \
                        graph[lastCurrNode2][currNode2] + \
                        graph[currNode2][nextCurrNode2]
                    newScore = graph[currNode2][nextCurrNode1] + \
                        graph[lastCurrNode2][currNode1] + \
                        graph[currNode1][currNode2]
                else:
                    prevScore = graph[lastCurrNode1][currNode1] + graph[currNode1][nextCurrNode1] + \
                        graph[lastCurrNode2][currNode2] + \
                        graph[currNode2][nextCurrNode2]
                    newScore = graph[currNode2][nextCurrNode1] + graph[lastCurrNode1][currNode2] + \
                        graph[lastCurrNode2][currNode1] + \
                        graph[currNode1][nextCurrNode2]
            else:
                prevScore = graph[lastCurrNode1][currNode1] + graph[currNode1][nextCurrNode1] + \
                    graph[lastCurrNode2][currNode2] + \
                    graph[currNode2][nextCurrNode2]
                newScore = graph[lastCurrNode1][currNode2] + graph[currNode2][nextCurrNode1] + \
                    graph[lastCurrNode2][currNode1] + \
                    graph[currNode1][nextCurrNode2]
            path[i], path[j] = path[j], path[i]
            newCost = currentCost - prevScore + newScore
            delta = newCost - currentCost
            if delta < 0 or random.random() < exp(-delta / temperature):
                currentPath = path
                currentCost = newCost

            if currentCost < bestDistance:
                bestPath = currentPath.copy()
                bestDistance = currentCost

        if not ((iteration + 1) % nbIterationsCooling):
            temperature *= coolingRate

        # You can add breaking condition here if cond : break

    return bestPath, bestDistance


def calculatePathDistance(graph: List[List[int]], path: List[int]) -> int:
    num_cities = len(graph)
    distance = 0

    for i in range(num_cities):
        j = (i + 1) % num_cities
        distance += graph[path[i]][path[j]]

    return distance


def constructPathForGreedy(oldPath: List[Tuple[int, int]]) -> List[int]:
    start, path = 0, []
    arcs = {}
    for arc in oldPath:
        arcs[arc[0]] = arc[1]

    curr = start

    while True:
        path.append(curr)
        curr = arcs[curr]
        if curr == start:
            path.append(start)
            break
    return path


if __name__ == "__main__":
    graph = [[INF, 2, 9, 10, 6, 4, 8, 5, 7, 3, 1, 11],
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
             [11, 6, 3, 4, 1, 7, 5, 1, 11, 6, 10, INF]]

    initial_temperature = 80.0
    cooling_rate = 0.9
    num_iterations = 1000
    num_iterations_for_cooling = 10

    initial_solution, intial_cost = [
        3, 9, 5, 8, 2, 7, 11, 4, 6, 1, 0, 10], 24

    print(initial_solution, intial_cost)

    best_path, best_distance = tspSimulatedAnnealing(
        graph,
        initial_temperature,
        cooling_rate,
        num_iterations,
        num_iterations_for_cooling,
        initial_solution,
        intial_cost,
    )

    print("Best Path:", best_path)
    print("Best Distance:", best_distance)


def tspSimulatedAnnealing_recording_delta(
    graph: List[List[int]],
    initialTemperature: float,
    coolingRate: float,
    nbIterations: int,
    nbIterationsCooling: int,
    currentPath: List[int],
    currentCost: int,
) -> Tuple[List[int], int]:

    N = len(graph)

    bestPath = currentPath.copy()
    bestDistance = currentCost

    temperature = initialTemperature

    delta_values = []

    for iteration in range(nbIterations):
        path = currentPath.copy()
        i = random.randint(0, N - 1)
        j = random.randint(0, N - 1)
        if i != j:
            i, j = min(i, j), max(i, j)
            currNode1, currNode2 = path[i], path[j]
            lastCurrNode1, lastCurrNode2 = path[(i-1) % N], path[(j-1) % N]
            nextCurrNode1, nextCurrNode2 = path[(i+1) % N], path[(j+1) % N]

            if i+1 == j:
                prevScore = graph[lastCurrNode1][currNode1] + \
                    graph[currNode2][nextCurrNode2] + \
                    graph[currNode1][currNode2]
                newScore = graph[lastCurrNode1][currNode2] + \
                    graph[currNode1][nextCurrNode2] + \
                    graph[currNode2][currNode1]
            elif i == 0:
                if j == N-1:
                    prevScore = graph[currNode1][nextCurrNode1] + \
                        graph[lastCurrNode2][currNode2] + \
                        graph[currNode2][nextCurrNode2]
                    newScore = graph[currNode2][nextCurrNode1] + \
                        graph[lastCurrNode2][currNode1] + \
                        graph[currNode1][currNode2]
                else:
                    prevScore = graph[lastCurrNode1][currNode1] + graph[currNode1][nextCurrNode1] + \
                        graph[lastCurrNode2][currNode2] + \
                        graph[currNode2][nextCurrNode2]
                    newScore = graph[currNode2][nextCurrNode1] + graph[lastCurrNode1][currNode2] + \
                        graph[lastCurrNode2][currNode1] + \
                        graph[currNode1][nextCurrNode2]
            else:
                prevScore = graph[lastCurrNode1][currNode1] + graph[currNode1][nextCurrNode1] + \
                    graph[lastCurrNode2][currNode2] + \
                    graph[currNode2][nextCurrNode2]
                newScore = graph[lastCurrNode1][currNode2] + graph[currNode2][nextCurrNode1] + \
                    graph[lastCurrNode2][currNode1] + \
                    graph[currNode1][nextCurrNode2]
            path[i], path[j] = path[j], path[i]
            newCost = currentCost - prevScore + newScore
            delta = newCost - currentCost
            delta_values.append(abs(delta))
            if delta < 0 or random.random() < exp(- delta / temperature):
                currentPath = path
                currentCost = newCost

            if currentCost < bestDistance:
                bestPath = currentPath.copy()
                bestDistance = currentCost

        if not ((iteration + 1) % nbIterationsCooling):
            temperature *= coolingRate

        # You can add breaking condition here if cond : break

    # Reading old values

    # Appending new values

    # Saving the values

    old_data = np.loadtxt(
        './results/ouss/delta/delta_distribution.txt', delimiter=',')
    my_array = np.array(delta_values + old_data.tolist())
    # my_array = np.array(delta_values)

    print(len(my_array))
    # Save the array to a CSV file
    np.savetxt('./results/ouss/delta/delta_distribution.txt', my_array)
    return bestPath, bestDistance
