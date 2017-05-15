from __future__ import print_function
import queue as Q
import copy
import matplotlib.pyplot as plt
import random
from variables import *
from math import sqrt
import a_star as a
# import cProfile

def main():
    values = []
    heatvals = []
    highestpos = []
    penalty_grid = []
    failed_pathlist = []
    highestscore = 0
    total_length = 0
    best_pathlist = []
    best_length = -1
    counter = 0
    with open(used_netlist) as netlist:
        permutation = []
        for line in netlist.read().split():
            counter += 1
            array = line.split(",")
            permutation.append(array)
        init = initialise()
        grid = init[0]
        points = init[1]
    for i in range(0,2):
        for heat in range(0, 15):
            penalty_grid = a.initialise_penalty_grid(points, heat)
            succes = 0
            pathlist = []
            total_length = 0
            for net in permutation:
                path = a.a_star(grid, penalty_grid, points[str(int(net[0]) + 1)], points[str(int(net[1]) + 1)])
                a.printpath(grid, path, '*')
                if len(path) > 0:
                    pathlist.append(path)
                    total_length += (len(path) - 1)
                    succes = succes + 1
                else:
                    failed_path = [points[str(int(array[0]) + 1)], points[str(int(array[1]) + 1)]]
                    failed_pathlist.append(failed_path)
        #values.append(succes)
        #heatvals.append(heat)
        #highestpos.append(counter)
            if succes > highestscore:
                best_pathlist = pathlist
                print("Highest score so far =", highestscore)
                print("Permutation:", i)
                print("Heat:", heat)
                print(succes, "/", counter)
                best_length = total_length
                highestscore = succes
                print("total length =", total_length)
                print('')
            if succes == highestscore:
                pathlist, total_length = optimize_astar(best_pathlist, grid, points)
                if (total_length < best_length) or (best_length < 0):
                    best_pathlist = pathlist
                    print("Highest score so far =", highestscore)
                    print("Permutation:", i)
                    print("Heat:", heat)
                    print(succes, "/", counter)
                    print('')
                    best_length = total_length
                    print("total length =", total_length)
        random.shuffle(permutation)
            #line1, line2 = plt.plot(heatvals, values, heatvals, highestpos)
            #plt.setp(line1, color='#51CD83', ls='--')
            #plt.setp(line2, color='#FC0057', ls='-')
            #plt.ylabel('wires')
            #plt.xlabel('heatvalue')
            #plt.show()
    print("HIGHSCORE =", highestscore)
    print(best_pathlist)

def optimize_astar(pathlist, grid, points):
    number_of_paths = len(pathlist)
    penaltygrid_zero = a.initialise_penalty_grid(points, 0)
    total_length1 = 0
    while number_of_paths != 0:
        current_path = pathlist.pop(0)
        a.printpath(grid, current_path, '.')
        adjusted_path = a.a_star(grid, penaltygrid_zero, current_path[0], current_path[-1])
        #adjusted_path = remove_duplicates(adjusted_path)
        length_adjusted_path = len(adjusted_path)
        if length_adjusted_path < len(current_path):
            pathlist.append(adjusted_path)
            total_length1 += length_adjusted_path
        else:
            pathlist.append(current_path)
            total_length1 += len(current_path)
        number_of_paths -= 1
    return (pathlist, total_length1)
    #print("New total length =", total_length1)
    #print(pathlist)


def initialise():
    # Width, length, height
    grid = [[["." for i in range(z_max+1)] for j in range(y_max+1)] for k in range(x_max+1)]

    dict = {}

    with open(coordinates) as f:
        for line in f.read().split():
            array = line.split(",")
            name = array[0]
            x = int(array[1])
            y = int(array[2])
            # print(x, y)
            grid[x][y][0] = name
            dict[name] = [x, y, 0]
    return (grid, dict)

def remove_duplicates(path_duplicates):
    path_singles = []
    for i in path_duplicates:
        if i not in path_singles:
            path_singles.append(i)
    return path_singles

main()



# cProfile.run('main()')
