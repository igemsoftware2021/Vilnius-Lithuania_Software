from simtk.openmm.app import AmberPrmtopFile, AmberInpcrdFile, Simulation, HBonds, PDBFile
from simtk.openmm.openmm import LangevinMiddleIntegrator
from simtk.unit import nanometer, kelvin, picosecond, picoseconds, kilojoule_per_mole, angstrom
import numpy as np
from scipy.stats import entropy
from functions import generate_sequence, get_dna_from_topology, move_dna, rotate_dna, anti_rotate_dna, rotate_nucleotide, anti_rotate_nucleotide

def compute_initial_entropy(tleap_dir, target, minimized_positions, sampling_positions, beta, frcmod_file, possible_nucleotides):
  results = {}

  for nuc in possible_nucleotides:
    results[nuc] = {
      "energies": [],
      "positions": [],
      "angles": [],
      "exp_energies": [],
      "probabilities": [],
      "entropy": -1
    }

  for nucleotide in possible_nucleotides:
    generate_sequence(tleap_dir, target, [nucleotide], frcmod_file)

    prmtop = AmberPrmtopFile(f'{tleap_dir}/{nucleotide}.prmtop')
    inpcrd = AmberInpcrdFile(f'{tleap_dir}/{nucleotide}.inpcrd')

    pos = inpcrd.getPositions(asNumpy=True).value_in_unit(angstrom)
    for k in range(len(minimized_positions)):
      pos[k] = minimized_positions[k]
    dna = get_dna_from_topology(prmtop.topology)
    O_index = dna[0][-1].index
    start_index = dna[0][0].index

    system = prmtop.createSystem(nonbondedCutoff=10*angstrom)
    integrator = LangevinMiddleIntegrator(300*kelvin, 1/picosecond, 0.004*picoseconds)
    simulation = Simulation(prmtop.topology, system, integrator)
    if inpcrd.boxVectors is not None:
      simulation.context.setPeriodicBoxVectors(*inpcrd.boxVectors)

    energies = []
    positions = []
    angles = []
    exp_energies = []
    rotation_angles = [0, np.pi]
    for aptamer_position in sampling_positions:
      pos = move_dna(start_index, O_index, aptamer_position, pos)
      for x_angle in rotation_angles:
        for y_angle in rotation_angles:
          for z_angle in rotation_angles:
            pos = rotate_dna(dna, pos, [(x_angle, y_angle, z_angle)])
            simulation.context.setPositions(pos * angstrom)
            state = simulation.context.getState(getEnergy = True)
            energy = state.getPotentialEnergy().value_in_unit(kilojoule_per_mole)
            pos = anti_rotate_dna(dna, pos, [(x_angle, y_angle, z_angle)])
            energies.append(energy)
            positions.append(aptamer_position)
            angles.append((x_angle, y_angle, z_angle))
            exp_energies.append(np.exp(-beta*energy))
    results[nucleotide] = {
      "energies": energies,
      "positions": positions,
      "angles": angles,
      "exp_energies": exp_energies,
      "probabilities": [],
      "entropy": -1
    }

  for key, value in results.items():
    Z = np.sum(value["exp_energies"])
    if Z != 0:
      results[key]["probabilities"] = np.array(value["exp_energies"]/Z)
    else:
      results[key]["probabilities"] = np.array([1]*len(value["exp_energies"]))
  
  uniform = 0.25*(np.sum([results[nuc]["probabilities"] for nuc in possible_nucleotides], axis=0))
  for key, value in results.items():
    results[key]["entropy"] = entropy(results[key]["probabilities"], uniform)

  return results

def compute_entropy(tleap_dir, target, minimized_positions, aptamer, rotations, spatial_position, beta, frcmod_file, possible_nucleotides):
  results = {}

  for nuc in possible_nucleotides:
    results[nuc] = {
      "energies": [],
      "angles": [],
      "exp_energies": [],
      "probabilities": [],
      "entropy": -1
    }

  for nucleotide in possible_nucleotides:
    generate_sequence(tleap_dir, target, [*aptamer, nucleotide], frcmod_file)

    prmtop = AmberPrmtopFile(f'{tleap_dir}/{nucleotide}.prmtop')
    inpcrd = AmberInpcrdFile(f'{tleap_dir}/{nucleotide}.inpcrd')

    pos = inpcrd.getPositions(asNumpy=True).value_in_unit(angstrom)
    for k in range(len(minimized_positions)):
      pos[k] = minimized_positions[k]
    dna = get_dna_from_topology(prmtop.topology)
    O_index = dna[0][-1].index
    start_index = dna[0][0].index

    system = prmtop.createSystem(nonbondedCutoff=10*angstrom,
            constraints=HBonds)
    integrator = LangevinMiddleIntegrator(300*kelvin, 1/picosecond, 0.004*picoseconds)
    simulation = Simulation(prmtop.topology, system, integrator)
    if inpcrd.boxVectors is not None:
      simulation.context.setPeriodicBoxVectors(*inpcrd.boxVectors)

    pos = move_dna(start_index, O_index, spatial_position, pos)
    pos = rotate_dna(dna, pos, rotations)

    energies = []
    angles = []
    exp_energies = []
    rotation_angles = [-np.pi/2, -np.pi/3, -np.pi/6, 0, np.pi/6, np.pi/3, np.pi/2]
    for x_angle in rotation_angles:
      for y_angle in rotation_angles:
        for z_angle in rotation_angles:
          pos = rotate_nucleotide(dna[-1], pos, (x_angle, y_angle, z_angle))
          simulation.context.setPositions(pos * angstrom)
          state = simulation.context.getState(getEnergy = True)
          energy = state.getPotentialEnergy().value_in_unit(kilojoule_per_mole)
          pos = anti_rotate_nucleotide(dna[-1], pos, (x_angle, y_angle, z_angle))
          energies.append(energy)
          angles.append((x_angle, y_angle, z_angle))
          exp_energies.append(np.exp(-beta*energy))
    results[nucleotide] = {
      "energies": energies,
      "angles": angles,
      "exp_energies": exp_energies,
      "probabilities": [],
      "entropy": -1
    }

  for key, value in results.items():
    Z = np.sum(value["exp_energies"])
    if Z != 0:
      results[key]["probabilities"] = np.array(value["exp_energies"]/Z)
    else:
      results[key]["probabilities"] = np.array([1]*len(value["exp_energies"]))
  
  uniform = 0.25*(np.sum([results[nuc]["probabilities"] for nuc in possible_nucleotides], axis=0))
  for key, value in results.items():
    results[key]["entropy"] = entropy(results[key]["probabilities"], uniform)

  return results

