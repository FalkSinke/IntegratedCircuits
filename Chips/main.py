from __future__ import print_function
import copy
import random
from variables import *
import functions as a

def main():
    penalty_grid = []
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
            if original_netlist is True:
                array[0] = str(int(array[0]) + 1)
                array[1] = str(int(array[1]) + 1)
            permutation.append(tuple(array))


    for i in range(amount_of_iterations):
        for heat in range(start_heatvalue, final_heatvalue + 1):
            grid, points = a.initialise()
            penalty_grid = a.initialise_penalty_grid(points, heat)
            succes = 0
            pathlist = []
            total_length = 0
            optim_length = 0
            for net in permutation:
                path = a.a_star(grid, penalty_grid, points[net[0]], points[net[1]])
                if len(path) > 0:
                    #a.printgrid(grid, 0)
                    # for a better view on what is printed,
                    # enable this, own written visualisation
                    a.printpath(grid, path, '*')
                    pathlist.append(path)
                    total_length += (len(path) - 1)
                    succes += 1
            if succes > highestscore:
                best_pathlist, best_length = a.optimize_astar(pathlist, grid, points)
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
                pathlist, optim_length = a.optimize_astar(pathlist, grid, points)
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
                    print("Succesfully laid down ", highestscore, "paths")
                    print("Total pathlength was longer than best pathlength")
            else:
                print(i, heat)
            results.append((heat, succes, total_length))
        random.shuffle(permutation)

    # Creates the results in a final file results.txt
    with open(results_file, "w") as file:
        file.write("heat, value, non-optimised length\n")
        for heatval, resval, length in results:
            file.write(str(heatval) + " " + str(resval) + " " +  str(length) +"\n")
        file.write("\nFINAL RESULT:" + str(highestscore) + "\n")
        file.write("heat: " + str(best_heat) + "\n")
        file.write("optimised length: " + str(best_length) + "\n")
        file.write(str(best_permutation) + "\n")
        file.close()

    print("HIGHSCORE =", highestscore)
    print(best_permutation)
    print("Best heat:", best_heat)
    print("Best length:", best_length)
    if set_plotting is True:
        import plotting_paths as plotting
        plotting.plotting_3d(best_pathlist, points)
    if plot_heatmap is True:
        import plotting_heatmap as heatplot
        heatplot.main()


main()
