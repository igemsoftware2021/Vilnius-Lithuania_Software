# EFBAScore

# Intro:

This is an implementation of the scoring function for aptamers based the article "Entropic Fragment-Based Approach to Aptamer Design".

This software was written as part of the 2021 iGEM team's Vilnius-Lithuania project. Please check out our [wiki](https://2021.igem.org/Team:Vilnius-Lithuania) for more information.

# Requirements:
The program was tested on a Linux machine (Manjaro).

The machine should have a GPU installed, otherwise the program will run extremely slowly. The program was tested on a machine with the following specifications:

GPU - NVIDIA® GeForce® GTX 1650; 4GB

CPU - AMD Ryzen 5 4600H

RAM - 8GB

# Installation:
The program uses OpenMM to compute potential energies of the complex and AmberTools to prepare .pdb files for molecular dynamics calculations.

Both of these programs need to be installed, this can be done using Anaconda. We recommend using [miniconda](https://docs.conda.io/en/latest/miniconda.html) as it is less bloat. 

OpenMM can be installed by learning how to do that at the offical [OpenMM](https://openmm.org/) website or running:

`conda install -c conda-forge openmm`

Instruction is also applied for [AmberTools](https://ambermd.org/AmberTools.php):

`conda install -c conda-forge ambertools=21 compilers`

Additionally, the program uses the following Python packages (all can be installed using conda):

1. Numpy
2. Scipy
3. Pexpect

Due to Pexpect dependency the program will not work on Windows. 
If it is required to run the program on Windows, the functions in `functions/generateAmberFiles.py` must be edited, thus they would use the [Pexpect API for Windows](https://pexpect.readthedocs.io/en/stable/overview.html#pexpect-on-windows).

# Usage:
Call: 

`python EFBAScore.py -h`

for the help screen.

You can benchmark the program on your system by running it with the sample .pdb and .fasta files provided by running: 

`python EFBAScore.py genes.fasta example.pdb -o output.pdb`

# Troubleshooting:
The program will not work on Windows! If you want it to run on Windows, you need to edit the functions in `functions/generateAmberFiles.py` to use the Pexpect API for Windows.

Getting .pdb files to work for MD simulations can be challenging.

Firstly, make sure that there are no hydrogens or water molecules in your .pdb file. This can be checked and edited using [PyMOL](https://pymol.org/2/) or other molecular visualisation program.

In PyMOL it could be done by entering the following commands into the PyMOL console:  
`load [path to your target .pdb file]`  
`remove solvent`

You should check that you are able to run the following commands on your .pdb file in leap in order to make sure that your .pdb file is fine:

1. If you have installed AmberTools through conda, you should be able to open the Leap program by running `tleap` in your terminal
2. Run `source leaprc.protein.ff14SB`
3. Run `source leaprc.DNA.OL15`
4. Run `source leaprc.gaff`
5. Run `set default PBradii mbondi2`
6. Run `target = loadpdb your_target_pdb_file.pdb`
7. `saveamberparm target target.prmtop target.inpcrd`

If leap generates the two files `target.prmtop` and `target.inpcrd,` you should be ready run our program without any problems.

If you experience issues, there is a program [pdbfixer](https://github.com/openmm/pdbfixer) that might be able to help. However, if none of the suggestions help, we recommend to search for the error messages. Most of the time it takes usually around 15 minutes to get your .pdb file to run.

# References:
* Tseng, C.-Y., Ashrafuzzaman, M., Mane, J. Y., Kapty, J., Mercer, J. R., & Tuszynski, J. A. (2011). Entropic Fragment-Based Approach to Aptamer Design. Chemical Biology & Drug Design, 78(1), 1–13. doi:10.1111/j.1747-0285.2011.01125.x 
