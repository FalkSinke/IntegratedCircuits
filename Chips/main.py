from __future__ import print_function

def initialise():
    # Width, length, height
    grid = [[[0 for i in range(6)] for j in range(7)] for k in range(2)]

    with open("coordinates_test.txt") as f:
        for line in f.read().split():
            name = line.split(",")
            x = line.split(",")
            y = line.split(",")
            grid[x][y][0] = name

    print(grid)

initialise()