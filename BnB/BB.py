import math 
import numpy as np


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
def evaluate_rest(G,C):
    n = len(G)
    tmp = np.full((n,),9999)
    for i in range(n):
        for j in range(n):
                if(i not in C or i == C[-1]) and (j not in C or j == 0 ) and G[i][j] > 0:
                    if(G[i][j]<tmp[i]):
                        tmp[i]= G[i][j]
    tmp.sort()
    return np.sum(tmp[:n-len(C)+1])

def evaluate(G,C):
    return calc_path_cost(G,C)  +  evaluate_rest(G,C)  #* remplacer 0 avec evaluation du cout restant 

def BB(G,A,n):
    #? G : le graph 
    #? A : le point de départ 
    #? n : nb sommets 
    
    nb_visited = 0


    P1 = [] #* Pile de parcours
    P2 = [] #* Pile du chemin
    cost_min = math.inf 
    path_min = None

    P1.append((A,1)) #* Point de départ 

    while (len(P1) > 0):
        s,d = P1.pop()
        nb_visited += 1
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
    return path_min,cost_min,nb_visited


