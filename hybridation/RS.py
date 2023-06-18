from math import exp
import random
from typing import List, Tuple

from greedy import greedy
import numpy as np

def calculatePathDistance(graph: List[List[int]], path: List[int]) -> int:
    num_cities = len(graph)
    distance = 0

    for i in range(num_cities):
        j = (i + 1) % num_cities
        distance += graph[path[i]][path[j]]

    return distance


def RS(
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
