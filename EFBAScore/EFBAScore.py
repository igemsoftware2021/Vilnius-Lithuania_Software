from simtk.openmm.app import AmberPrmtopFile, AmberInpcrdFile, PDBFile
from simtk.unit import angstrom
import numpy as np
import time
from argparse import ArgumentParser
from functions import read_fasta, write_fasta, generate_target, generate_sequence, compute_spatial_sampling_positions, get_dna_from_topology, move_dna, rotate_dna, compute_initial_entropy, compute_entropy

#Process input arguments
parser = ArgumentParser(description='Computes an aptamer that should bind to the target using the EFBA approach')
parser.add_argument('input', help='A FASTA file containing sequences to score')
parser.add_argument('target', help='The .pdb file of the target molecule')
parser.add_argument('output', help="The file to output the results to (FASTA format)")
parser.add_argument('-f', '--forcefield', dest="forcefield", default="", help="Optional forcefield modification file (.frcmod)")
parser.add_argument('-b', '--beta', dest="beta", type=float, default=1e-5, help="Beta parameter (default 1e-5)")
parser.add_argument('-bs', '--box_size', dest="box_size", type=float, default=5, help="Box size (in Angstroms) to use when generating spatial sampling positions (default 5)")
args = parser.parse_args()


tleap_dir = "./tleap/"
target = args.target
input = args.input
output = args.output
frcmod_file = args.forcefield
start_time = time.time()
beta = args.beta

sequences_with_headers = read_fasta(input)
sequences = np.unique([seq["sequence"] for seq in sequences_with_headers])

#Prepare sequences for calculation
split_sequences = []
initial_nucleotides = []
for sequence in sequences:
  initial_nucleotides.append(sequence[0])
  for idx in range(2, len(sequence)+1):
    split_sequences.append(sequence[:idx])
split_sequences = np.array(sorted(np.unique(split_sequences), key=len))
initial_nucleotides = np.unique(initial_nucleotides)

generate_target(tleap_dir, target, frcmod_file)

#Compute the spatial sampling positions
prmtop = AmberPrmtopFile(f'{tleap_dir}/target.prmtop')
inpcrd = AmberInpcrdFile(f'{tleap_dir}/target.inpcrd')
pos = inpcrd.getPositions(asNumpy=True).value_in_unit(angstrom)
sampling_positions = compute_spatial_sampling_positions(pos, args.box_size)
print(f"Number of spatial sampling positions {len(sampling_positions)}")
print(f"Done computing the spatial sampling positions, time elapsed so far: {np.floor(time.time() - start_time)} s.")

results = {}

for nucleotide in initial_nucleotides:
  result = compute_initial_entropy(tleap_dir, target, sampling_positions, "D"+nucleotide+"5", beta, frcmod_file)

  max_probability_idx = np.argmax(result["probabilities"])
  results[nucleotide] = {
    "position": result["positions"][max_probability_idx],
    "rotation": [result["angles"][max_probability_idx]],
    "entropy": result["entropy"]
  }
  print(f"Done with {nucleotide}, total entropy with this sequence {result['entropy']}, total time spent so far {np.floor(time.time() - start_time)} s.")

for idx, sequence in enumerate(split_sequences):
  prev_sequence_result = results[sequence[:-1]]
  aptamer = ["D" + letter for letter in sequence]
  aptamer[0] = aptamer[0] + "5"
  result = compute_entropy(tleap_dir, target, aptamer[:-1], prev_sequence_result["rotation"], prev_sequence_result["position"], aptamer[-1], beta, frcmod_file)

  max_probability_idx = np.argmax(result["probabilities"])
  results[sequence] = {
    "position": prev_sequence_result["position"],
    "rotation": [*prev_sequence_result["rotation"], result["angles"][max_probability_idx]],
    "entropy": prev_sequence_result["entropy"] + result["entropy"]
  }
  print(f"Done with {sequence}, total entropy with this sequence {prev_sequence_result['entropy'] + result['entropy']}, entropy gained in this step {result['entropy']}, done with {idx+1} / {len(split_sequences)}, total time spent so far {np.floor(time.time() - start_time)} s.")

for key in results:
  if key in sequences:
    for seq in sequences_with_headers:
      if seq["sequence"] == key:
        seq["header"] = seq["header"] + f"; Score (relative entropy): {results[key]['entropy']}"

write_fasta(output, sequences_with_headers)
print("Done!")