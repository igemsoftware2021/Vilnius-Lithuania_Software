#!/usr/bin/env python
import pymol
from pymol import cmd
from functions import center_of_mass
from pymol import stored
from statistics import mean

# Subroutine that counts how many digits the number has
def countDigit(n):
    count = 0
    while n != 0:
        n //= 10
        count += 1
    return count

# Subroutine that calculates distance between active sites when rigid linker
# is used in the fusion protein system
def calculate_distance(par, dist):
    COM_1 = 'COM_1_1'
    COM_2 = 'COM_2_1'

    # Calculating center of mass for each active site
    center_of_mass.com('as_1_1', None, None, COM_1, 0)
    center_of_mass.com('as_2_1', None, None, COM_2, 0)
    
    # Creating a distance object for visualisation in PyMOL
    d = cmd.distance('distance_COM', COM_1, COM_2)
    #dist[0] = d
    
    # Write distance
    cmd.set('label_color', par.colors[0], 'distance_COM')
    cmd.color(par.colors[4], 'distance_COM')
    
    cmd.center(par.obj_name)
    cmd.zoom(par.obj_name)
    
def calculate_distance_multiple_states(par, dist):
    COM_1 = 'COM_1_1'
    COM_2 = 'COM_2_1'

    # Calculating center of mass for each active site
    center_of_mass.com('as_1_1', None, None, COM_1, 0)
    center_of_mass.com('as_2_1', None, None, COM_2, 0)
    
    # Creating a distance object for visualisation in PyMOL
    d = cmd.distance('distance_COM', COM_1, COM_2)
    
    # Creating a pseudo atom for distance calculation between atoms
    cmd.create('ov_COM_1', COM_1, 0, 1)
    cmd.create('ov_COM_2', COM_2, 0, 1)
    cmd.delete(COM_1)
    cmd.delete(COM_2)
    
    # Calculating distance between pseudo atoms in each state
    for i in range(1, len(dist)+1):
        if len(str(i)) > 2:
            num = str(i)[-2:]
            dist[i-1] = cmd.get_distance(atom1="/ov_COM_1/PSDO/P/PSD`1/"+str(i)[0:len(str(i))-2]+"PS"+num, atom2="/ov_COM_2/PSDO/P/PSD`1/"+str(i)[0:len(str(i))-2]+"PS"+num, state=i)
        else:
            dist[i-1] = cmd.get_distance(atom1="/ov_COM_1/PSDO/P/PSD`1/PS"+str(i), atom2="/ov_COM_2/PSDO/P/PSD`1/PS"+str(i), state=i)
    
    # Visualize distances 
    cmd.set('label_color', par.colors[0], 'distance_COM')
    cmd.color(par.colors[4], 'distance_COM')
    
    cmd.show('spheres', 'all')
    cmd.center(par.obj_name)
    cmd.zoom(par.obj_name)

def write_to_file(par, dist, file):
    if file is None:
        file = "./tmp/distances.txt"
    
    outFile = open(file, 'w')
    
    outFile.write("%s\n" % par.fusion_file)
    if(dist):
        outFile.write("Minimum distance: %s\n" % (min(dist)))
        outFile.write("Maximum distance: %s\n" % (max(dist)))
        outFile.write("Average distance: %s\n" % (mean(dist)))
    
    outFile.close()
        
    
