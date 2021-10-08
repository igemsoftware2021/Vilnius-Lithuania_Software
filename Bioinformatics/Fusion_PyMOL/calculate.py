#!/usr/bin/env python
import pymol
import os
import subprocess

from functions import parse_parameters, color_fusion, calculate_distance

# Script that colors the residues of the active site and linker in fusion
# protein system and calculates distance between active sites

# usage: pymol calculate.py -- param.txt
# param.txt - parameter file that contains values:
#   * fusion protein system file name (.pdb)
#   * templates of the first and second proteins (.pdb)
#   * lengths of the first and second proteins (.pdb)
#   * active site residues of the first and second proteins (.pdb)
#   * linker sequence
#   * number of linker repeats
#   * hex codes of the colors in the palette
# More information about the format of parameters file can be found: https://github.com/iGEM-Vilnius/Bioinformatics/tree/master/Fusion_PyMOL

class Parameters():
    pass

par = Parameters()
par.obj_name = 'fusion'

parse_parameters.parse_parameters(sys.argv[1], par)

# Perform coloring
color_fusion.color_fusion(par)

# Calculate distance between active sites
command = "grep 'ENDMDL' "+ par.fusion_file + " | wc -l"
states = int(subprocess.getstatusoutput(command)[1])

# Choose the according method for calculation
if states > 1:
    dist = [None] * states
    print("Multiple states")
    calculate_distance.calculate_distance_multiple_states(par, dist)
else:
    dist = []
    print("One state")
    calculate_distance.calculate_distance(par, dist)

# Write distance statistics to file
calculate_distance.write_to_file(par, dist, par.output_distance_file)
