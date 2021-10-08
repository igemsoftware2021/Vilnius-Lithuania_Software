# RamachanDrawX

This is a program that draws a Ramachandran plot based on the input PDB file. It makes use of 
[RamachanDraw](https://github.com/alxdrcirilo/RamachanDraw) library. RamachanDrawX 
allows plot customization.

This program was tested using conda environment with Python 3.7 version installed.

## Requirements

Since this RamachanDrawX was tested using conda environment, it is recommended to create 
one to use this program. 
Since [miniconda](https://docs.conda.io/en/latest/miniconda.html) is less bloat, it is suggested
to install this version of Python package manager.

* Create a conda environment  
`conda create -n ramachandrawx python=3.7`

* Activate conda environment  
`conda activate ramachandrawx`

* Install dependencies  
`conda install biopython`  
`conda install matplotlib`  
`conda install rich`  

## Example usage

RamachanDrawX can be run using command:  
`python RamachanDrawX.py PDB/4CL.pdb`

This command will generate an output file R_plot.png in `./PNG` folder for PDB structure 
of 4CL protein.

## Customization arguments

Manual for the customization arguments can also be found using  
`python RamachanDrawX.py -h`

### Colormap

By default the program uses color palette of [Vilnius-Lithuania iGEM 2021 team](https://2021.igem.org/Team:Vilnius-Lithuania).

Custom colormap can be set using  
`-cmap` or `--color_map`  
This option allows to create a new colormap or use from existing [Matplotlib colormaps](https://matplotlib.org/stable/tutorials/colors/colormaps.html).  

In order to create a new colormap from the palette that contains N colors of the user's choice, it is required to provide colors in format:  
`-cmap '#[hex_color_code_1] #[hex_color_code_2] ... #[hex_color_code_N]'`

### Element color

By default the program uses #002733 (color similar to [Daintree](https://chir.ag/projects/name-that-color/#002733)) to color dots, numbers and labels on axles.  

Custom element color can be set using  
`-el_color '#[hex_color_code]'`  
or  
`-el_color [color_name]`  

### Font

By default the program uses Quicksand font that was downloaded from [Google Fonts](https://fonts.google.com) and placed in `Fonts` folder found in the working directory.  

Customization of the title's and axles numbers' font can be done using  
`-font [full_path_to_font_dir]`

### Background transparency

By default the program produces PNG file with a transparent background. Another option 
is a white background that can be set using  
`-tr 0`  

The PNG file with white background will be generated.  

### Opacity of the colormap

By default the opacity of the colormap is set to 1 (the brightest option).  

The opacity of the colormap can be altered using  
`-a [float_from_[0;1]]`

### Resolution of the plot

By default the program produces PNG file with aresolution of 1000 dots per inch.  

The resolution can be changed using  
`-dpi [integer]`

### Output location

By default the program generates a PNG file `./PNG/R_plot.png`.  

The change of the output file's location can be done using  
`-out [path_with_a_custom_name.png]`  

## License
[MIT](https://choosealicense.com/licenses/mit/)

## References

This tool is intended to support [The Small Tools Manifesto for Bioinformatics](https://github.com/pjotrp/bioinformatics).
