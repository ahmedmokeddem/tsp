import numpy as np

# Convention
#   - Rows : Sources
#   - Columns : Destinations

def CI(arcs):
    #? Cheapest Insertion Heuristic Algorithm


    # 1 . Initialization : 
    #       - Initialize params
    #       - Find minimum arc between 2 nodes
    #       - Initialize Unvisited nodes set to V - {i, j} as i, j first two nodes linked with minimum arc.

    # Initialize result params
    best_tour, best_length = None, float('inf')

    # S is the set Of visited Arcs
    S = [np.unravel_index(np.argmin(arcs, axis=None), arcs.shape)]
    i, j = S[0]


    # unvisited_nodes is the set of visited nodes
    unvisited_nodes = [k for k in range(arcs.shape[0])]
    unvisited_nodes.remove(i)
    unvisited_nodes.remove(j)

    #! For testing
    # print(S)
    # print(unvisited_nodes)

    # 2 . Add Third Node :
    #     - This step is different since we wont be omitting any arc

    minimum_arcs = float('inf')
    seq_arcs_best_tour = None
    for k in unvisited_nodes:
        current_arcs = arcs[S[0][1]][k] + arcs[k][S[0][0]]
        if minimum_arcs > current_arcs:
            minimum_arcs = current_arcs
            # Store arcs to be added
            seq_arcs_best_tour = [(S[0][1], k), (k, S[0][0])]

    # Added Arcs 
    S.append(seq_arcs_best_tour[0])
    S.append(seq_arcs_best_tour[1])

    # Delete Visited Node
    unvisited_nodes.remove(seq_arcs_best_tour[0][1])

    #! For testing
    # print(S)
    # print(unvisited_nodes)



    # 3 . Loop :
    #      - For each Unvisited Node, find best insertion, which satisfies :
    #         Insertion of that node between two cities will keep the subtour minimum
    # Link : https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&ved=2ahUKEwjW8vemnZX-AhX6UqQEHba9B1YQFnoECAsQAQ&url=https%3A%2F%2Fcore.ac.uk%2Fdownload%2Fpdf%2F31029163.pdf&usg=AOvVaw0zhFih_DogCfUj9KHMP9Fg


    while(len(unvisited_nodes) != 0) :
        minimum_arcs = float('inf')
        seq_arcs_best_tour = None
        sacrificed_arc = None
        for l in S:
            for k in unvisited_nodes:
                current_arcs = arcs[l[0]][k] + arcs[k][l[1]] - arcs[l[0]][l[1]]
                if minimum_arcs > current_arcs:
                    minimum_arcs = current_arcs
                    # Store arcs to be added
                    seq_arcs_best_tour = [(l[0], k), (k, l[1])]
                    # Store arc to be sacrificed
                    sacrificed_arc = l

        # Remove Sacrificed Arc
        S.remove(sacrificed_arc)

        # Added Arcs 
        S.append(seq_arcs_best_tour[0])
        S.append(seq_arcs_best_tour[1])

        # Delete Visited Node
        unvisited_nodes.remove(seq_arcs_best_tour[0][1])

        #! For testing
        # print(S)
        # print(unvisited_nodes)






    # 4 . Construct Results

    # best_tour
    best_tour = []
    mapping = dict(S)

    # Append First Value
    next_value = next(iter(mapping.values()))
    best_tour.append(next_value)

    while (len(best_tour) != len(mapping)) :
        next_value = mapping[next_value]
        best_tour.append(next_value)

    # best_tour = S

    # best_length
    best_length = 0
    for k in range(len(S)) :
        best_length += arcs[S[k][0]][S[k][1]]


    return best_tour, best_length