from __future__ import print_function
from math import sqrt

def initialise():
    # Width, length, height
    grid = [[["." for i in range(2)] for j in range(7)] for k in range(7)]

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

def printgrid(grid, z):
    for j in range (len(grid)):
        for i in range (len(grid[0])):
            print(grid[j][i][z], end=' ')
        print('')

def calc_admissable(path_length, xn, yn, zn, xd, yd, zd):
    return (sqrt(((xn-xd)**2)+((yn-yd)**2)+((zn-zd)**2)) + path_length + 1)

initialise()
