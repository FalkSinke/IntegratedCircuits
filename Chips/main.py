from __future__ import print_function
import Queue as Q
import copy
from math import sqrt

x_max = 6
y_max = 6
z_max = 1

def main():
    grid = initialise()
    printgrid(grid, 0)
    print('')
    a_star(grid, [1, 1, 0], [2, 5, 0])

def initialise():
    # Width, length, height
    grid = [[["." for i in range(z_max+1)] for j in range(x_max+1)] for k in range(y_max+1)]

    with open("coordinates_test.txt") as f:
        for line in f.read().split():
            array = line.split(",")
            name = array[0]
            x = int(array[1])
            y = int(array[2])
            print(x, y)
            grid[x][y][0] = name
    return grid

def printgrid(grid, z):
    for j in range (len(grid)):
        for i in range (len(grid[0])):
            print(grid[j][i][z], end=' ')
        print('')

def options(grid, point):
    options = []

    x = point[0]
    y = point[1]
    z = point[2]

    if x != x_max and grid[x+1][y][z] == '.':
        options.append([x+1, y, z])
    if x!= 0 and grid[x - 1][y][z] == '.':
        options.append([x - 1, y, z])
    if y != y_max and grid[x][y+1][z] == '.':
        options.append([x, y+1, z])
    if y != 0 and grid[x][y-1][z]:
        options.append([x, y-1, z])
    if z != z_max and grid[x][y][z+1] == '.':
        options.append([x, y, z+1])
    if z != 0 and grid[x][y][z-1] == '.':
        options.append([x, y, z-1])

    print(options)

    return options

#Calculates total path length from A to B going by point n + 1
def calc_admissable(path_length, a, b):
    return path_length + abs(a[0] - b[0]) + abs(a[1]-b[1]) + \
           abs(a[2] - b[2])

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


def find_route(grid, a, b):
    path_length = 0
    options2 = options(grid, a)
    best_step = [calc_admissable(path_length, options2[0], b), options2[0]]
    for i in options2:
        admissable = calc_admissable(path_length, i, b)
        if admissable < best_step[0]:
            best_step[1] = i
            best_step[0] = admissable
    print(best_step)

def a_star(grid, a, b):
    prioq = Q.PriorityQueue()
    admissable = calc_admissable(0, a, b)
    visited = []
    prioq.put((admissable, [a])

    while prioq.qsize() != 0:
        current = prioq.get()
        current_path = current[1]
        if(current_path[-1] == b):
            return current_path
        options = options(grid, current_path[-1])
        for i in options:
            if(i not in visited):
                visited.append(i)
                admissable = calc_admissable(i, b)
                path = copy.copy(current_path)
                next_path = path.append(i)
                prioq.put((admissable + len(current_path), next_path))


main()
