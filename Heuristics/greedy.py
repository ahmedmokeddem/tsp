import random

# Cette fonction cherche tous les arcs éligibles (qui peuvent être ajoutés au tour sans créer de cycle ou causer un degré supérieur à 1)
# Les arcs éligibles sont stockés dans une liste eligible_arcs, puis triés par ordre croissant de longueur
# Finalement, la fonction retourne une liste de tous les arcs qui ont la même longueur que le plus court arc
def find_shortest_eligible_arcs(arcs, chosen_arcs, degree, n):
    eligible_arcs = []
    for i in range(n):
        for j in range(n):
            if i != j and degree[i] < 2 and degree[j] < 2:
                arc = (i, j)
                if arc not in chosen_arcs and arc[::-1] not in chosen_arcs:
                    eligible_arcs.append(arc)
    sorted_arcs = sorted(eligible_arcs, key=lambda x: arcs[x[0]][x[1]])
    return [arc for arc in sorted_arcs if arcs[arc[0]][arc[1]] == arcs[sorted_arcs[0][0]][sorted_arcs[0][1]]]
# Cette fonction construit un tour hamiltonien en choisissant de manière aléatoire parmi les arcs éligibles les plus courts
# Elle initialise une liste degree pour stocker le degré entrant et sortant de chaque sommet
# Elle itère jusqu'à ce que tous les sommets soient visités, en choisissant à chaque fois un arc éligible de manière aléatoire
# Elle stocke chaque arc choisi dans la liste chosen_arcs
# Elle met à jour les degrés de chaque sommet en ajoutant 1 pour chaque extrémité de l'arc choisi
# Elle construit le tour en partant du premier sommet de l'arc initial et en ajoutant les sommets des arcs suivants
# Elle calcule la longueur totale du tour en sommant les longueurs des arcs choisis
# Elle retourne le tour et la longueur totale en tant que tuple
def construct_tour(arcs):
    n=len(arcs)
    degree = [0] * n
    chosen_arcs = []
    while len(chosen_arcs) < n - 1:
        eligible_arcs = find_shortest_eligible_arcs(arcs, chosen_arcs, degree, n)
        if not eligible_arcs:
            return None,None
        arc = random.choice(eligible_arcs)
        chosen_arcs.append(arc)
        degree[arc[0]] += 1
        degree[arc[1]] += 1
    tour = [chosen_arcs[0][0]]
    total_cost = 0
    for arc in chosen_arcs:
        if arc[0] == tour[-1]:
            tour.append(arc[1])
        else:
            tour.append(arc[0])
        total_cost += arcs[arc[0]][arc[1]]
    tour.append(chosen_arcs[-1][1])
    return tour, total_cost
