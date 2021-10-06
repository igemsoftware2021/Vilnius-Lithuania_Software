from itertools import groupby

def read_fasta(file):
  """
  Reads a fasta file
  """
  fh = open(file, "r")
  faiter = (x[1] for x in groupby(fh, lambda line: line[0] == ">"))
  result = []
  for header in faiter:
    result.append({
      "header": header.__next__()[1:].strip(),
      "sequence": "".join(s.strip() for s in faiter.__next__())
    })
  fh.close()
  return result

def write_fasta(file, sequences):
  """
  Writes to a fasta file
  """
  fh = open(file, "w")
  for seq in sequences:
    fh.writelines([">" + seq["header"] + "\n", seq["sequence"] + "\n", "\n"])
  fh.close()