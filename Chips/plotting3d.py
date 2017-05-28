from __future__ import print_function
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from variables import *

def plotting_3d(pathlist, points):
    color1='#FF0058'
    color = '#51CD83'
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    axes = plt.gca()
    axes.set_xlim([0, x_max])
    axes.set_ylim([0, y_max])
    axes.set_zlim([0, z_max])
    axes.set_autoscale_on(False)
    #xticks([0, 1, 2, 3])
    for gate in points:
        #print(gate)
        ax.scatter(points[gate][0], points[gate][1], c=color1, marker='o')
    for path in pathlist:
        X = []
        Y = []
        Z = []
        #set_markeredgecolor(color1)
        #ax.scatter(path[0][0], path[0][1], c=color1, marker='o')
        #ax.scatter(path[-1][0], path[-1][1], c=color1, marker='o')
        for coordinate in path:
            X.append(coordinate[0])
            Y.append(coordinate[1])
            Z.append(coordinate[2])

        ax.plot_wireframe(X, Y, Z, color=color)
    plt.axis([0, x_max, 0, y_max])
    plt.show()
