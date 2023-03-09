from BB import *
import tsplib95



#* Chargement du benchmark : br17.atsp avec 17  
problem = tsplib95.load('br17.atsp')
print(problem.render())
tmp = problem.edge_weights
G = []
for i in range(17):
    G.append(tmp.pop(0)+tmp.pop(0))
print(G)

# G = [[-1,1,1,-1],
#      [-1,-1,1,2],
#      [-1,-1,-1,1],
#      [1,-1,-1,-1],]

n = 17  #* Nombre de sommets 
A = 0   #* Le point de départ 

print(BB(G,A,n))