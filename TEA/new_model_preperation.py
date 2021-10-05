import os
import pandas as pd
from sympy import symbols, Eq, solve

protein = ''
path = ''

#  Create folders for a target protein to remove redundant work
try:
    os.makedirs("./datasets/ga_interim_data/{}".format(protein))
    os.makedirs("./datasets/model_validation/{}".format(protein))
    os.makedirs("./datasets/training/{}".format(protein))
    os.makedirs("./model/{}".format(protein))
except FileExistsError:
    print("Directory exists, change folders name.")


#  Setup data for training and GA from score_sequences.csv
scored_sequences = pd.read_csv(path)
scored_sequences.to_csv("./datasets/ga_interim_data/{}".format(protein))

#  top_iter_0.csv from scored_sequences
top_iter_0 = scored_sequences.df.nlargest(200, 'Entropy')

#  Calculating out a number of aptamers to distribute between train/val/test datasets
#  Because you cannot train on overlapping sequences
from sympy import symbols, solve, simplify, factor
x = symbols('x', positive=True, real=True)

length = len(scored_sequences.index)

expr = (15 * (length - 2*x) * (length-1 - 2*x) / 2 - 70 * x*(x-1)/2 )

sol = solve(expr)[0]


df_test = 
df_val =




import os

os.system("python myOtherScript.py arg1 arg2 arg3")  


