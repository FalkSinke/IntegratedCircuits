from __future__ import print_function
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from variables import *

def plotting_3d(pathlist, points):
    color1='#000000'
    color = '#18c4ff'
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    axes = plt.gca()
    #axes.axis('equal')
    axes.set_xlim([0, x_max])
    axes.set_ylim([0, y_max])
    axes.set_zlim([0, plotheight])

    ax.w_xaxis.set_pane_color((1.0, 1.0, 1.0, 1.0))
    ax.w_yaxis.set_pane_color((1.0, 1.0, 1.0, 1.0))
    ax.w_zaxis.set_pane_color((1.0, 1.0, 1.0, 1.0))

    axes.set_autoscale_on(False)
    ax.set_xticks([i for i in range(x_max)])
    ax.set_yticks([j for j in range(y_max)])
    ax.set_zticks([k for k in range(plotheight + 1)])

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
