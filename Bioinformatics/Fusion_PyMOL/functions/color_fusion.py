#!/usr/bin/env python
import pymol
from pymol import cmd
from pathlib import Path

# Subroutine that colors fusion system
def color_fusion(par):
    # Loading and coloring structure
    cmd.load(par.fusion_file, par.obj_name)
    cmd.color(par.colors[2], par.obj_name)

    # Selecting residues of the active site
    for i in range(len(par.active_site_residues_1)):
        cmd.select('resi '+par.active_site_residues_1[i])
        active_site_name = 'as_1_'+str(i+1)
        cmd.set_name('sele', active_site_name)
        cmd.color(par.colors[4], active_site_name)

    # Color the residues of the linker
    first_linker_res = int(par.first_length)+1
    last_linker_res = int(par.first_length)+par.linker_length
    cmd.select('resi '+str(first_linker_res)+'-'+str(last_linker_res))
    cmd.set_name('sele', 'linker')
    cmd.color(par.colors[5], 'linker')

    # Modifying the number of residues (accordingly to the length of first
    # protein and the linker)
    mod_active_site_residues_2 = []
    for j in range(len(par.active_site_residues_2)):
        sep_residues = par.active_site_residues_2[0].split('+')
        mod_res = ''
        for i in range(len(sep_residues)):
            sep_res_num = int(sep_residues[i])
            sep_res_num += int(par.first_length)
            sep_res_num += par.linker_length
            mod_res += str(sep_res_num)
            if(i != len(sep_residues)-1):
                mod_res += '+'
        mod_active_site_residues_2.append(mod_res)

    # Color the residues of the second protein active site
    for i in range(len(mod_active_site_residues_2)):
        cmd.select('resi '+mod_active_site_residues_2[i])
        active_site_name = 'as_2_'+str(i+1)
        cmd.set_name('sele', active_site_name)
        cmd.color(par.colors[4], active_site_name)
        
# Subroutine that loads template files
def load_templates(par):
    cmd.load(par.first_protein)
    first_prot_name = Path(par.first_protein).stem
    cmd.color(par.colors[3], first_prot_name)
    cmd.load(par.second_protein)
    second_prot_name = Path(par.second_protein).stem
    cmd.color(par.colors[0], second_prot_name)
    
    cmd.cealign(par.obj_name, first_prot_name)
    cmd.cealign(par.obj_name, second_prot_name)
    cmd.center(par.obj_name)
