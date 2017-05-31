This code is written by:
Claartje Barkhof
Falk Sinke
Lucas Fijen

It has been written for the subject Heuristieken at the UvA.
This code is an atempt to resolve the constraint optimalisation problem
found in chips production.

main.py should be ran to run the code. Variables can be changed in
variables.py in order to enable certain functions.

The code can be run with python2, python3 and pypy, as long as you change
the setting in variables.py

To create a visualisation of the heatmap, plot.ly is required.
Also matplotlib is required for the normal plots

List of libraries used:
- The Python Standard library
- MatplotLib 2.0.2
- Plot.ly 2.0.8

We used the following hardware to run this code:
A MacBook Pro running macOS Sierra 10.12.1 with a 2,4 GHz Intel Core i5
processor and 4 GB DDR3 RAM, a MacBook Pro running OS X El Capitan 10.11.5
with a 2GHz Intel Core i7 processor and 8 GB DDR3 RAM and a HP EliteBook 8570W
running Ubuntu 16.04LTS with a 2,4 GHz intel i7 and 8GB DDR3 RAM.

Using pypy the code should run in about 0.5-1 second per heat, depending on
the netlist used.

Please read the details in variables.py for more explaination of the
optional functions
