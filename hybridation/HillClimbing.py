from math import exp
import random
from typing import List, Tuple
INF = 99999999


def HillClimbing(
    graph: List[List[int]],
    nbIterations: int,
    currentPath: List[int],
    currentCost: int,
) -> Tuple[List[int], int]:

    N = len(graph)
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
                graph[currNode2][nextCurrNode2] + graph[currNode1][currNode2]
            newScore = graph[lastCurrNode1][currNode2] + \
                graph[currNode1][nextCurrNode2] + graph[currNode2][currNode1]
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

        if newCost < currentCost:
            currentPath = path
            currentCost = newCost

    return currentPath, currentCost


if __name__ == "__main__":
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

    path, cost = [4, 11, 7, 2, 8, 5, 9, 3, 6, 1, 0, 10], 27
    print(HillClimbing(graph, 1000, path, cost))
