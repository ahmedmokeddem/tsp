from BB import *
import tsplib95
import time


# #* Chargement du benchmark : br17.atsp avec 17   #
# #! Mauvais Benchmark 
# problem = tsplib95.load('br17.atsp')
# print(problem.render())
# tmp = problem.edge_weights
# G = []
# for i in range(17):
#     G.append(tmp.pop(0)+tmp.pop(0))
# print(G)

#* Chargement du benchmark : ft53.atsp avec 17  
problem = tsplib95.load('ft53.atsp')
print(problem.render())
tmp = problem.edge_weights
G = []
for i in range(17):
    G.append(tmp.pop(0)+tmp.pop(0)+tmp.pop(0)+tmp.pop(0))
print(G)


# G = [[0,1,0,108],
#      [5,0,125,20],
#      [2,11,0,1],
#      [10,50,20,0],]

n = 12  #* Nombre de sommets 
A = 0   #* Le point de départ 
start = time.time()
print(BB(G[:n][:n],A,n))
end = time.time()
print("\nLe temp d'éxecution est : "+str(end - start)+"s")
