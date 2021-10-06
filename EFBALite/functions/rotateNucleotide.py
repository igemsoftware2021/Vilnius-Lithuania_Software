import numpy as np

R_x = lambda phi: np.array([[1, 0, 0], [0, np.cos(phi), -np.sin(phi)], [0, np.sin(phi), np.cos(phi)]])
R_y = lambda phi: np.array([[np.cos(phi), 0, np.sin(phi)], [0, 1, 0], [-np.sin(phi), 0, np.cos(phi)]])
R_z = lambda phi: np.array([[np.cos(phi), -np.sin(phi), 0], [np.sin(phi), np.cos(phi), 0], [0, 0, 1]])


def rotate_nucleotide(nucleotide, pos, angle):
  '''
  Rotates nucleotide
  '''

  P_index = nucleotide[0].index
  end_index = nucleotide[-1].index

  P_pos = pos[P_index]
  pos = pos - P_pos
  for i in range(end_index-P_index):
    v = pos[i+P_index+1]
    v = np.matmul(v, R_x(angle[0]).T)
    v = np.matmul(v, R_y(angle[1]).T)
    v = np.matmul(v, R_z(angle[2]).T)
    pos[i+P_index+1] = v
  pos = pos + P_pos

  return pos

def anti_rotate_nucleotide(nucleotide, pos, angle):
  '''
  Anti rotates nucleotide
  '''

  P_index = nucleotide[0].index
  end_index = nucleotide[-1].index

  P_pos = pos[P_index]
  pos = pos - P_pos
  for i in range(end_index-P_index):
    v = pos[i+P_index+1]
    v = np.matmul(v, R_z(-1*angle[2]).T)
    v = np.matmul(v, R_y(-1*angle[1]).T)
    v = np.matmul(v, R_x(-1*angle[0]).T)
    pos[i+P_index+1] = v
  pos = pos + P_pos

  return pos