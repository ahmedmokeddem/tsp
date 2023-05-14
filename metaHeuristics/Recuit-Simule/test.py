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

    #? interval 01 
    # p_values = [0.6,0.7,0.75,0.8,0.85,0.9,0.91,0.92,0.93,0.94,0.95,0.96,0.97,0.98,0.99]
    # values_cooling_rate = [0.6,0.7,0.75,0.8,0.85,0.9,0.91,0.92,0.93,0.94,0.95,0.96,0.97,0.98,0.99]

    
    #? OPT : For now best intervals 
    # p_values = [0.66,0.67,0.68,0.69,0.7,0.71,0.72]
    # values_cooling_rate = [0.55,0.555,0.6,0.61,0.625,0.65,0.7]
    # values_initial_temperature = [-AVG_DELTA/math.log(p) for p in p_values]
    # values_num_iteration =[200000]
    # values_nb_iterations_cooling =[1]
    # * Init : PPV 

    #? Top intervals 
        # p_values = [0.655,0.66,0.665,0.67,0.675,0.68,0.685,0.69,0.695]
        # values_cooling_rate = [0.59,0.595,0.6,0.605,0.61,0.615,0.62,0.625,0.63]
        # values_initial_temperature = [-AVG_DELTA/math.log(p) for p in p_values]
        # values_num_iteration =[200000]
        # values_nb_iterations_cooling =[1]

    #? Top Combinations : PPV init
    # Step1_test_Single_1
    #   0.66 0.65 200000 1   50 exec avg 26% [15-35] Single 1 (34 init -> 26 )
    #   0.66 0.65 400000 1   50 exec avg 27%   [18-38]   Single 2
    #   0.675 0.6155 200000 1   50 exec avg 27%  [17 - 45]  Single 3

    #? Top Combinations : Rand Init 
    # Step1_test_Single_1_rand
    #   0.66 0.65 200000 1   50 exec avg 55% [44-64] Single 1 (277 init -> 55 )




    p_values = [0.66 for i in range(50)]
    values_cooling_rate = [ 0.65]
    values_initial_temperature = [-AVG_DELTA/math.log(p) for p in p_values]
    values_num_iteration =[200000]
    values_nb_iterations_cooling =[1]


    #! change file name 
    filename = './results/ouss/Opt_test_rand.csv'
    test_RS(benchmark,values_initial_temperature, values_cooling_rate, values_num_iteration, values_nb_iterations_cooling ,filename,nb_executions=5)
    # plot_line('NB Iterations','average %',filename,'./results/ouss/plots/Test_NB_iter_0.66_0.65.png')
    # contour_plot('Initiale Temperature','Cooling Rate','average %',filename,'./results/ouss/plots/Step1_test_8.png')



    # T0 tuniing
    # delta_estim()

