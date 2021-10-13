#!/usr/bin/perl

use strict;
use warnings;

# The script that generates protein_solvate_ions.gro file to check how many atoms
# the system contains.

my $input = shift @ARGV;

`mv $input protein_or.pdb`;

# Preparing protein file
`grep -v HETATM protein_or.pdb > protein.pdb`;

# Converting PDB to gmx and generating topology
# -ignh - ignores hydrogen atoms that are in the coordinate file
my $pdb2gmx = 'gmx pdb2gmx -f protein.pdb -o protein.gro -p protein.top -ignh -ff amber94 -water tip3p';
system $pdb2gmx;
# Recommended force-field: AMBER94
# Recommended water model: TIP3 (chosen accordingly to force-field)

# Defining a box
# -c used to keep protein in the center of the box
# -d determines distance of protein from the box edges
# -bt box type
my $editconf = 'gmx editconf -f protein.gro -o protein_box.gro -c -d 1.2 -bt dodecahedron';
system $editconf;

# Solvating the protein
# -cp configuration of protein
# -cs configuration of solvent (inner part of GROMACS)
my $solvate = 'gmx solvate -cp protein_box.gro -cs spc216.gro -o protein_solvate.gro -p protein.top';
system $solvate;

# Adding ions to neutralize the system
# ions.mdp file initially downloaded from https://bitbucket.org/Bioinformatics-Review/md-simulation-files/raw/8f54e7a38b392f78f606bffb102e8e15757fbbb8/ions.mdp
my $grompp = 'gmx grompp -f ions.mdp -c protein_solvate.gro -p protein.top -o ions.tpr';
system $grompp;
# -neutral adds enough ions to neutralize the system
# Selecting Group 13 - SOL
my $genion = 'echo SOL | gmx genion -s ions.tpr -o protein_solvate_ions.gro -pname NA -nname CL -conc 0.15 -neutral -p protein.top';
system $genion;
