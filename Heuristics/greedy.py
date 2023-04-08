import numpy as np
def is_cycle(edges, x):
    # Create a dictionary of nodes and their parent nodes
    parents = {}
    for edge in edges:
        parent, child = edge[:2]
        if child not in parents:
            parents[child] = parent
    #print(parents)
    # Check if any node has a path of length x to itself
    for node in parents:
        path = [node]
        parent = parents[node]
        while parent is not None and len(path) < x:
            if (parent in path): 
                #print(edges,x,"Reponse => True")
                return True
            path.append(parent)
            parent = parents.get(parent)
        if parent == node and len(path) == x:
            #print(edges,x,"Reponse => True")
            return True
    #print(edges,x,"Reponse => False")
    return False

def greedy(matrix):
    edges=[]
    n=len(matrix)
    in_degree=[0]*n
    out_degree=[0]*n
    chosen_edges=[]
    total_cost=0
    for i in range(n):
        for j in range(len(matrix[0])):
            edges.append((i, j, matrix[i][j]))
    sorted_edges = sorted(edges, key=lambda x: x[2])
    #print(sorted_edges)
    for element in sorted_edges:
        if (len(chosen_edges)==n):
            break
        current_edge=element[:2]
        temp=chosen_edges+[current_edge]
        if(in_degree[current_edge[1]]<1 and out_degree[current_edge[0]]<1 and (not (current_edge[1],current_edge[0]) in chosen_edges ) and(not is_cycle(temp,n-1))):
            chosen_edges.append(current_edge)
            total_cost+=element[2]
            in_degree[current_edge[1]]+=1
            out_degree[current_edge[0]]+=1
    #print(chosen_edges,total_cost)
    return chosen_edges,total_cost
    


    
