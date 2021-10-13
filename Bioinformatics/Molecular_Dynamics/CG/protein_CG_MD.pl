#!/usr/bin/perl

use strict;
use warnings;

# Script written in regards of http://cgmartini.nl/index.php/tutorials-general-introduction-gmx5/proteins-gmx5#soluble-martini

# The script should be run in the directory where structure files are found
# Prerequisites:
# * martinize.py
# * martini_v2.2.itp file
# * dssp
# * water.gro file
# * em.mdp file
# * eq.mdp file
# * md.mdp file

my $PATH_DSSP = './dssp/mkdssp';

my $protein_file = shift @ARGV;
`cp $protein_file protein_or.pdb`;

# Generating secondary structure file for protein
`mkdssp -i protein_or.pdb -o protein_or.dssp`;

# Creating CG (coarse grained) model for protein
`python martinize.py -f protein_or.pdb -o protein.top -x protein_CG.pdb -ss protein_or.dssp -p backbone -ff elnedyn22`;

# Short minimization in vacuum
# .top file required (include the correct .tp file)
# .itp file required
# .mdp file required
`gmx editconf -f protein_CG.pdb -d 1.0 -bt dodecahedron -o protein_CG.gro`;

# Minimizing energy (log file keeps the potential energy score)
# Topology file requires martini.itp file (downloaded from: http://cgmartini.nl/images/parameters/ITP/martini_v2.2.itp)
`gmx grompp -f em.mdp -c protein_CG.gro -p protein.top -o 01-em.tpr -maxwarn 1`;
`gmx mdrun -v -deffnm 01-em -s 01-em.tpr`;

# Solvating system
# Required water.gro file: http://cgmartini.nl/images/applications/water/water.gro
`gmx solvate -cp 01-em.gro -cs water.gro -radius 0.21 -o solvated.gro`;

# Creating system.top file
`cp protein.top system.top`;
my $line = "\nW\t";
my $num_W = `grep -c W solvated.gro`;
$line .= $num_W;
open(FH, '>>', 'system.top') or die $!;
print FH $line;

# Perform minimization of solvated protein
`gmx grompp -p system.top -c solvated.gro -f em.mdp -o 02-em.tpr -maxwarn 1`;
`gmx mdrun -v -deffnm 02-em -s 02-em.tpr`;
`gmx grompp -p system.top -c 02-em.gro -f eq.mdp -o equilibration.tpr -maxwarn 1`;
`gmx mdrun -v -deffnm equilibration -s equilibration.tpr`;

# Production run
`gmx grompp -p system.top -c equilibration.gro -f md.mdp -o dynamic.tpr -maxwarn 1`;
`gmx mdrun -v -deffnm dynamic -s dynamic.tpr`;
