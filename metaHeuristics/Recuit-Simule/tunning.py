
import tsplib95
import time
import numpy as np
import pandas as pd
import csv
import pandas as pd
import matplotlib.pyplot as plt
import itertools

columns = ["Initiale Temperature","Cooling Rate","NB Iterations","NB Iterations cooling","average %","min result","nb opt","average execution time (s)"]
def plot_line(param1,param2,filename,pngfile):

    # Load data from CSV file
    data = pd.read_csv(filename)
    print(data)
    
    if(param1 not in columns or param2 not in columns ):
        print("params should be in {}".format(columns))
        return
    # Extract x and y values from data
    x = data[param1]
    y = data[param2]

    # Create line plot
    plt.plot(x, y)

    # Set plot title and axis labels
    plt.title('Line Plot')
    plt.xlabel('X')
    plt.ylabel('Y')

    # Show the plot
    plt.savefig(pngfile)
    plt.show()

def contour_plot(param1,param2,param3,filename,pngfile):
# Load data from CSV file
    data = pd.read_csv(filename)
    print(data)
    
    if(param1 not in columns or param2 not in columns or param3 not in columns):
        print("params should be in {}".format(columns))
        return
    # Extract x and y values from data
    # Extract x and y values from data
    x = data[param1]
    y = data[param2]

    X,Y = np.meshgrid(x.unique(), y.unique())
    # Extract z values from data
    z = data[param3].values.reshape(len(set(x)), len(set(y)))
    print(z.shape)
    print(X.shape)
    print(z.shape)

    print(x.unique().shape,y.unique().shape)
    # Create contour plot
    plt.contourf(x.unique(), y.unique(), z)
    plt.colorbar()

    # Set plot title and axis labels
    plt.title('Contour Plot')
    plt.xlabel(param1)
    plt.ylabel(param2)


    # Show the plot
    plt.savefig(pngfile)
    plt.show()



def plot_hist_delta(filename,pngfile):  
    # Load the data from the CSV file
    my_data = np.loadtxt(filename, delimiter=',')

    # Plot a histogram of the data
    plt.hist (my_data, bins=10)
    plt.xlabel('Value')
    plt.ylabel('Frequency')
    plt.title('Histogram of my_data')
    plt.savefig(pngfile)
    plt.show()


def get_mean_delta(filename):
    my_data = np.loadtxt(filename, delimiter=',')
    return np.mean(my_data)