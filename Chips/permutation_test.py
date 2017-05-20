from __future__ import print_function
import Queue as Q
import copy
import matplotlib.pyplot as plt
import random
from variables import *
from math import sqrt
import a_star as a
import cProfile

def main():
    values = []
    heatvals = []
    highestpos = []
    penalty_grid = []
    failed_pathlist = []
    highestscore = 0
    total_length = 0
    best_pathlist = []
    best_permutation = []
    results = []
    best_length = 0
    counter = 0
    best_heat = 0
    with open(used_netlist) as netlist:
        permutation = []
        for line in netlist.read().split():
            counter += 1
            array = line.split(",")
            array[0] = str(int(array[0]) + 1)
            array[1] = str(int(array[1]) + 1)
            permutation.append(tuple(array))
<<<<<<< HEAD
    for i in range(0,100):
        for heat in range(5,30):
=======
    for i in range(0,41):
        for heat in range(0,31):
>>>>>>> 2cb60be7b908363e8017f8ecf20a72ed43c83139
            grid, points = a.initialise()
            penalty_grid = a.initialise_penalty_grid(points, heat)
            succes = 0
            pathlist = []
            total_length = 0
            optim_length = 0
            for net in permutation:
                path = a.a_star(grid, penalty_grid, points[net[0]], points[net[1]])
                if len(path) > 0:
                    a.printpath(grid, path, '*')
                    pathlist.append(path)
                    total_length += (len(path) - 1)
                    succes += 1
                #else:
                #    failed_path = [points[str(int(array[0]) + 1)], points[str(int(array[1]) + 1)]]
                #    failed_pathlist.append(failed_path)
            #values.append(succes)
            #heatvals.append(heat)
            #highestpos.append(counter)
            if succes > highestscore:
                best_pathlist, best_length = optimize_astar(pathlist, grid, points)
                highestscore = succes
                best_permutation = copy.copy(permutation)
                best_heat = heat
                print("Highest score so far =", highestscore)
                print("Permutation:", i)
                print("Heat:", heat)
                print(succes, "/", counter)
                print("total length =", total_length)
                print("optimalized =", best_length)
                print(best_permutation)
                print('')
            elif succes == highestscore:
                pathlist, optim_length = optimize_astar(pathlist, grid, points)
                if (optim_length < best_length) or (best_length == 0):
                    best_pathlist = pathlist
                    best_length = optim_length
                    best_permutation = copy.copy(permutation)
                    best_heat = heat
                    print("Found shorter path")
                    print("Highest score so far =", highestscore)
                    print("Permutation:", i)
                    print("Heat:", heat)
                    print(succes, "/", counter)
                    print("total length =", total_length)
                    print("optimized =", optim_length)
                    print(best_permutation)
                    print('')

            else:
                print(i, heat)
            results.append((heat, succes,total_length))
        random.shuffle(permutation)
<<<<<<< HEAD
    optimized_pathlist, optimized_length = optimize_astar(pathlist, grid, points)
    while optimized_length < best_length:
        print("New best length =", best_length)
        best_length = optimized_length
        pathlist = optimized_pathlist
        optimized_pathlist, optimized_length = optimize_astar(pathlist, grid, points)
    file = open("results.txt", "w")
    file.write("heat, value, length\n")
    for heatval, resval, length in results:
        file.write(str(heatval) + " " + str(resval) + " " +  str(length) +"\n")
=======

    with open("results.txt", "w") as file:
        file.write("heat, value, length\n")
        for heatval, resval, length in results:
            file.write(str(heatval) + " " + str(resval) + " " +  str(length) +"\n")
>>>>>>> 2cb60be7b908363e8017f8ecf20a72ed43c83139

        file.write("\nFINAL RESULT:" + str(highestscore) + "\n")
        file.write("heat: " + str(best_heat) + "\n")
        file.write("length: " + str(best_length) + "\n")
        file.write(str(best_permutation) + "\n")
        file.close()

    #line1, line2 = plt.plot(heatvals, values, heatvals, highestpos)
    #plt.setp(line1, color='#51CD83', ls='--')
    #plt.setp(line2, color='#FC0057', ls='-')
    #plt.ylabel('wires')
    #plt.xlabel('heatvalue')
    #plt.show()
    print("HIGHSCORE =", highestscore)
    print(best_permutation)
    print("Best heat:", best_heat)
    print("Best length:", best_length)

def optimize_astar(pathlist, grid, points):
    penaltygrid_zero = a.initialise_penalty_grid(points, 0)
    new_pathlist = []
    length = 0
    for path in pathlist:
        a.printpath(grid, path, '.')
        new_path = a.a_star(grid, penaltygrid_zero, path[0], path[-1])
        length += (len(new_path) - 1)
        new_pathlist.append(new_path)
        a.printpath(grid, path, '*')
    return (new_pathlist, length)


main()



#cProfile.run('main()')
