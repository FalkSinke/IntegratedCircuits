from __future__ import print_function
import Queue as Q
import copy
from math import sqrt

'''
First test version:
x_max = 6
y_max = 6
z_max = 1
'''

x_max = 17
y_max = 12
z_max = 7

def main():
    init = initialise()
    grid = init[0]
    points = init[1]
    penalty_grid = initialise_penalty_grid(points)
    printgrid(penalty_grid, 0)
    printgrid(grid, 0)
    with open("netlist_1.txt") as netlist:
        counter = 0
        for line in netlist.read().split():
            array = line.split(",")
            printpath(grid, a_star(grid, penalty_grid, points[array[0]], points[array[1]]), '*')
            counter = counter + 1
            printgrid(grid, 0)
            printgrid(grid, 1)


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
            print(x, y)
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
            print(grid[j][i][z], end=' ')
        print('')
    print('')

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

def initialise_penalty_grid(points_dict):
    penalty_grid = [[[0 for i in range(z_max+1)] for j in range(y_max+1)] for k in range(x_max+1)]
    heat = 10

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
        options.append([[y+1, y, z], penalty_grid[y+1][y][z]])
    if y != 0 and grid[x][y-1][z] == '.':
        options.append([[y-1, y, z], penalty_grid[y-1][y][z]])
    if z != z_max and grid[x][y][z+1] == '.':
        options.append([[z+1, y, z], penalty_grid[z+1][y][z]])
    if z != 0 and grid[x][y][z-1] == '.':
        options.append([[z-1, y, z], penalty_grid[z-1][y][z]])

    return options

#Calculates total path length from A to B going by point n + 1
def calc_admissable(a, b):
    return abs(a[0] - b[0]) + abs(a[1]-b[1]) + abs(a[2] - b[2])

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

def a_star(grid, penalty_grid, a, b):
    prioq = Q.PriorityQueue()
    admissable = calc_admissable(a, b)
    visited = []
    prioq.put((admissable, [a]))

    while (prioq.qsize() != 0):
        current = prioq.get()
        current_path = current[1]
        if calc_admissable(current_path[-1], b) == 1:
            print(current_path)
            return current_path

        possible = options(grid, penalty_grid, current_path[-1])
        for i, k in possible:
            if (i not in visited):
                visited.append(i)
                admissable = calc_admissable(i, b)
                path = copy.copy(current_path)
                for j in range(0,k):
                    path.append(i)
                prioq.put((admissable + len(path), path))
    print("No solution", a, b)

main()
