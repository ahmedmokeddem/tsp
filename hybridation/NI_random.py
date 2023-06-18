from Benchmark import *
import random
def calc_path_cost(G,C): 
    #? G : Graphe
    #? C : chemin 
    tmp = 0
    if(len(C)>1):
        for i in range(len(C)-1):
            tmp += G[C[i]][C[i+1]]
    return tmp

#def verifie_circuit(G,T):
#    for i in range(len(T)) :
#        if G[T[i]][T[i+1]]==INF :
#            return False
#    return True

def exclude_node(node_to_test,excluded_nodes) :
    for node in excluded_nodes:
        if node[0]==node_to_test and node[1]==0 :
            return True
    return False   

def nearest_node(G,current_tour,unvisited_nodes,excluded_nodes) : 
    node_result=unvisited_nodes[0]
    none_return=True
    for node in unvisited_nodes :
        if not(exclude_node(node,excluded_nodes)) :
            none_return=False
            break
    if none_return :
        return None    
    for node in current_tour :
            for u_node in unvisited_nodes:
                if G[node][u_node]<G[node][node_result] or G[node][u_node]<G[node_result][node] or G[u_node][node]<G[node][node_result] or G[u_node][node]<G[node_result][node] :
                    if  len(excluded_nodes)==0: 
                        node_result=u_node
                    elif not(exclude_node(u_node,excluded_nodes)):
                        node_result=u_node
                    else :
                        pass
    return node_result

def possible_tours(G,current_tour,nearest_node) :
    po_tours=[current_tour[:i]+[nearest_node]+current_tour[i:] for i in range(1,len(current_tour))] #generation de tous les insertions possibles
    tours_with_cost=[]
    for tour in po_tours :
        cost=calc_path_cost(G,tour)
        if cost<INF :
            tours_with_cost.append([tour,calc_path_cost(G,tour)])
    return sorted(tours_with_cost, key = lambda x: x[0])
    
def possible_Insertions(G,current_tour,nearest_node) :
    po_tours=[current_tour[:i]+[nearest_node]+current_tour[i:] for i in range(0,len(current_tour)+1)] #generation de tous les insertions possibles
    tours_with_cost=[]
    for tour in po_tours :
        cost=calc_path_cost(G,tour)
        if cost<INF :
            tours_with_cost.append([tour,calc_path_cost(G,tour)])
    return sorted(tours_with_cost, key = lambda x: x[1])    

def NI(G) :
    tour, current_length = None, float('inf')
    n=len(G)
    first=random.randint(0,n-1)
    second=random.randint(0,n-1)
    while first == second and G[first][second] == INF :
        second=random.randint(0,n-1)
    if G[first][second]==INF :
        print("There's no tour\n")
        return 0
    tour=[first,second,first]
    current_length=calc_path_cost(G,tour)
    unvisited_nodes= [k for k in range(0,n)]
    unvisited_nodes.remove(first)
    unvisited_nodes.remove(second)
    steps=[[[second,0]]]
    new_step=True
    old_node=second
    while(len(unvisited_nodes)!=0 and len(steps)!=0):
        if new_step :
            steps.append([])
        current_node=nearest_node(G,tour,unvisited_nodes,steps[-1])
        if current_node==None :
            steps.pop()
            if(len(steps)==0):
                break
            tour.remove(steps[-1][-1][0])
            unvisited_nodes.append(steps[-1][-1][0])
            new_step=False
            pass
        elif(current_node!=old_node) :
            possible_insr=possible_tours(G,tour,current_node)
            steps[-1].append([current_node,len(possible_insr)])
        else :
            pass
        if(len(possible_insr)==0):
            new_step=False
            pass
        else :
            possible_insr=sorted(possible_insr,key = lambda y: y[1])
            tour,current_length=possible_insr[len(possible_insr)-steps[-1][-1][1]][0],possible_insr[len(possible_insr)-steps[-1][-1][1]][1]
            steps[-1][-1][1]-=1
            unvisited_nodes.remove(current_node)
            new_step=True
    #Testing if the original heuristic gives a solution
    if(len(tour)==n+1) :
        return tour,current_length
    else : 
        tour=[first,second]
        current_length=calc_path_cost(G,tour)
        unvisited_nodes= [k for k in range(0,n)]
        unvisited_nodes.remove(first)
        unvisited_nodes.remove(second)
        steps=[[[second,0]]]
        new_step=True
        old_node=second
        while(len(unvisited_nodes)!=0 and len(steps)!=0):
            print(steps)
            if new_step :
                steps.append([])
            current_node=nearest_node(G,tour,unvisited_nodes,steps[-1])
            if current_node==None :
                steps.pop()
                if(len(steps)==0):
                    break
                tour.remove(steps[-1][-1][0])
                unvisited_nodes.append(steps[-1][-1][0])
                new_step=False
                pass
            elif(current_node!=old_node) :
                possible_insr=possible_Insertions(G,tour,current_node)
                steps[-1].append([current_node,len(possible_insr)])
            else :
                pass
            if(len(possible_insr)==0):
                new_step=False
                pass
            else :
                tour,current_length=possible_insr[len(possible_insr)-steps[-1][-1][1]][0],possible_insr[len(possible_insr)-steps[-1][-1][1]][1]
                steps[-1][-1][1]-=1
                if len(tour)==n and G[tour[-1]][tour[0]]!=INF :
                    current_length+=G[tour[-1]][tour[0]]
                    tour.append(tour[0])
                    return tour,current_length
                elif len(tour)==n and G[tour[-1]][tour[0]]!=INF :
                    new_step=False
                else :
                    new_step=True
                    unvisited_nodes.remove(current_node)
        if len(steps)==0 :
            return None,None
        
if __name__ == "__main__" :
    graph = [ [INF, 2, 9, 10, 6, 4, 8, 5, 7, 3, 1, 11], [2, INF, 11, 9, 8, 3, 1, 7, 4, 10, 5, 6], [9, 11, INF, 6, 7, 8, 10, 2, 1, 4, 5, 3], [10, 9, 6, INF, 2, 11, 3, 8, 5, 1, 7, 4], [6, 8, 7, 2, INF, 5, 4, 9, 10, 3, 11, 1], [4, 3, 8, 11, 5, INF, 6, 10, 1, 2, 9, 7], [8, 1, 10, 3, 4, 6, INF, 7, 2, 9, 11, 5], [5, 7, 2, 8, 9, 10, 7, INF, 6, 11, 4, 1], [7, 4, 1, 5, 10, 1, 2, 6, INF, 8, 3, 11], [3, 10, 4, 1, 3, 2, 9, 11, 8, INF, 7, 6], [1, 5, 5, 7, 11, 9, 11, 4, 3, 7, INF, 10], [11, 6, 3, 4, 1, 7, 5, 1, 11, 6, 10, INF] ]
    for i in range(10) :
        print(NI(graph))