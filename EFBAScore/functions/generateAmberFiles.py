import pexpect
import re

pdb = re.compile('\.(pdb)$')
mol2 = re.compile('\.(mol2)$')

def generate_sequence(dir, target, aptamer, frcmod_file):
  '''
  Generates AMBER files for the specific DNA sequence
  '''
  tleap = pexpect.spawn('tleap')
  tleap.expect(r'(Welcome to LEaP)')

  if frcmod_file != "":
    tleap.sendline(f'loadamberparams {frcmod_file}')
    tleap.expect('Reading force field modification type file')
    tleap.expect(">")

  tleap.sendline('source leaprc.protein.ff14SB')
  tleap.expect('ff14SB protein backbone and sidechain parameters')
  tleap.expect(">")

  tleap.sendline('source leaprc.DNA.OL15')
  tleap.expect('OL15 force field for DNA')
  tleap.expect(">")

  tleap.sendline('source leaprc.gaff2')
  tleap.expect('AMBER General Force Field for organic molecules')
  tleap.expect(">")

  tleap.sendline("set default PBradii mbondi2")
  tleap.expect(">")
  #tleap.expect('Using H(N)-modified Bondi radii')
  
  if pdb.search(target) != None:
    tleap.sendline(f"target = loadpdb {target}")
    tleap.expect('Loading PDB file')
    tleap.expect(">")
  elif mol2.search(target) != None:
    tleap.sendline(f"target = loadmol2 {target}")
    tleap.expect('Loading Mol2 file')
    tleap.expect(">")

  tleap.sendline(f"aptamer = sequence {{{' '.join(aptamer)}}}")
  tleap.sendline("system = combine { target aptamer }")
  tleap.sendline(f"saveamberparm system {dir}/{aptamer[-1]}.prmtop {dir}/{''.join(aptamer[-1])}.inpcrd")
  tleap.expect("(no restraints)")
  tleap.expect(">")
  
  tleap.kill(9)

def generate_target(dir, target, frcmod_file):
  '''
  Generates AMBER files for the target
  '''
  tleap = pexpect.spawn('tleap')
  tleap.expect(r'(Welcome to LEaP)')

  if frcmod_file != "":
    tleap.sendline(f'loadamberparams {frcmod_file}')
    tleap.expect('Reading force field modification type file')
    tleap.expect(">")

  tleap.sendline('source leaprc.protein.ff14SB')
  tleap.expect('ff14SB protein backbone and sidechain parameters')
  tleap.expect(">")

  tleap.sendline('source leaprc.DNA.OL15')
  tleap.expect('OL15 force field for DNA')
  tleap.expect(">")

  tleap.sendline('source leaprc.gaff2')
  tleap.expect('AMBER General Force Field for organic molecules')
  tleap.expect(">")

  tleap.sendline("set default PBradii mbondi2")
  #tleap.expect('Using H(N)-modified Bondi radii')
  
  if pdb.search(target) != None:
    tleap.sendline(f"target = loadpdb {target}")
    tleap.expect('Loading PDB file')
    tleap.expect(">")
  elif mol2.search(target) != None:
    tleap.sendline(f"target = loadmol2 {target}")
    tleap.expect('Loading Mol2 file')
    tleap.expect(">")

  tleap.sendline(f"saveamberparm target {dir}/target.prmtop {dir}/target.inpcrd")
  tleap.expect("(no restraints)")
  tleap.expect(">")

  tleap.kill(9)