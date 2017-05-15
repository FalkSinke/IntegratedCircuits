from __future__ import print_function
import queue as Q
import copy
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

'''
First test version:
x_max = 6
y_max = 6
z_max = 1
'''

x_max = 17
y_max = 12
z_max = 7

'''
x_max = 17
y_max = 16
z_max = 7
'''

def main():
    values = []
    heatvals = []
    highestpos = []
    pathlist = []
    penalty_grid = []
    failed_pathlist = []
    total_length = 0
    for heat in range(7,8):
        total_length = 0
        init = initialise()
        grid = init[0]
        points = init[1]
        penalty_grid = initialise_penalty_grid(points, heat)
        #printgrid(penalty_grid, 1)
        #printgrid(grid, 0)
        #printpath(grid, a_star(grid, penalty_grid,[1,1,0], [1,5,0]), '*')
        #printgrid(grid, 0)
        #rintgrid(grid, 1)
        with open("netlist_2.txt") as netlist:
            counter = 0
            succes = 0
            for line in netlist.read().split():
                array = line.split(",")
                path = a_star(grid, penalty_grid, points[str(int(array[0]) + 1)], points[str(int(array[1]) + 1)])
                printpath(grid, path, '*')
                if len(path) > 0:
                    path = remove_duplicates(path)
                    pathlist.append(path)
                    total_length += (len(path) - 1)
                    succes = succes + 1
                    #print(array[0], array[1])
                else:
                    failed_path = [points[str(int(array[0]) + 1)], points[str(int(array[1]) + 1)]]
                    failed_pathlist.append(failed_path)
                counter = counter + 1
            #printgrid(grid, 0)
            #printgrid(grid, 1)
            #printgrid(grid, 7)
        values.append(succes)
        heatvals.append(heat)
        highestpos.append(counter)
        print("Heat:", heat)
        print(succes,  "/", counter)
        print('')
        print("total length =", total_length)
        #plt.plot(heatvals, values, '--', heatvals, highestpos, 'r-')
        #plt.show()
        #fix(grid, pathlist, failed_pathlist, penalty_grid)
        plotting_3d(pathlist)

def plotting_3d(pathlist):
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

    with open("coordinates_netlist1.txt") as f:
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

def remove_duplicates(path_duplicates):
    path_singles = []
    for i in path_duplicates:
        if i not in path_singles:
            path_singles.append(i)
    return path_singles

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

def options(grid, penalty_grid, point):
    options = []

    x, y, z = point

    if x != x_max and grid[x+1][y][z] == '.':
       options.append([[x+1, y, z], penalty_grid[x+1][y][z]])
    if x!= 0 and grid[x-1][y][z] == '.':
        options.append([[x-1, y, z], penalty_grid[x-1][y][z]])
    if y != y_max and grid[x][y+1][z] == '.':
        options.append([[x, y+1, z], penalty_grid[x][y+1][z]])
    if y != 0 and grid[x][y-1][z] == '.':
        options.append([[x, y-1, z], penalty_grid[x][y-1][z]])
    if z != z_max and grid[x][y][z+1] == '.':
        options.append([[x, y, z+1], penalty_grid[x][y][z+1]])
    if z != 0 and grid[x][y][z-1] == '.':
        options.append([[x, y, z-1], penalty_grid[x][y][z-1]])

    return options

#Calculates total path length from A to B going by point n + 1
def calc_admissable(a, b):
    return abs(a[0] - b[0]) + abs(a[1]-b[1]) + abs(a[2] - b[2])


def a_star(grid, penalty_grid, a, b):
    prioq = Q.PriorityQueue()
    admissable = calc_admissable(a, b)
    visited = set()
    prioq.put((admissable, [a]))

    while (prioq.qsize() != 0):
        current = prioq.get()
        current_path = current[1]
        if calc_admissable(current_path[-1], b) == 1:
            #print(current_path)
            current_path.append(b)
            return current_path

        possible = options(grid, penalty_grid, current_path[-1])
        for i, k in possible:
            i = tuple(i)
            if (i not in visited):
                visited.add(i)
                admissable = calc_admissable(i, b)
                path = copy.copy(current_path)
                for j in range(0,k+1):
                    path.append(i)
                prioq.put((admissable + len(path), path))
    #print("No solution", a, b)
    return []


#main()



# cProfile.run('main()')
