from RamachanDraw import fetch, phi_psi, palette, plot
from matplotlib import cm
from matplotlib.colors import ListedColormap
import numpy as np
import sys
from argparse import ArgumentParser

# Process input arguments
parser = ArgumentParser(description='RamachanDrawX is a program that uses RamachanDraw library to plot  customizable Ramachandran plots.')
parser.add_argument('file', help='The .pdb file of the protein')
parser.add_argument('-cmap', '--color_map', type=str, dest="cmap", default='#002733 #054d54 #1b8489 #ef9f8d #fccec0', help='Provide the color palette to create the colormap or use the existing colormap.')
parser.add_argument('-el_color', '--element_color', type=str, dest="el_color", default='#002733', help='The color of dots, elements of axles and labels (string, default: \'#002733)\'')
parser.add_argument('-font', '--font', type=str, dest="font", default='-', help='Full path to the font directory of your choice (default: Quicksand)')
parser.add_argument('-tr', '--transparency', type=int, dest="transparency", default=1, help='Option whether to set transparent background or not (any int value except 0 stands for True, default: 1)')
parser.add_argument('-a', '--alpha', type=float, dest="alpha", default=1, help='The opacity of the colormap (float value [0; 1], default: 1)')
parser.add_argument('-dpi', '--dpi', type=int, dest="dpi", default=1000, help='Resolution (int dots per inch, default: 1000)')
parser.add_argument('-out', '--output', dest="output", default="./PNG/R_plot.png", help='The name of the output plot file (default: ./PNG/R_plot.png)')
args = parser.parse_args()

# Palette processing
palette_ = args.cmap
our_palette = palette_.split()
if(len(our_palette) > 1):
    palette_colormap = palette.get_continuous_cmap(our_palette)
    args.cmap = palette_colormap

# Plotting the graph
plot(args.file, args.cmap, args.alpha, args.dpi, args.el_color, font=args.font, transparency=args.transparency, save=True, show=False, out=args.output)
