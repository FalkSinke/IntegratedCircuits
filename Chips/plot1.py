'''
======================
3D surface (color map)
======================

Demonstrates plotting a 3D surface colored with the coolwarm color map.
The surface is made opaque by using antialiased=False.

Also demonstrates using the LinearLocator and custom formatting for the
z axis tick labels.
'''

from __future__ import print_function
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import numpy as np
import matplotlib.pyplot as plt
from mayavi import mlab

'''
First test version:
x_max = 6
y_max = 6
z_max = 1
'''
'''
netlist 1-3
x_max = 17
y_max = 12
z_max = 7
'''

x_max = 17
y_max = 16
z_max = 7

def penalty_x(penalty_grid, X, Y):
    return penalty_grid[X][Y][0]

def main():
    heat = 8
    init = initialise()
    grid = init[0]
    points = init[1]
    penalty_grid = initialise_penalty_grid(points, heat)

    for x in range(len(penalty_grid)):
        for y in range(len(penalty_grid[x])):
            penalties[y][x] = penalty_grid[x][y][0]

    surface_plot(penalty_grid)

    plt.show()

def surface_plot(pathlist):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    axes = plt.gca()
    axes.set_xlim([0, x_max])
    axes.set_ylim([0, y_max])
    axes.set_zlim([0, z_max])
    axes.set_autoscale_on(False)
    #xticks([0, 1, 2, 3])

    for path in pathlist:
        X = []
        Y = []
        Z = []
        color1='#FF0058'
        #set_markeredgecolor(color1)
        ax.scatter(path[0][0], path[0][1], c=color1, marker='o')
        ax.scatter(path[-1][0], path[-1][1], c=color1, marker='o')
        for coordinate in path:
            X.append(coordinate[0])
            Y.append(coordinate[1])
            Z.append(coordinate[2])
        color = '#51CD83'
        ax.plot_wireframe(X, Y, Z, color=color)
    plt.axis([0, x_max, 0, y_max])
    plt.show()

def initialise():
    # Width, length, height
    grid = [[["." for i in range(z_max+1)] for j in range(y_max+1)] for k in range(x_max+1)]

    dict = {}

    with open("coordinates_netlist4.txt") as f:
        for line in f.read().split():
            array = line.split(",")
            name = array[0]
            x = int(array[1])
            y = int(array[2])
            # print(x, y)
            grid[x][y][0] = name
            dict[name] = [x, y, 0]
    return (grid, dict)

def printpath(grid, path, icon):
    for x,y,z in path[1:]:
        grid[x][y][z] = icon

def printgrid(grid, z):
    print("layer: ", z)
    for j in range (len(grid)):
        for i in range (len(grid[0])):
            if len(str(grid[j][i][z])) == 2:
                print(grid[j][i][z], end=' ')
            else:
                print(grid[j][i][z], end='  ')
        print('')
    print('')


def initialise_penalty_grid(points_dict, heat):
    penalty_grid = [[[0 for i in range(z_max+1)] for j in range(y_max+1)] for k in range(x_max+1)]

    for x in range(len(penalty_grid)):
        for y in range(len(penalty_grid[x])):
            for z in range(len(penalty_grid[x][y])):
                for gate in points_dict:
                    distance = calc_admissable([x,y,z], points_dict[gate])
                    penalty = heat - (distance*2);
                    if penalty < 0:
                        penalty = 0
                    penalty_grid[x][y][z] += penalty

    return penalty_grid

#Calculates total path length from A to B going by point n + 1
def calc_admissable(a, b):
    return abs(a[0] - b[0]) + abs(a[1]-b[1]) + abs(a[2] - b[2])


main()