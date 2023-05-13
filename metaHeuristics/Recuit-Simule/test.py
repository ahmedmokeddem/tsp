from Benchmark import test_RS
from RS import tspSimulatedAnnealing
from tunning import plot_line,contour_plot,plot_hist_delta,get_mean_delta
import math 

AVG_DELTA = 1127

# Compute delta params 
def delta_estim():
    values_initial_temperature = [25,50,100,150,200,250,300,350,400,450,500,550,1000,1500,2000,2500,3000,3500,4000,5000,6000,8000,9000,10000,11000,12000,13000,14000,15000]
    values_cooling_rate = [0.9,0.8,0.85,0.7,0.75,0.95]
    values_num_iteration =[10000]
    values_nb_iterations_cooling =[10]
    print(get_mean_delta('./results/ouss/delta/delta_distribution.txt'))
    plot_hist_delta('./results/ouss/delta/delta_distribution.txt','./results/ouss/delta/delta_distribution.png')

if  __name__ == "__main__" :
    benchmark = "ft53"
    p_values = [0.6,0.7,0.75,0.8,0.85,0.9,0.91,0.92,0.93,0.94,0.95,0.96,0.97,0.98,0.99]
    values_initial_temperature = [-AVG_DELTA/math.log(p) for p in p_values]
    values_cooling_rate = [0.6,0.7,0.75,0.8,0.85,0.9,0.91,0.92,0.93,0.94,0.95,0.96,0.97,0.98,0.99]
    values_num_iteration =[50000]
    values_nb_iterations_cooling =[5]
    filename = './results/ouss/tmp2_p_16_col_rate_16_50000_iter_nb_col_5.csv'
    test_RS(benchmark,values_initial_temperature, values_cooling_rate, values_num_iteration, values_nb_iterations_cooling ,filename,nb_executions=1)
    # plot_line('NB Iterations','average %',filename,'./results/ouss/plots/test_nb_iter.png')
    contour_plot('Initiale Temperature','Cooling Rate','average %',filename,'./results/ouss/plots/tmp2_p_16_col_rate_16_50000_iter_nb_col_5.png')



    # T0 tuniing
    # delta_estim()


#? Tunning steps
# #! Tunning temperature and cooling rate  
#Ste9 01
"""
    p_values = [0.6,0.7,0.75,0.8,0.85,0.9,0.91,0.92,0.93,0.94,0.95,0.96,0.97,0.98,0.99]
    values_initial_temperature = [-AVG_DELTA/math.log2(p) for p in p_values]
    values_cooling_rate = [0.6,0.7,0.75,0.8,0.85,0.9,0.91,0.92,0.93,0.94,0.95,0.96,0.97,0.98,0.99]
    values_num_iteration =[50000]
    values_nb_iterations_cooling =[5]

"""

