import numpy as np

def get_dna_from_topology(topology):
  '''
  Extracts the DNA atoms from the topology and puts them in separate lists based on residues
  output is list of lists
  '''
  dna = np.array([x for x in topology.atoms() if x.residue.name in ['DA', 'DG', 'DC', 'DT']])
  dna_residues = np.sort(np.unique([x.residue.index for x in dna]))
  dna = [[y for y in dna if y.residue.index == x] for x in dna_residues]

  return dna