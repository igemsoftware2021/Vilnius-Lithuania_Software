import numpy as np

def compute_spatial_sampling_positions(vectors, box_size):
  '''
  Computes spatial sampling positions on the surface of the target
  box_size denotes the average distance between two neighbouring sampling points
  '''
  box_positions = np.unique(np.array([np.round(v/box_size) for v in vectors]), axis=0)
  positions = []
  for x in [-1, 1]:
    for y in [-1, 1]:
      for z in [-1, 1]:
        positions.extend([[v[0]+x, v[1]+y, v[2]+z] for v in box_positions])
  positions = np.unique(np.array(positions), axis=0)
  box_positions = set([tuple(x) for x in box_positions])
  positions = set([tuple(x) for x in positions])
  positions = np.array([x for x in positions if x not in box_positions])
  positions = np.array([box_size*x for x in positions])
  return positions