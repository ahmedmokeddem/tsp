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
    return tmp


#? Une estimation du cout restant 
def evaluate_rest(G,A,C):
    #? G :Graphe
    #? A : Point de départ
    #? C : Chemin
    n = len(G)
    tmp = np.full((n,),999999) #! 999999 => inf
    for i in range(n):
        for j in range(n):
                #? Tester que 
                #*  - Il reste encore un arc sortant de i
                #*  - Il reste encore un arc entrant dans j
                #*  - Il existe un arce de i vers j
                if(i not in C or i == C[-1]) and (j not in C or j == A ) and G[i][j] > 0:
                    if(G[i][j]<tmp[i]):
                        tmp[i]= G[i][j]
    tmp.sort()  #? Pour mettre les 999999 a la fin 
    return np.sum(tmp[:n-len(C)+1])  #* Somme des arcs trouvés 

def evaluate(G,A,C):
    #? G :Graphe
    #? A : Point de départ
    #? C : Chemin
    return calc_path_cost(G,C)  +  evaluate_rest(G,A,C)  

def BB(G,A,n):
    #? G : le graph 
    #? A : le point de départ 
    #? n : nb sommets 
        
    nb_visited = 0 #* Nombre de noeuds visités 

    P1 = [] #* Pile de parcours
    P2 = [] #* Pile du chemin

    #* Initialisation 
    cost_min = math.inf 
    path_min = None

    P1.append((A,1)) #* Point de départ 

    while (len(P1) > 0):
        s,d = P1.pop()
        nb_visited += 1
        
        while(len(P2) != d-1): #* Depiler dans la pile P2 jusqu'au père du noeuds s
            P2.pop()
        P2.append(s)

        if(len(P2)==n+1): #* Cas ou on trouve un circuit , on test si il améliore le cout 
            path_cost = calc_path_cost(G,P2)    
            print(f"Eval {P2} = {path_cost}  ---> {path_min} {cost_min}") 
            if(path_cost<cost_min):
                cost_min = path_cost
                path_min = P2.copy()
        else: 
            node_eval = evaluate(G,A,P2)  #* Evaluation du noeud 
            if(node_eval <= cost_min): #? Condition d'élagage 
                for k in range(n): #* Parcours des fils  
                    if(G[s][k]>0): 
                        if(k not in P2 or len(P2)==n and k==A): #* Empilement des noeuds non encore dans le chemin actuel 
                            P1.append((k,d+1))
    return path_min,cost_min,nb_visited


