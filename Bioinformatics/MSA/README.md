# GenFusMSA

GenFusMSA is a script that generates multiple sequence alignment (MSA) file that can be used 
for fusion protein joined via linkers of choice modelling. This program supports [small tool for 
bioinformatics manifesto](https://github.com/pjotrp/bioinformatics).

## Requirements

Download and install [Perl](https://www.perl.org/get.html).

## Usage

Inputs for this program are:  
1. `-i1 .a3m_file` full query-template .a3m file of the first protein  
2. `-i2 .a3m_file` full query-template .a3m file of the second protein  
3. `-l str` peptide linker sequence
4. `[-n int]` repeats of the linker
5. `[-p int]` option to extend the linker with 10 glycine aminoacids on both sides of the linker

These .a3m files can be generated using external software. The program was tested with MSA
files that were generated using [HHblits](https://toolkit.tuebingen.mpg.de/tools/hhblits) program. 

`perl GenFusMSA.pl -i1 4CL_fullQT.a3m -i2 CHS_fullQT.a3m -l EAAAK -n 1`  

This command generates MSA file for 4CL and CHS linked via prolonged EAAAK linker. The 
option to choose prolonged linker by glycines (by 10 on both sides of the linker) is set by the 
last option (0 or 1).

## License
[MIT](https://choosealicense.com/licenses/mit/)


