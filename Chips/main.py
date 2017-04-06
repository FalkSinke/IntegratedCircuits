from __future__ import print_function

def initialise():
    # Width, length, height
    grid = [[["." for i in range(2)] for j in range(7)] for k in range(7)]

    with open("coordinates_test.txt") as f:
        for line in f.read().split():
            array = line.split(",")
            name = array[0]
            x = int(array[2])
            y = int(array[1])
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

initialise()
