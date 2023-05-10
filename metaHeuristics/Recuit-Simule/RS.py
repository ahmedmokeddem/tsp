from math import exp
import random
from typing import List, Tuple

from greedy import greedy


def tspSimulatedAnnealing(
    graph: List[List[int]],
    initialTemperature: float,
    coolingRate: float,
    nbIterations: int,
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
        path[i], path[j] = path[j], path[i]

        newCost = calculatePathDistance(graph, path)
        delta = newCost - currentCost

        if delta < 0 or random.random() < exp(-delta / temperature):
            currentPath = path
            currentCost = newCost

        if currentCost < bestDistance:
            bestPath = currentPath.copy()
            bestDistance = currentCost

        temperature *= coolingRate

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
    graph = [[0, 4, 4, 10], [1, 4, 1, 4], [15, 7, 3, 8], [6, 4, 12, 0]]

    initial_temperature = 80.0
    cooling_rate = 0.9
    num_iterations = 1000

    initial_solution, intial_cost = greedy(graph)
    initial_solution = constructPathForGreedy(initial_solution)

    print(initial_solution, intial_cost)

    best_path, best_distance = tspSimulatedAnnealing(
        graph,
        initial_temperature,
        cooling_rate,
        num_iterations,
        initial_solution,
        intial_cost,
    )

    print("Best Path:", best_path)
    print("Best Distance:", best_distance)
