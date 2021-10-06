def move_dna(start_index, O_index, to, positions):
  '''
  Moves DNA to the position, such that the atom with index specified in O_index would be at pos specified in to
  start_index denotes the starting index of DNA atoms in list of positions
  '''
  O_pos = positions[O_index].copy()
  for i in range((len(positions)-start_index)):
    positions[i+start_index] = positions[i+start_index]-O_pos+to
  return positions