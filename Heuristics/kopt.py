import copy
from CI import *


def getCost(graph, path, pathLength):
    return sum(graph[path[i]][path[i + 1]] for i in range(pathLength - 1))


def k_opt(graph, path, k, bestCost, pathLength):
    for i in range(pathLength):
        for j in range(i + k + 1, pathLength):
            reversedPath = path[i + 1 : j][::-1]
            newPath = path[: i + 1] + reversedPath + path[j:]
            cost = getCost(graph, newPath, pathLength)
            if cost < bestCost:
                bestCost = cost
                path = copy.deepcopy(newPath)
    return path, bestCost


def mainKOPT(graph, k):
    initialSolution, initialCost = CI(graph)
    pathLength = len(initialSolution)

    optimized_solution, newCost = k_opt(
        graph, initialSolution, k, initialCost, pathLength
    )
    return optimized_solution, newCost
