#!/usr/bin/perl

use strict;
use warnings;

# Tutorial flow from: https://bioinformaticsreview.com/20191210/tutorial-molecular-dynamics-md-simulation-using-gromacs/

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

# Energy minimization to stabilize the system and avoid steric clashes
# em.mdp file initially downloaded from https://bitbucket.org/Bioinformatics-Review/md-simulation-files/raw/8f54e7a38b392f78f606bffb102e8e15757fbbb8/em.mdp
$grompp = 'gmx grompp -f em.mdp -c protein_solvate_ions.gro -p protein.top -o em.tpr';
system $grompp;
my $mdrun = 'gmx mdrun -v -deffnm em';
system $mdrun;
# -deffnm sets default name to all output files
# Epot has to be negative
# Fmax must be less than 1000 kJ/mol/nm (set as max force in em.mdp file).

# Plotting Epot using em.edr file
# selecting type '10 0'
my $energy = 'echo 10 0 | gmx energy -f em.edr -o potential.xvg';
system $energy;

# Equilibration of ions and solvent around the protein
# bringing the system at a particular temperature at which it is simulated.
# After constant pressure is applied

# isothermal phase
# nvt.mdp file initially downloaded needed from https://bitbucket.org/Bioinformatics-Review/md-simulation-files/raw/8f54e7a38b392f78f606bffb102e8e15757fbbb8/nvt.mdp
# 100 ps is generally enough to reach 300 K temperature
$grompp = 'gmx grompp -f nvt.mdp -c em.gro -r em.gro -p protein.top -o nvt.tpr';
system $grompp;
$mdrun = 'gmx mdrun -v -deffnm nvt';
system $mdrun;

# Plotting temperature progression
# selecting type '16 0'
$energy = 'echo 16 0 | gmx energy -f nvt.edr -o temperature.xvg';
system $energy;

# isobaric phase
# npt.mdp initially downloaded file from https://bitbucket.org/Bioinformatics-Review/md-simulation-files/raw/8f54e7a38b392f78f606bffb102e8e15757fbbb8/npt.mdp
# using 100 ps timeframe for this phase too
$grompp = 'gmx grompp -f npt.mdp -c nvt.gro -r nvt.gro -t nvt.cpt -p protein.top -o npt.tpr';
system $grompp;
$mdrun = 'gmx mdrun -v -deffnm npt';
system $mdrun;

# Plotting pressure progression
# selecting type '18 0'
$energy = 'echo 18 0 | gmx energy -f npt.edr -o pressure.xvg';
system $energy;

# Plotting graph for density
# selecting type '24 0'
$energy = 'echo 24 0 | gmx energy -f npt.edr -o density.xvg';
system $energy;
# Compare the density value with experimental

# Running MD
# md.mdp file initially downloaded from https://bitbucket.org/Bioinformatics-Review/md-simulation-files/raw/8f54e7a38b392f78f606bffb102e8e15757fbbb8/md.mdp
$grompp = 'gmx grompp -f md.mdp -c npt.gro -t npt.cpt -p protein.top -o md_0_1.tpr';
system $grompp;
$mdrun = 'gmx mdrun -v -deffnm md_0_1';
system $mdrun;

# Convert trajectory file to .pdb
my $trjconv = 'gmx trjconv -s md_0_1.tpr -f md_0_1.xtc -o md.pdb';
system $trjconv;

