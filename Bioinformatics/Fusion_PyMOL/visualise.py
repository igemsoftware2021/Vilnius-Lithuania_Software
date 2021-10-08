#!/usr/bin/env python
import pymol

from functions import parse_parameters, color_fusion, calculate_distance

# Script that colors the residues of the active site and linker in fusion
# protein system

# usage: pymol visualise.py -- param.txt
# param.txt - parameter file that contains values:
#   * fusion protein system file name (.pdb)
#   * templates of the first and second proteins (.pdb)
#   * lengths of the first and second proteins (.pdb)
#   * active site residues of the first and second proteins (.pdb)
#   * linker sequence
#   * number of linker repeats
#   * hex codes of the colors in the palette
# More information about the format of parameters file can be found: https://github.com/iGEM-Vilnius/Bioinformatics/tree/master/Fusion_PyMOL

# Parse parameters
class Parameters():
    pass

par = Parameters()
par.obj_name = 'fusion'

parse_parameters.parse_parameters(sys.argv[1], par)

# Perform coloring
color_fusion.color_fusion(par)

# Structural alignment with homologs
color_fusion.load_templates(par)
