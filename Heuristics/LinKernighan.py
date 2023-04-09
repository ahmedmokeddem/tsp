from greedy import *


def getCost(graph, path, pathLength):
    return sum(graph[path[i]][path[i + 1]] for i in range(pathLength - 1))


def linKernighan(graph, path, pathLength):
    while True:
        bestGain = 0
        for i in range(pathLength):
            for j in range(i + 2, pathLength):
                gain = getGain(graph, path, i, j, pathLength)
                if gain > bestGain:
                    bestGain = gain
                    bestI, bestJ = i, j

        if bestGain == 0:
            path.append(path[0])
            return path

        path = makeMove(path, bestI, bestJ)


def getGain(graph, path, i, j, pathLength):
    a, b = path[i], path[(i + 1) % pathLength]
    c, d = path[j], path[(j + 1) % pathLength]
    return (graph[c][d] + graph[a][b]) - (graph[a][c] + graph[b][d])


def makeMove(path, i, j):
    return path[: i + 1] + path[j:i:-1] + path[j + 1 :]


def linKernighanMain(graph):
    initialSolution, _ = construct_tour(graph)

    initialSolution.pop()
    pathLength = len(initialSolution)
    path = linKernighan(graph, initialSolution, pathLength)
    cost = getCost(graph, path, pathLength + 1)

    return path, cost
