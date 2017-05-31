from __future__ import print_function
import copy
from math import sqrt
import cProfile
from variables import *

if python2 is True:
    import Queue as Q
else:
    import queue as Q

def initialise():
    # Width, length, height
    grid = [[["." for i in range(z_max+1)] for j in range(y_max+1)] for k in range(x_max+1)]
    diction = {}
    with open(coordinates) as f:
        for line in f.read().split():
            name, x, y = line.split(",")
            x, y = int(x), int(y)
            grid[x][y][0] = name
            diction[name] = (x, y, 0)
    return (grid, diction)

def initialise_penalty_grid(points_dict, heat):
    penalty_grid = [[[0 for i in range(z_max+1)] for j in range(y_max+1)] for k in range(x_max+1)]
    for x in range(len(penalty_grid)):
        for y in range(len(penalty_grid[x])):
            for z in range(len(penalty_grid[x][y])):
                for gate in points_dict:
                    distance = calc_admissable((x,y,z), points_dict[gate])
                    penalty = heat - (distance*2);
                    if penalty < 0:
                        penalty = 0
                    penalty_grid[x][y][z] += penalty
    return penalty_grid

def printpath(grid, path, icon):
    if len(path) > 2:
        for x,y,z in path[1:-1]:
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

def construct_path(parents, location):
    path = []
    while parents[location] != None:
        path.append(location)
        location = parents[location]
    path.append(location)
    return path

def a_star(grid, penalty_grid, a, b):
    a = tuple(a)
    b = tuple(b)
    prioq = Q.PriorityQueue()
    admissable = calc_admissable(a, b)
    visited = set()
    prioq.put((admissable, admissable, a, a))
    parents = {a : None}

    while (prioq.qsize() != 0):
        current_score, current_admissable, current_location, last_location = prioq.get()
        if current_location not in visited:
            if current_location is not a:
                visited.add(current_location)
                parents[current_location] = last_location
            if calc_admissable(current_location, b) == 1:
                parents[b] = current_location
                return construct_path(parents, b)[::-1]

            possible = options(grid, penalty_grid, current_location)
            for location, k in possible:
                admissable = calc_admissable(location, b)
                score = admissable + current_score + k + 1 - current_admissable
                prioq.put((score, admissable, location, current_location))
    return []

def optimize_astar(pathlist, grid, points):
    penaltygrid_zero = initialise_penalty_grid(points, 0)
    old_pathlist = pathlist
    length = 0
    new_length = 0
    changed = True
    while length == 0 or new_length < length:
        new_pathlist = []
        length = new_length
        new_length = 0
        for path in old_pathlist:
            printpath(grid, path, '.')
            new_path = a_star(grid, penaltygrid_zero, path[0], path[-1])
            new_length += (len(new_path) - 1)
            new_pathlist.append(new_path)
            printpath(grid, new_path, '*')
        old_pathlist = new_pathlist
    return (new_pathlist, new_length)
