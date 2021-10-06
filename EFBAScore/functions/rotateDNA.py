import numpy as np

R_x = lambda phi: np.array([[1, 0, 0], [0, np.cos(phi), -np.sin(phi)], [0, np.sin(phi), np.cos(phi)]])
R_y = lambda phi: np.array([[np.cos(phi), 0, np.sin(phi)], [0, 1, 0], [-np.sin(phi), 0, np.cos(phi)]])
R_z = lambda phi: np.array([[np.cos(phi), -np.sin(phi), 0], [np.sin(phi), np.cos(phi), 0], [0, 0, 1]])

def rotate_dna(dna, pos, angles):
  '''
  Rotates the DNA based on angles
  '''

  start_index = dna[0][0].index
  end_index = dna[-1][-1].index

  for idx, angle in enumerate(angles):
    if idx == 0:
      #Rotate with respect to oxygen
      O_index = dna[idx][-1].index
      O_pos = pos[O_index].copy()
      pos = pos - O_pos
      for i in range(O_index-start_index):
        v = pos[i+start_index]
        v = np.matmul(v, R_x(angle[0]).T)
        v = np.matmul(v, R_y(angle[1]).T)
        v = np.matmul(v, R_z(angle[2]).T)
        pos[i+start_index] = v
      pos = pos + O_pos

    else:
      #Rotate with respect to phosphate
      P_index = dna[idx][0].index
      P_pos = pos[P_index].copy()
      pos = pos - P_pos
      for i in range(end_index-P_index):
        v = pos[i+P_index+1]
        v = np.matmul(v, R_x(angle[0]).T)
        v = np.matmul(v, R_y(angle[1]).T)
        v = np.matmul(v, R_z(angle[2]).T)
        pos[i+P_index+1] = v
      pos = pos + P_pos

  return pos


def anti_rotate_dna(dna, pos, angles):
  '''
  Anti rotates the DNA based on angles, such that anti_rotate_dna(rotate_dna(angle)) = 1
  '''

  start_index = dna[0][0].index
  end_index = dna[-1][-1].index

  for idx, angle in enumerate(angles):
    if idx == 0:
      #Rotate with respect to oxygen
      O_index = dna[idx][-1].index
      O_pos = pos[O_index].copy()
      pos = pos - O_pos
      for i in range(O_index-start_index):
        v = pos[i+start_index]
        v = np.matmul(v, R_z(-1*angle[2]).T)
        v = np.matmul(v, R_y(-1*angle[1]).T)
        v = np.matmul(v, R_x(-1*angle[0]).T)
        pos[i+start_index] = v
      pos = pos + O_pos

    else:
      #Rotate with respect to phosphate
      P_index = dna[idx][0].index
      P_pos = pos[P_index].copy()
      pos = pos - P_pos
      for i in range(end_index-P_index):
        v = pos[i+P_index+1]
        v = np.matmul(v, R_z(-1*angle[2]).T)
        v = np.matmul(v, R_y(-1*angle[1]).T)
        v = np.matmul(v, R_x(-1*angle[0]).T)
        pos[i+P_index+1] = v
      pos = pos + P_pos

  return pos