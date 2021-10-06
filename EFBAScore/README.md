# EFBAScore

# Intro:

This is an implementation of the scoring function for aptamers based the article "Entropic Fragment-Based Approach to Aptamer Design".

This software was written as part of the 2021 iGEM team's Vilnius-Lithuania project. Please check out our [wiki](https://2021.igem.org/Team:Vilnius-Lithuania) for more information.

# Requirments:
The program was written to run and tested on a linux machine (Manjaro).

The machine should have a GPU installed, otherwise the program will run increadibly slowly, the program was tested on a machine with the followig specs:

GPU - NVIDIA® GeForce® GTX 1650; 4GB

CPU - AMD Ryzen 5 4600H

RAM - 8GB

# Instalation:
The program uses OpenMM to compute potential energies of the complex and AmberTools to prepare .pdb files for molecular dynamics calculations.

Both of these programs need to be installed, this can be done using Anaconda. We recommend using [miniconda](https://docs.conda.io/en/latest/miniconda.html) as it is less bloat.

OpenMM can be installed by learning how to do that at the offical [OpenMM](https://openmm.org/) website or running:

`conda install -c conda-forge openmm`

Same for [AmberTools](https://ambermd.org/AmberTools.php):

`conda install -c conda-forge ambertools=21 compilers`.

Additionally the program uses the following python packages:

1. Numpy,
2. Scipy,
3. Pexpect - due to this dependency the program will not work on Windows, if you want it to run on Windows you need to edit the functions in functions/generateAmberFiles.py to use the Pexpect api for Windows.

# Usage:
The program uses a .fasta file as input to specify which sequences to score (example input file provided in the repository).

In general to run the program run:

`python EFBAScore.py input.fasta target.pdb output.fasta`.

Call: 

`python EFBAScore.py -h`

for the help screen to see all optional parameters.

You can benchmark the program on your system by running it with the sample .pdb file provided by running: 

`python EFBAScore.py genes.fasta example.pdb output.fasta`

On our system this command took 2018 s. (~30 min.) to run.

# Troubleshooting:
The program will not work on Windows! If you want it to run on Windows you need to edit the functions in functions/generateAmberFiles.py to use the Pexpect api for Windows.

Getting .pdb files to work with the AMBER forcefield usually requires some tinkering.

You should check that you are able to run the following commands on your .pdb file in leap in order to make sure that your .pdb file is fine:

1. If you have installed AmberTools through conda you should be able to open the Leap program by running tleap in your terminal
2. Run `source leaprc.protein.ff14SB`
3. Run `source leaprc.DNA.OL15`
4. Run `source leaprc.gaff`
5. Run `set default PBradii mbondi2`
6. Run `target = loadpdb your_target_pdb_file.pdb`
7. Run `saveamberparm target target.prmtop target.inpcrd`

If leap generates two files target.prmtop target.inpcrd you should be ready run our program without problems.

If leap throws errors we followed the following [guide](https://ambermd.org/tutorials/pengfei/index.htm) to get our .pdb files to work with leap.

