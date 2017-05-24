'''
First test version:
x_max = 6
y_max = 6
z_max = 1
'''

<<<<<<< HEAD
used_netlist = 'netlist_2.txt'
=======
used_netlist = 'netlist_1.txt'
>>>>>>> 788d50e72001626c012e11c257c7a7d900bb3dff

if ('1' in used_netlist) or ('2' in used_netlist) or ('3' in used_netlist):
    print('netlist1-3')
    coordinates = 'coordinates_netlist1.txt'
    x_max = 17
    y_max = 12
    z_max = 7
elif ('test' in used_netlist):
    coordinates = 'coordinates_test.txt'
    x_max = 6
    y_max = 6
    z_max = 1
else:
    coordinates = 'coordinates_netlist4.txt'
    x_max = 17
    y_max = 16
    z_max = 7
