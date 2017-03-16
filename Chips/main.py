from __future__ import print_function
from math import sqrt

x_max = 6
y_max = 6
z_max = 1

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

    printgrid(grid, 0)
    print('')
    printgrid(grid, 1)

    options(grid, 1, 0, 0)


def printgrid(grid, z):
    for j in range (len(grid)):
        for i in range (len(grid[0])):
            print(grid[j][i][z], end=' ')
        print('')

def options(grid, x, y, z):
    options = []

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

#Calculates total path length from A to B going by point n
def calc_admissable(path_length, xn, yn, zn, xd, yd, zd):
    return (sqrt(((xn-xd)**2)+((yn-yd)**2)+((zn-zd)**2)) + path_length + 1)

initialise()

