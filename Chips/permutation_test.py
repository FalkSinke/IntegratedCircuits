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
    for i in range(0,15):
        with open(used_netlist) as netlist:
            permutation = []
            for line in netlist.read().split():
                array = line.split(",")
                permutation.append(array)
            init = initialise()
            grid = init[0]
            points = init[1]
            for heat in range(0, 21):
                penalty_grid = a.initialise_penalty_grid(points, heat)
                counter = 0
                succes = 0
                pathlist = []
                total_length = 0
                #random.shuffle(permutation)
                for net in permutation:
                    path = a.a.a_star(grid, penalty_grid, points[str(int(net[0]) + 1)], points[str(int(net[1]) + 1)])
                    printpath(grid, path, '*')
                    if len(path) > 0:
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
            #values.append(succes)
            #heatvals.append(heat)
            #highestpos.append(counter)
                print(succes)
                if succes > highestscore:
                    best_pathlist = pathlist
                    print("Highest score so far =", highestscore)
                    print("Permutation:", i)
                    print("Heat:", heat)
                    print(succes, "/", counter)
                    print('')
                    best_length = total_length
                    highestscore = succes
                    print("total length =", total_length)
                if succes == highestscore:
                    if (total_length < best_length) or (best_length < 0):
                        best_pathlist = pathlist
                        print("Highest score so far =", highestscore)
                        print("Permutation:", i)
                        print("Heat:", heat)
                        print(succes, "/", counter)
                        print('')
                        best_length = total_length
                        print("total length =", total_length)
            #line1, line2 = plt.plot(heatvals, values, heatvals, highestpos)
            #plt.setp(line1, color='#51CD83', ls='--')
            #plt.setp(line2, color='#FC0057', ls='-')
            #plt.ylabel('wires')
            #plt.xlabel('heatvalue')
            #plt.show()
    print("HIGHSCORE =", highestscore)
    print(best_pathlist)
    optimize_astar(best_pathlist, grid, points)

def optimize_astar(pathlist, grid, points):
    number_of_paths = len(pathlist)
    penaltygrid_zero = a.initialise_penalty_grid(points, 0)
    total_length1 = 0
    while number_of_paths != 0:
        current_path = pathlist.pop(0)
        printpath(grid, current_path, '.')
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
    print("New total length =", total_length1)
    print(pathlist)


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

'''
def get_penalty_grid_point(grid, options):
    penalised_options = []

    for x, y, z in options:
        counter = 1
        penalty = 10
        if x != x_max and grid[x + 1][y][z].isdigit():
            counter += penalty
        if x != 0 and grid[x - 1][y][z].isdigit():
            counter += penalty
        if y != y_max and grid[x][y + 1][z].isdigit():
            counter += penalty
        if y != 0 and grid[x][y - 1][z].isdigit():
            counter += penalty
        if z != z_max and grid[x][y][z + 1].isdigit():
            counter += penalty
        if z != 0 and grid[x][y][z - 1].isdigit():
            counter += penalty

        penalised_options.append([[x, y, z], counter])

    return penalised_options
'''

'''
penalty grid DOCUMENTEREN
    - heat varieren
    - penalty functie varieren (linear/kwadratisch etc)
    - proberen met andere netlists/grids


uberhaupt documenteren van Penalty

resultaten tabel: alleen a*, met penalty (verschillende soorten), hillclimber?

'''



'''
als je snelste route van a naar b wil vinden:
    - expand naar alle richtingen (bewaar punten in visited list), als niet in visited list,
     stop al die paths in queue (met als sorteer variabele dx+dy+dz
    vanaf daar + afgelegde afstand).
    - pak eerste item uit queue en expand
    - als next step = final, dan #WIN


    python heeft prioqueue
    q.get() als q leeg, gaat oneindig lang wachten, dus check eerst of leeg

'''
'''
def fix(grid, pathlist, failed_pathlist, penalty_grid):
    print(len(pathlist))
    intermediate_pathlist = []
    number_failedpaths = len(failed_pathlist)
    counter = 0
    while (counter != number_failedpaths):
        path = pathlist[counter]
        intermediate_pathlist.append(path)
        pathlist.pop(counter)
        printpath(grid, path, '.')
        failed_path = failed_pathlist[counter]
        print(failed_path)
        a = failed_path[0]
        b = failed_path[1]
        print(a, "||", b)
        new_path = a.a.a_star(grid, penalty_grid, a, b)
        if new_path != []:
            counter += 1
            old_path = a.a_star(grid, penalty_grid, path[0], path[-1])
            if old_path != []:
                print('winwin')
                counter = number_failedpaths
        else:
            print('fail')
            while intermediate_pathlist != []:
                path1 = intermediate_pathlist[0]
                old_path1 = a.a_star(grid, penalty_grid, path1[0], path1[-1])
                if old_path1 != []:
                    pathlist.append(old_path1)
                    intermediate_pathlist.pop(0)
                    print('successs')
                else:
                    continue
    print(len(pathlist))
'''
'''
Make fix function
- pak item (path) uit pathlist, zet in intermediate list
- leg een path uit failedpathslist
- als succes leg andere

misschien eerst korte of eerst lange

'''

main()



# cProfile.run('main()')
