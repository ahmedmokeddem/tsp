import random

# For all functions population : List[List[List[int],int]] , N:int -> List[List[List[int],int]]


def SEL_ROULETTE(population, N):
    somme = 0
    selected_population = []
    population.sort(key=lambda x: x[1], reverse=True)
    for RD in population:
        somme += (1/RD[1])
    while (len(selected_population) < N):
        # To define intervals of the roulette
        cumul = 0
        tmp = []
        for RD in population:
            cumul += ((1/RD[1])/somme)
            tmp.append([RD[0], RD[1], cumul])
        choice = random.uniform(0, 1)
        i = 0
        while True:
            if (i == 0 and choice <= tmp[i][2]):
                break
            elif (i != 0 and choice <= tmp[i][2] and choice > tmp[i-1][2]):
                break
            else:
                i += 1
        selected_population.append([tmp[i][0], (tmp[i][1])])
        population.remove([tmp[i][0], tmp[i][1]])
        somme -= (1/tmp[i][1])
    return selected_population


def SEL_RANKING(population, N):
    selected_population = []
    population.sort(key=lambda x: x[1], reverse=True)
    while (len(selected_population) < N):
        # To define intervals of the roulette
        rang = 1
        tmp = []
        total = (len(population)/2)*(len(population)+1)
        cumul = 0
        for RD in population:
            cumul += rang/total
            tmp.append([RD[0], RD[1], cumul])
            rang += 1
        choice = random.uniform(0, 1)
        i = 0
        while True:
            if (i == 0 and choice <= tmp[i][2]):
                break
            elif (i != 0 and choice <= tmp[i][2] and choice > tmp[i-1][2]):
                break
            else:
                i += 1
        selected_population.append([tmp[i][0], tmp[i][1]])
        population.remove([tmp[i][0], tmp[i][1]])
    return selected_population


def SEL_ELITISTE(population, N):
    population.sort(key=lambda x: x[1])
    selected_population = population[:N]
    return selected_population


def SEL_TOURNAMENT(population, N):
    selected_population = []
    while (len(selected_population) < N):
        curr_pop_len = len(population)
        i = random.randint(0, curr_pop_len-1)
        j = random.randint(0, curr_pop_len-1)
        while (j == i):
            j = random.randint(0, curr_pop_len-1)
        choice = random.uniform(0, 1)
        if (population[j][1] < population[i][1]):
            i, j = j, i
        somme = (1/population[i][1])+(1/population[j][1])
        if (choice <= ((1/population[j][1])/somme)):
            i = j
        selected_population.append(population[i])
        population.pop(i)
    return selected_population


def SEL_RANDOM(population, N):
    selected_population = random.sample(population, N)
    return selected_population
