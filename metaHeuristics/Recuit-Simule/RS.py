from math import exp
import random
from typing import List, Tuple

from greedy import greedy


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
        i = random.randint(1, N - 2)
        j = random.randint(1, N - 2)
        if i != j :
            i, j = min(i, j), max(i, j)
            currNode1, currNode2 = path[i], path[j] 
            lastCurrNode1, lastCurrNode2 = path[(i-1)%N], path[(j-1)%N]
            nextCurrNode1, nextCurrNode2 = path[(i+1)%N], path[(j+1)%N]

            if i+1 == j :
                prevScore = graph[lastCurrNode1][currNode1]*(int((i!=0))) + graph[currNode2][nextCurrNode2] + graph[currNode1][currNode2]
                newScore = graph[lastCurrNode1][currNode2] + graph[currNode1][nextCurrNode2]*(int(N!=j)) + graph[currNode2][currNode1]
            else:
                prevScore = graph[lastCurrNode1][currNode1]*(int((i!=0))) + graph[currNode1][nextCurrNode1] + graph[lastCurrNode2][currNode2] + graph[currNode2][nextCurrNode2]
                newScore = graph[lastCurrNode1][currNode2] + graph[currNode2][nextCurrNode1] + graph[lastCurrNode2][currNode1] + graph[currNode1][nextCurrNode2]*(int(N!=j))
            
            path[i], path[j] = path[j], path[i]
            newCost = currentCost - prevScore + newScore
            delta = newCost - currentCost
            if delta < 0 or random.random() < exp(-delta / temperature):
                currentPath = path
                currentCost = newCost

            if currentCost < bestDistance:
                bestPath = currentPath.copy()
                bestDistance = currentCost
        
        if not ( (iteration + 1 ) % nbIterationsCooling ):
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
    graph = [[0, 4, 4, 10], [1, 4, 1, 4], [15, 7, 3, 8], [6, 4, 12, 0]]

    initial_temperature = 80.0
    cooling_rate = 0.9
    num_iterations = 1000
    num_iterations_for_cooling = 10

    initial_solution, intial_cost = greedy(graph)
    initial_solution = constructPathForGreedy(initial_solution)

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
