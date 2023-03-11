import math 
import numpy as np
from scipy.sparse.csgraph import minimum_spanning_tree

def mst_lower_bound(graph, path):
    # converting the list to numpy for faster process
    graph = np.array(graph)
    path = np.array(path)

    # getting the unvisited nodes
    unvisited = set(range(len(graph))) - set(path)

    # creating a subgraph with only unvisited nodes
    subgraph = np.zeros((len(graph), len(graph)))
    for i in unvisited:
        for j in unvisited:
            subgraph[i][j] = graph[i][j]

    # calculating the MST for the subgraph
    mst = minimum_spanning_tree(subgraph).toarray()

    # Compute the sum of the edge weights in the MST
    mst_cost = np.sum(mst)

    nearest_dist = np.min(mst[:, path], axis=1)
    nearest_cost = np.sum(nearest_dist)
    
    # Return the estimated cost of the best possible path that can be obtained by extending the partial path
    return mst_cost + nearest_cost


#? Fonction qui calcul le cout d'un chemin 
def calc_path_cost(G,C):
    #? G : Graphe
    #? C : chemin 
    tmp = 0
    if(len(C)>1):
        for i in range(len(C)-1):
            tmp += G[C[i]][C[i+1]]
    # print(f"Eval {C} = {tmp}")
    return tmp


#! Fonction d'evaluation basique a ameliorer 
def evaluate(G,C):
    return calc_path_cost(G,C)  + mst_lower_bound(G,C) 

def BB(G,A,n):
    #? G : le graph 
    #? A : le point de départ 
    #? n : nb sommets 
    
    P1 = [] #* Pile de parcours
    P2 = [] #* Pile du chemin
    cost_min = math.inf 
    path_min = None

    P1.append((A,1)) #* Point de départ 

    while (len(P1) > 0):
        s,d = P1.pop()
        while(len(P2) != d-1):
            P2.pop()
        P2.append(s)

        if(len(P2)==n+1):
            path_cost = calc_path_cost(G,P2)    
            print(f"Eval {P2} = {path_cost}  ---> {path_min} {cost_min}")
            if(path_cost<cost_min):
                cost_min = path_cost
                path_min = P2.copy()
        else:
            node_eval = evaluate(G,P2) 
            if(node_eval <= cost_min):
                for k in range(n):
                    if(G[s][k]>0):
                        if(k not in P2 or len(P2)==n and k==A):
                            P1.append((k,d+1))
    return path_min,cost_min


