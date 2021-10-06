from simtk.openmm.app import AmberPrmtopFile, AmberInpcrdFile, Simulation, HBonds, PDBFile
from simtk.openmm.openmm import LangevinMiddleIntegrator
from simtk.unit import nanometer, kelvin, picosecond, picoseconds, kilojoule_per_mole, angstrom
import numpy as np
import time
from argparse import ArgumentParser, BooleanOptionalAction
from functions import generate_target, generate_sequence, compute_spatial_sampling_positions, get_dna_from_topology, move_dna, rotate_dna, compute_initial_entropy, compute_entropy

#Process input arguments
parser = ArgumentParser(description='Computes an aptamer that should bind to the target using the EFBA approach')
parser.add_argument('target', help='The .pdb file of the target molecule')
parser.add_argument('-l', '--length', type=int, dest="length", default=15, help='The desired length of the aptamer in bases, default is 15')
parser.add_argument('-o', '--output', dest="output", default="", help="The .pdb file to output the final complex to, leave blank if you do not want this .pdb file")
parser.add_argument('-f', '--forcefield', dest="forcefield", default="", help="Optional forcefield modification file (.frcmod)")
parser.add_argument('-t', '--threshold', dest="threshold", type=float, default = 0, help="Entropy gain threshold for each step (default 0)")
parser.add_argument('-mp', '--min_probability', dest="minimum_probability", type=float, default=0, help="Minimum probability that a position must have in order to be sampled (default 0)")
parser.add_argument('-b', '--beta', dest="beta", type=float, default=1e-5, help="Beta parameter (default 1e-5)")
parser.add_argument('-bs', '--box_size', dest="box_size", type=float, default=5, help="Box size (in Angstroms) to use when generating spatial sampling positions (default 5)")
parser.add_argument('-rna', '--rna', dest="rna", type=bool, default=False, action=BooleanOptionalAction, help="Generate RNA aptamer (default false)")
args = parser.parse_args()

tleap_dir = "./tleap/"
target = args.target
length = args.length
output = args.output
isRNA = args.rna
frcmod_file = args.forcefield
start_time = time.time()
beta = args.beta
threshold = args.threshold
min_probability = args.minimum_probability

starting_nucleotides = ['DA5', 'DT5', 'DC5', 'DG5']
nucleotides = ['DA', 'DT', 'DC', 'DG']

if isRNA:
  starting_nucleotides = ['A5', 'U5', 'C5', 'G5']
  nucleotides = ['A', 'U', 'C', 'G']

generate_target(tleap_dir, target, frcmod_file)

#Compute the spatial sampling positions
prmtop = AmberPrmtopFile(f'{tleap_dir}/target.prmtop')
inpcrd = AmberInpcrdFile(f'{tleap_dir}/target.inpcrd')
system = prmtop.createSystem(nonbondedCutoff=10*angstrom,
            constraints=HBonds)
integrator = LangevinMiddleIntegrator(300*kelvin, 1/picosecond, 0.004*picoseconds)
simulation = Simulation(prmtop.topology, system, integrator)
simulation.context.setPositions(inpcrd.positions)
if inpcrd.boxVectors is not None:
    simulation.context.setPeriodicBoxVectors(*inpcrd.boxVectors)
simulation.minimizeEnergy()
state = simulation.context.getState(getPositions = True)
minimized_pos = state.getPositions(asNumpy=True).value_in_unit(angstrom)
sampling_positions = compute_spatial_sampling_positions(minimized_pos, args.box_size)
print(f"Number of spatial sampling positions {len(sampling_positions)}")
print(f"Done computing the spatial sampling positions, time elapsed so far: {np.floor(time.time() - start_time)} s.")

total_entropy = 0

results = compute_initial_entropy(tleap_dir, target, minimized_pos, sampling_positions, beta, frcmod_file, starting_nucleotides)


max_entropy_key = max(results, key=lambda nucleotide: results[nucleotide]["entropy"])
result = results[max_entropy_key]
probability_indexes = np.argsort(result["probabilities"])[ : :-1]
max_entropy_value = results[max_entropy_key]["entropy"]
total_entropy = total_entropy + max_entropy_value
print(f"Done computing step 1, aptamer so far: {max_entropy_key.replace('D', '').replace('3', '').replace('5', '')}, relative entropy added in this step: {max_entropy_value}, total relative entropy so far: {total_entropy}, time elapsed so far: {np.floor(time.time() - start_time)} s.")

def recursion_level(tleap_dir, target, aptamer, rotations, spatial_pos, beta, total_entropy, max_length):
  results = compute_entropy(tleap_dir, target, minimized_pos, aptamer, rotations, spatial_pos, beta, frcmod_file, nucleotides)

  max_entropy_key = max(results, key=lambda nucleotide: results[nucleotide]["entropy"])
  result = results[max_entropy_key]
  probability_indexes = np.argsort(result["probabilities"])[ : :-1]
  print(f"Computed {''.join([*aptamer, max_entropy_key]).replace('D', '').replace('3', '').replace('5', '')}, relative entropy gained in this step: {result['entropy']}, total entropy w this aptamer {total_entropy + result['entropy']}, time elapsed so far: {np.floor(time.time() - start_time)} s.")
  if result["entropy"] < threshold or (len(aptamer) + 1) == max_length:
    if result["entropy"] < threshold:
      print(f"Failed to meet entropy gain target with {''.join([*aptamer, max_entropy_key]).replace('D', '').replace('3', '').replace('5', '')}, retracing.")
    return [*aptamer, max_entropy_key], [*rotations, result["angles"][probability_indexes[0]]], spatial_pos, total_entropy + result["entropy"]
  for idx in probability_indexes:
    if result["probabilities"][idx] < min_probability:
      print(f"Failed to find aptamer with {''.join(aptamer).replace('D', '').replace('3', '').replace('5', '')}, retracing.")
      return [*aptamer, max_entropy_key], [*rotations, result["angles"][probability_indexes[0]]], spatial_pos, total_entropy + result["entropy"]
    new_aptamer, new_rotations, new_spatial_pos, new_entropy = recursion_level(tleap_dir, target, [*aptamer, max_entropy_key], [*rotations, result["angles"][idx]], spatial_pos, beta, total_entropy + result["entropy"], max_length)
    if len(new_aptamer) == max_length:
      return new_aptamer, new_rotations, new_spatial_pos, new_entropy

for idx in probability_indexes:
  if result["probabilities"][idx] > 0:
    aptamer, rotations, spatial_pos, total_entropy = recursion_level(tleap_dir, target, [max_entropy_key], [result["angles"][idx]], [result["positions"][idx]], beta, max_entropy_value, length)
    if len(aptamer) == length:
      break


print(f"Done computing, final aptamer: {''.join(aptamer).replace('D', '').replace('3', '').replace('5', '')}, total relative entropy: {total_entropy}, time elapsed: {np.floor(time.time() - start_time)} s.")

if len(output) > 0:
  generate_sequence(tleap_dir, target, aptamer, frcmod_file)

  prmtop = AmberPrmtopFile(f'{tleap_dir}/{aptamer[-1]}.prmtop')
  inpcrd = AmberInpcrdFile(f'{tleap_dir}/{aptamer[-1]}.inpcrd')
  pos = inpcrd.getPositions(asNumpy=True).value_in_unit(angstrom)
  for k in range(len(minimized_pos)):
    pos[k] = minimized_pos[k]
  dna = get_dna_from_topology(prmtop.topology)
  pos = rotate_dna(dna, pos, rotations)
  pos = move_dna(dna[0][0].index, dna[0][-1].index, spatial_pos, pos)

  with open(output, 'w') as file:
    PDBFile.writeFile(prmtop.topology, pos, file)