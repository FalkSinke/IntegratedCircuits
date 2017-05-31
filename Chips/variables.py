# Make both same if you only want to run one single heat value
# final heatvalue is inclusive
start_heatvalue = 5
final_heatvalue = 5

# Amount of iterations to be performed, a value of 1 will run the original
# .txt permutation order.
amount_of_iterations = 1

# Set to True if normal netlist is used (netlist_1.txt, netlist_2.txt etc.)
# Original files started with gate 0, while the coordinates started at 1,
# so set this one to False if using an own created netlist.
original_netlist = False

# Name of netlist used
# Files in netlists map with _final are the best permutations we
# found, see the report for the associated heat values
used_netlist = 'netlists/netlist_1_final.txt'

# Enable when running in python2 (or pypy when going for performance)
# Dissable when running python3
python2 = False

# Set True if you want perform 3d plotting at the end of the coordinates
set_plotting = True
# Determine the max heigh of paths plotting
plotheight = 3
# Enable plotting of the heatmap at the end REQUIRES plot.ly
plot_heatmap = False

# Determine in which file you want to save the results
results_file = "results/FILENAME.txt"

# Leave as it is, describes which coordinate grid should be used
if ('1' in used_netlist) or ('2' in used_netlist) or ('3' in used_netlist):
    print('netlist1-3')
    coordinates = 'coordinates/coordinates_netlist1.txt'
    x_max = 17
    y_max = 12
    z_max = 7
elif ('test' in used_netlist):
    coordinates = 'coordinates/coordinates_test.txt'
    x_max = 6
    y_max = 6
    z_max = 1
else:
    coordinates = 'coordinates/coordinates_netlist4.txt'
    x_max = 17
    y_max = 16
    z_max = 7
