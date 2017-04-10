from __future__ import print_function
import queue as Q
import copy
from math import sqrt

x_max = 6
y_max = 6
z_max = 1

def main():
    init = initialise()
    grid = init[0]
    points = init[1]
    with open("netlist_test.txt") as netlist:
        counter = 0
        for line in netlist.read().split():
            array = line.split(",")
            printpath(grid, a_star(grid, points[array[0]], points[array[1]]), counter)
            counter = counter + 1
            printgrid(grid, 0)
            printgrid(grid, 1)


def initialise():
    # Width, length, height
    grid = [[["." for i in range(z_max+1)] for j in range(x_max+1)] for k in range(y_max+1)]

    dict = {}

    with open("coordinates_test.txt") as f:
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

def options(grid, point):
    options = []

    x, y, z = point

    if x != x_max and grid[x+1][y][z] == '.':
        options.append([x+1, y, z])
    if x!= 0 and grid[x - 1][y][z] == '.':
        options.append([x - 1, y, z])
    if y != y_max and grid[x][y+1][z] == '.':
        options.append([x, y+1, z])
    if y != 0 and grid[x][y-1][z] == '.':
        options.append([x, y-1, z])
    if z != z_max and grid[x][y][z+1] == '.':
        options.append([x, y, z+1])
    if z != 0 and grid[x][y][z-1] == '.':
        options.append([x, y, z-1])

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

def a_star(grid, a, b):
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

        possible = options(grid, current_path[-1])
        for i in possible:
            if (i not in visited):
                visited.append(i)
                admissable = calc_admissable(i, b)
                path = copy.copy(current_path)
                path.append(i)
                prioq.put((admissable + len(path), path))
    print("No solution", a, b)

main()
