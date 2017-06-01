'''
Visualises a heatmap, uses variables from variables.py
Requires offline library of plot.ly to be installed!
creates a html file in this folder
'''

from __future__ import print_function
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import matplotlib.pyplot as plt
import numpy as np
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
import pandas as pd
from variables import *
import functions as a

def penalty_x(penalty_grid, X, Y):
    return penalty_grid[X][Y][0]

def main():
    init = a.initialise()
    grid = init[0]
    points = init[1]
    penalty_grid = a.initialise_penalty_grid(points, start_heatvalue)
    surface_plot(penalty_grid)

def surface_plot(penalty_grid):
    matrix = [["." for j in range(y_max+1)] for k in range(x_max+1)]
    X = []
    Y = []
    Z = []
    color1='#FF0058'

    for x in range(len(penalty_grid)):
        for y in range(len(penalty_grid[x])):
            matrix[x][y] = penalty_x(penalty_grid, x, y)
    data = [go.Surface(z=np.matrix(np.array(matrix)))]
    print(np.array(matrix))

    layout = go.Layout(
        title=used_netlist,
        #autosize=False,
        width=1000,
        height=900,
        #margin=dict(
        #    l=0,
        #    r=50,
        #    b=65,
        #    t=90
        #)
    )
    fig = go.Figure(data=data, layout=layout)
    plotly.offline.plot(fig)
