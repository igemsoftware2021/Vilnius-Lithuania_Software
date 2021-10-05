from __future__ import division
from random import randint, choice
import random, decimal
from numpy import mean
import numpy as np
import pandas as pd
import argparse

parser = argparse.ArgumentParser(description='Breeder acquires new aptamers...')
parser.add_argument("--p", "--path_initial_aptamers"
                        , help="Path to fittest aptamers CSV"
                        , type=str)
parser.add_argument("--o", "--output_location"
                        , help="Location of new breed"
                        , type=str)
parser.add_argument("--l", "--lenght"
                        , help="How many aptamers we should have"
                        , type=int)
parser.add_argument("--i", "--iter"
                        , help="What iteration it is"
                        , type=int)
args = parser.parse_args()


# parents are in the format of ['ACGTCGT', fitness score]
def crossover(parent1, parent2): #prideti iteracija ir generacija
    crossPosition = randint(1,14) # ar galime taikyti distribucija ar kita randomizacija
    initialParent = randint(0,1)

    if initialParent == 0:
        childSeq = parent1[:crossPosition] + parent2[crossPosition:]
    else:
        childSeq = parent2[:crossPosition] + parent1[crossPosition:]
    childSeq = mutate(childSeq)

    return str(childSeq)


#for each base and not once
def mutate(aptamer, mutation_probability = 0.002): #mutacijos
    apt = [char for char in aptamer]
    for i in range(0,15):
        if random.random() <= mutation_probability:
            notList = ['A', 'G', 'C', 'T']
            notList.remove(apt[i])
            apt[i] = random.choice(notList) 
    
    aptamer = "".join(apt) 
    
    return aptamer


def breed(dataset): #prideti kad geresni parent poruotusi dazniau
    aptamers = []

    df = dataset['Sequence'].tolist()
    aptamers.extend(df)
   
    iter = 0
    while len(aptamers) < 1000:
    #for child in range(0,1000 - len(dataset)): # tiesiog while loop padarom
        newAptamer = crossover(choice(df), choice(df))
        aptamers.append(newAptamer)

        if len(aptamers) == 1000: #so there is no duplicates in further process
          aptamers = list(set(aptamers))

    aptamers = pd.DataFrame(aptamers)
    aptamers.columns = ['Sequence']
    return aptamers

def main():
    dataset = pd.read_csv(args.p)
    afterBreed = breed(dataset)

    print("New generation saved in ", args.o)
    afterBreed.to_csv(args.o + 'breed_{}.csv'.format(args.i), encoding='utf-8', index=False)


if __name__=="__main__":
    main()
