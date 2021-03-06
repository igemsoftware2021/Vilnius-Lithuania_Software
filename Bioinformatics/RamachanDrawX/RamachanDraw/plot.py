import os
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
from Bio.PDB import PDBParser, PPBuilder
from pkg_resources import resource_stream
from math import pi
from matplotlib import font_manager

def plot(pdb_file, cmap='viridis', alpha=0.75, dpi=100, el_color='white', font='-', transparency=1, save=True, show=False, out='plot.png'):
    batch_mode = [True if type(pdb_file) is list else False][0]
    
#   Setting default font
    if(font == '-'):
        font = './Fonts/Quicksand/'
        
#   Customizing text font
    font_dirs = [font]
    font_files = font_manager.findSystemFonts(fontpaths=font_dirs)
    without_extra_slash = os.path.normpath(font)
    last_part = os.path.basename(without_extra_slash)
        
    for font_file in font_files:
        font_manager.fontManager.addfont(font_file)
        plt.rcParams['font.family'] = last_part
    
#   Customizing font colour (white by default):
    plt.rcParams['text.color'] = el_color
    plt.rcParams['axes.labelcolor'] = el_color
    plt.rcParams['xtick.color'] = el_color
    plt.rcParams['ytick.color'] = el_color

    def get_ignored_res(file: str):
        x, y, ignored, output = [], [], [], {}
        for model in PDBParser().get_structure(id=None, file=file):
            for chain in model:
                peptides = PPBuilder().build_peptides(chain)
                for peptide in peptides:
                    for aa, angles in zip(peptide, peptide.get_phi_psi_list()):
                        residue = aa.resname + str(aa.id[1])
                        output[residue] = angles

        for key, value in output.items():
            # Only get residues with both phi and psi angles
            if value[0] and value[1]:
                x.append(value[0] * 180 / pi)
                y.append(value[1] * 180 / pi)
            else:
                ignored.append((key, value))

        return output, ignored, x, y

    size = [(8.5, 5) if batch_mode else (5.5, 5)][0]
    plt.figure(figsize=size, dpi=dpi)
    ax = plt.subplot(111)
    
#   Change title of the plot to the name of PDB file
    without_extra_slash = os.path.normpath(pdb_file)
    last_part = os.path.basename(without_extra_slash)
    ax.set_title("".join(["Batch" if batch_mode else last_part]))

    # Import 'density_estimate.dat' data file
    Z = np.fromfile(resource_stream('RamachanDraw', 'data/density_estimate.dat'))
    Z = np.reshape(Z, (100, 100))

    ax.set_aspect('equal')
    ax.set_xlim(-180, 180)
    ax.set_ylim(-180, 180)
    ax.set_xticks([-180, -135, -90, -45, 0, 45, 90, 135, 180], minor=False)
    ax.set_yticks([-180, -135, -90, -45, 0, 45, 90, 135, 180], minor=False)
    
    # Color of the axles configurable as elements (el_color) from command line
    plt.axhline(y=0, color=el_color, lw=0.5)
    plt.axvline(x=0, color=el_color, lw=0.5)
    plt.grid(b=None, which='major', axis='both', color=el_color, alpha=0.2)
    
    # Font chosen to visualise phi and psi letter symbols
    axis_font = {'fontname':'Arial', 'size':'12'}
    # Phi letter symbol
    plt.xlabel('\u03C6', **axis_font)
    # Psi letter symbol
    plt.ylabel('\u03C8', **axis_font)

    # Normalize data
    data = np.log(np.rot90(Z))
    ax.imshow(data, cmap=plt.get_cmap(cmap), extent=[-180, 180, -180, 180], alpha=alpha)

    # Fit contour lines correctly
    data = np.rot90(np.fliplr(Z))
    ax.contour(data, colors=el_color, linewidths=0.5,
               levels=[10 ** i for i in range(-7, 0)],
               antialiased=True, extent=[-180, 180, -180, 180], alpha=0.65)
               
    # Color of the dots configurable as elements (el_color) from command line
    def start(fp, color=el_color):
        assert os.path.exists(fp), \
            'Unable to fetch file: {}. PDB entry probably does not exist.'.format(pdb_file)
        phi_psi_data, ignored_res, x, y = get_ignored_res(file=fp)
        ax.scatter(x, y, marker='.', s=3, c="".join([color if color else 'k']), label=fp)

    if batch_mode:
        for _, file in enumerate(pdb_file):
            start(fp=file, color=list(mcolors.BASE_COLORS.keys())[_])
        ax.legend(bbox_to_anchor=(1.04, 1), loc='upper left')
    else:
        start(fp=pdb_file)
    
    transparent_var = False
    
    if(transparency != 0):
        transparent_var = True

    if save:
        plt.savefig(out, transparent=transparent_var)
    if show:
        plt.show()
