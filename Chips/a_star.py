from __future__ import print_function
import queue as Q
import copy
import matplotlib.pyplot as plt
import plotting3d
import a_star as a
from math import sqrt
import cProfile

from variables import *

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
