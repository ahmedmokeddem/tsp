import numpy as np
import matplotlib.pyplot as plt


def plot_3d_surface(x, y, z, x_label, y_label, z_label, graph_name, show=True, save=False):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(x, y, z)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_zlabel(z_label)
    ax.set_title(graph_name)
    
    if save:
        plt.savefig(graph_name+".png")
    if show:
        plt.show()



def plot_contour(x, y, z, x_label, y_label, graph_name, show=True, save=False):
    plt.contourf(x, y, z)
    plt.colorbar()
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(graph_name)
    
    if save:
        plt.savefig(graph_name+".png")
    if show:
        plt.show()


def plot_heatmap(x, y, z, x_label, y_label, graph_name, show=True, save=False):
    plt.imshow(z, extent=[min(x), max(x), min(y), max(y)], origin='lower', aspect='auto')
    plt.colorbar()
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(graph_name)
    
    if save:
        plt.savefig(graph_name+".png")
    if show:
        plt.show()


def plot_scatter(x, y, z, x_label, y_label, graph_name, show=True, save=False):
    plt.scatter(x, y, c=z, cmap='viridis')
    plt.colorbar()
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(graph_name)
    if save:
        plt.savefig(graph_name+".png")   
    if show:
        plt.show()


# Example usage
N = 100
x = np.random.rand(N)
y = np.random.rand(N)
X, Y = np.meshgrid(x, y)
Z = X + Y  
# to not to displaye set show=False, to save set save=True
plot_3d_surface(x, y, Z, "Param x", "Param Y", "Param Z", "Graph 1"?)
plot_contour(x, y, Z, "Param x", "Param Y", "Graph 2")
plot_heatmap(x, y, Z, "Param x", "Param Y", "Graph 3")
plot_scatter(X.flatten(), Y.flatten(), Z.flatten(), "Param x", "Param Y", "Graph 4")
