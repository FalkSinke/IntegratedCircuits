#Make both same if you only want to run one single heat value
start_heatvalue = 0
final_heatvalue = 0

# Amount of iterations to be performed, value 1 will run the original txt
# order only
amount_of_iterations = 1

# Set on True if normal netlist is used (netlist_1.txt etc)
# Output file converted to a netlist file usually have +1 to gates,
# so set this one to False if using a own created netlist.
original_netlist = True

# Name of netlist used
used_netlist = 'netlists/netlist_1.txt'

# Enable when running in python2 (or pypy when going for performance)
python2 = False

# Set True if you want perform 3d plotting at the end of the coordinates
set_plotting = True
# Determine the max heigh of paths plotting
plotheight = 7
# Enable plotting of the heatmap at the end REQUIRES plot.ly
plot_heatmap = False


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
