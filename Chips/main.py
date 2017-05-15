from __future__ import print_function
import queue as Q
import copy
import matplotlib.pyplot as plt
import plotting3d
import a_star as a
from math import sqrt
import cProfile

from variables import *

def main():
    values = []
    heatvals = []
    highestpos = []
    pathlist = []
    penalty_grid = []
    failed_pathlist = []
    total_length = 0
    for heat in range(0,15):
        total_length = 0
        init = initialise()
        grid = init[0]
        points = init[1]
        penalty_grid = a.initialise_penalty_grid(points, heat)
        with open(used_netlist) as netlist:
            counter = 0
            succes = 0
            for line in netlist.read().split():
                array = line.split(",")
                path = a.a_star(grid, penalty_grid, points[str(int(array[0]) + 1)], points[str(int(array[1]) + 1)])
                a.printpath(grid, path, '*')
                if len(path) > 0:
                    pathlist.append(path)
                    total_length += (len(path) - 1)
                    succes = succes + 1
                    #print(array[0], array[1])
                else:
                    failed_path = [points[str(int(array[0]) + 1)], points[str(int(array[1]) + 1)]]
                    failed_pathlist.append(failed_path)
                counter = counter + 1
                #print(str(int(array[0]) + 1), str(int(array[1]) + 1))
                #a.printgrid(grid, 0)
                #a.printgrid(grid, 1)
            #a.printgrid(grid, 7)
        values.append(succes)
        heatvals.append(heat)
        highestpos.append(counter)
        print("Heat:", heat)
        print(succes,  "/", counter)
        print('')
        print("total length =", total_length)
    #line1, line2 = plt.plot(heatvals, values, heatvals, highestpos)
    #plt.setp(line1, color='#51CD83', ls='--')
    #plt.setp(line2, color='#FC0057', ls='-')
    #plt.ylabel('wires')
    #plt.xlabel('heatvalue')
    #plt.show()
    #plotting3d.plotting_3d(pathlist)

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
       options.append([(x+1, y, z), penalty_grid[x+1][y][z]])
    if x!= 0 and grid[x-1][y][z] == '.':
        options.append([(x-1, y, z), penalty_grid[x-1][y][z]])
    if y != y_max and grid[x][y+1][z] == '.':
        options.append([(x, y+1, z), penalty_grid[x][y+1][z]])
    if y != 0 and grid[x][y-1][z] == '.':
        options.append([(x, y-1, z), penalty_grid[x][y-1][z]])
    if z != z_max and grid[x][y][z+1] == '.':
        options.append([(x, y, z+1), penalty_grid[x][y][z+1]])
    if z != 0 and grid[x][y][z-1] == '.':
        options.append([(x, y, z-1), penalty_grid[x][y][z-1]])

    return options

#Calculates total path length from A to B going by point n + 1
def calc_admissable(a, b):
    return abs(a[0] - b[0]) + abs(a[1]-b[1]) + abs(a[2] - b[2])
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
def construct_path(parents, location):
    path = []
    while parents[location] != None:
        path.append(location)
        location = parents[location]
    path.append(location)
    return path

def a_star(grid, penalty_grid, a, b):
    prioq = Q.PriorityQueue()
    admissable = calc_admissable(a, b)
    visited = set()
    prioq.put((admissable, admissable, tuple(a)))
    parents = {tuple(a) : None}

    while (prioq.qsize() != 0):
        current_score, current_admissable, current_location = prioq.get()
        if calc_admissable(current_location, b) == 1:
            return construct_path(parents, current_location)[::-1]

        possible = options(grid, penalty_grid, current_location)
        for location, k in possible:
            if (location not in visited):

                visited.add(location)
                parents[location] = current_location

                admissable = calc_admissable(location, b)
                #path = copy.copy(current_path)
                #for j in range(0,k+1):
                #    path.append(location)
                score = admissable + current_score + k + 1 - current_admissable
                prioq.put((score, admissable, location))
    #print("No solution", a, b)
    return []
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
        a.printpath(grid, path, '.')
        failed_path = failed_pathlist[counter]
        print(failed_path)
        a = failed_path[0]
        b = failed_path[1]
        print(a, "||", b)
        new_path = a_star(grid, penalty_grid, a, b)
        if new_path != []:
            counter += 1
            old_path = a_star(grid, penalty_grid, path[0], path[-1])
            if old_path != []:
                print('winwin')
                counter = number_failedpaths
        else:
            print('fail')
            while intermediate_pathlist != []:
                path1 = intermediate_pathlist[0]
                old_path1 = a_star(grid, penalty_grid, path1[0], path1[-1])
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



#cProfile.run('main()')
