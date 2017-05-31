from __future__ import print_function
import numpy as np
import matplotlib.pyplot as plt

def main():
    heat = []
    succes = []
    length = []
    data = [[] for i in range(51)]
    with open("results.txt", "r") as f:
        for line in f:
            values = line.split()
            #print(values)
            #data[int(values[0])].append(int(values[2]) / int(values[1]))
            data[int(values[0])].append(int(values[1]))
            #heat.append(int(values[0]))
            #succes.append(int(values[1]))
            #length.append(int(values[2]))

    plt.boxplot(data)
    plt.plot([0, 51], [60, 60], 'r:')
    #plt.axis([0, 31, 0, 70])
    plt.show()
main()
