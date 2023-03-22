import random 
from Benchmark import INF




#? Randomized insertion heuristic 
def RAI(G,run_times=1):
    """
        G : Asymetric graph 
    """
    n = len(G) #size of the graph 
    
    #? Generating the initiale circuit 
    
    s = random.randint(0,n-1) #* Step 01 : starting from this node
    T = [s] #* Contains the current circuit
    cost_T = 0 #* Cost of the current circuit 
    #* Step 02, 03 
    NS = [i for i in range(0,n)] #* nodes not visited yet 
    NS.remove(s) 
    while len(T)<n: #* While a full circuit is not found 
        #* Step 02
        rs = NS.pop(random.randint(0,len(NS)-1)) #select a random node
        #* Step 03  : Inserting rs in the best possible position 
        lowest_cost = INF #The lowest cost after inserting rs at position lowest_cost 
        lowest_pos = None #To store the lowest position until now
        possible = False #TODO : check if the circuit exists 
        if(len(T)==1):
            lowest_cost = cost_T + G[s,rs] + G[rs,s]
            lowest_pos = 0
        else:
            for i_ in range(0,len(T)): #* Explore all the possibles positions for rs 
                if(i_==0):
                    cost_tmp = cost_T - G[T[len(T)-1],T[i_]] + G[T[len(T)-1],rs] + G[rs,T[i_]] #*Cost if rs is inserted at ith position 
                else:
                    cost_tmp = cost_T - G[T[i_-1],T[i_]] + G[T[i_-1],rs] + G[rs,T[i_]] #*Cost if rn is inserted at ith position 
                if(cost_tmp < lowest_cost): #* Check if the cost has been reduced when inserted at i-th position 
                    lowest_pos = i_
                    lowest_cost = cost_tmp
        T.insert(lowest_pos,rs)
        cost_T = lowest_cost

    opt_circuit = T.copy() #* Best Circuit until now
    opt_cost = cost_T  #* The cost of the best circuit 
    # print(f"Initialisation : {(opt_circuit,opt_cost)}")

    #? Optimization of the initiale circuit 
    
    #* T is the current solution , it's cost is cost_T
    #* Steps 5 -> 10
    for iter in range(n**2): 
        #* Step 6 : selecting random i and j (i < j in T)
        indx_i = random.randint(0,n-1)
        indx_j = random.randint(0,n-1)
        if indx_i>indx_j:
            indx_i,indx_j = indx_j,indx_i
        i = T[indx_i]
        j = T[indx_j]
        #TODO : i should be < j

        #* Step 7
        removed_path = T[indx_i:indx_j+1]
        new_path = T[0:indx_i]+ T[indx_j+1:n]
        cost_new_path = 0        #* Cost of the new path
        for i_ in range(len(new_path)-1):
            cost_new_path+=G[new_path[i_],new_path[i_+1]]
        if(len(new_path)>1):
            cost_new_path += G[new_path[len(new_path)-1],new_path[0]]
        
        # print(f"iter : {iter} i,j={(i,j)}{(indx_i,indx_j)}  removed_path={removed_path} new_path={new_path} T = {T}")
        #TODO : check if the new path forms a circuit 
        #print(new_path)
        while len(new_path) != n: #* While all the nodes are not inserted in the new_path
            rn = removed_path.pop(random.randint(0,len(removed_path)-1)) #Select a random node
            
            lowest_cost = INF*n 
            lowest_pos = None
            possible = False #TODO :check if the circuit is possible 
            if(len(new_path)==0):
                new_path.append(rn)
                cost_new_path = 0
            else:
                if(len(new_path)==1):  #*rn has one possible position
                    cost_new_path = G[rn,new_path[0]]+G[new_path[0],rn]
                    new_path.append(rn)
                else:
                    for i_ in range(0,len(new_path)): #* Exploring the possible positions for rn 
                        if(i_==0):
                            cost_tmp = cost_new_path - G[new_path[len(new_path)-1],new_path[i_]] + G[new_path[len(new_path)-1],rn] + G[rn,new_path[i_]] #*Cost if rn is inserted at ith position 
                        else:
                            cost_tmp = cost_new_path - G[new_path[i_-1],new_path[i_]] + G[new_path[i_-1],rn] + G[rn,new_path[i_]] #*Cost if rn is inserted at ith position 
                        if(cost_tmp < lowest_cost): #* Check if the cost has been reduced when inserted at ith position 
                            lowest_pos = i_
                            lowest_cost = cost_tmp
                    new_path.insert(lowest_pos,rn)
                    cost_new_path = lowest_cost

        T = new_path.copy()
        cost_T = cost_new_path
        #* Updating the lowest path 
        if(cost_T < opt_cost):
            opt_cost = cost_T
            opt_circuit = T.copy()
            # print(f"Lowest cost updated at iter={iter} {opt_cost}")



    return opt_circuit,opt_cost


def RAI_OLD(G,run_times=1):
    """
        G : Asymetric graph 
    """
    # transform_garph(G)
    n = len(G) #size of the graph 
    
    #? Generating the initiale circuit 
    
    s = random.randint(0,n-1) #* Step 01
    T = [s] # Contains the current circuit
    
    #* Step 02, 03
    NS = [i for i in range(0,n)]
    NS.remove(s)
    stop = False
    while not stop:
        #* Step 02
        rs = NS.pop(random.randint(0,len(NS)-1)) #random node
        #* Step 03  : Inserting rs in the best possible position 
        lowest_cost = INF
        lowest_circuit = None
        possible = False
        for i in range(0,len(T)): # All possible positions for the random node
            T_cp = T.copy() 
            T_cp.insert(i,rs)
            #* Computing the cost of the circuit T_cp
            cost = 0
            for j in range(0,len(T_cp)-1):  
                cost +=  G[T_cp[j]][T_cp[j+1]]
            cost += G[T_cp[len(T_cp)-1]][T_cp[0]]
            #* Checking if the new circuit improves the cost 
            if (cost < lowest_cost):
                possible = True
                lowest_cost = cost
                lowest_circuit = T_cp.copy()
        if possible: 
            T = lowest_circuit.copy()
        else:
            NS.append(rs)
        if(len(T)==n):
            stop = True

    #? Optimization of the initiale circuit 
    opt_circuit = T.copy() #* Best Circuit until now
    opt_cost = lowest_cost  #* The cost of the best circuit 
    print(f"{opt_circuit}  {opt_cost}")
    #* T is the current solution 
    #* Steps 5 -> 10
    for iter in range(n**2): 
        #* Step 6
        indx_i = random.randint(0,n-1)
        indx_j = random.randint(0,n-1)
        if indx_i>indx_j:
            indx_i,indx_j = indx_j,indx_i
        i = T[indx_i]
        j = T[indx_j]
        #* Step 7
        removed_path = T[indx_i:indx_j+1]
        new_path = T[0:indx_i]+ T[indx_j+1:n]
        # print(f"iter : {iter} i,j={(i,j)}{(indx_i,indx_j)}  removed_path={removed_path} new_path={new_path} T = {T}")
        #TODO : check if the new path forms a circuit 
        #print(new_path)
        stop = False
        while not stop: #* Inserting all the nodes on the path
            # print(new_path)
            rn = removed_path.pop(random.randint(0,len(removed_path)-1)) #random node from the removed path 
            # print(f"{rn}",end=" ")
            #Inserting the node on the cheapest way 
            lowest_cost = INF
            lowest_circuit = None
            possible = False
            if(len(new_path)==0):
                new_path.append(rn)
            else:
                for i_ in range(0,len(new_path)): # All the possible positions for the random  node 
                    NP_cp = new_path.copy()
                    NP_cp.insert(i_,rn)
                    #* Computing the cost of the circuit NP_cp
                    cost = 0
                    for j_ in range(0,len(NP_cp)-1):  
                        cost +=  G[NP_cp[j_]][NP_cp[j_+1]]
                    cost += G[NP_cp[len(NP_cp)-1]][NP_cp[0]]
                    #* Checking if the new circuit improves the cost 
                    if (cost < lowest_cost):
                        possible = True
                        lowest_cost = cost
                        lowest_circuit = NP_cp.copy()
                if possible: 
                    new_path = lowest_circuit.copy()
                else:
                    removed_path.append(rn)
                # print(f'{len(removed_path)}')
            
            if(len(removed_path)==0):
                stop = True
        T = new_path
        #* Updating the lowest path 
        if(lowest_cost < opt_cost):
            opt_cost = lowest_cost
            opt_circuit = T.copy()
            print(f"Lowest cost updated at iter={iter} {opt_cost}")



    return opt_circuit,opt_cost

    pass