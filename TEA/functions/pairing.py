import pandas as pd
import numpy as np
from sklearn.utils import shuffle
import argparse
import os
pd.options.mode.chained_assignment = None  # default='warn'


parser = argparse.ArgumentParser(description='Breeder acquires new aptamers...')
parser.add_argument("--p", "--path_initial_aptamers"
                        , help="Path to evaluatedd aptamers with M.A.W.S"
                        , type=str)
parser.add_argument("--h", "--later"
                        , help="Path to evaluatedd aptamers with M.A.W.S"
                        , type=str)
parser.add_argument("--o", "--output_path"
                        , help="Path to save new generation of aptamers"
                        , type=str)
parser.add_argument("--i", "--iter"
                        , help="The iteration number"
                        , type=str)
parser.add_argument("--l", "--labeled"
                        , help="Is data labeled"
                        , action="store_true")
args = parser.parse_args()


def pairWithLabel(df):
    apt1 = pd.DataFrame(columns=['Sequence1', 'Entropy1'])
    apt2 = pd.DataFrame(columns=['Sequence2', 'Entropy2'])

    for first in range(0,len(df)):
        x = pd.DataFrame({'Sequence1':df.loc[first,'Sequence'],'Entropy1':df.loc[first,'Entropy']},index = range(1))
        apt1 = apt1.append([x]*(len(df) - first - 1), ignore_index=True)
            
    for second in range(1,len(df) + 1):
        y = pd.DataFrame({'Sequence2':df.loc[second:,'Sequence'],'Entropy2':df.loc[second:,'Entropy']})
        apt2 = apt2.append(y, ignore_index=True)

    dataset = apt1.join(apt2)
    dataset["Label"] = np.where(dataset.eval("Entropy1 >= Entropy2"), 1, 0)
    dataset = shuffle(dataset)

    return dataset[['Sequence1', 'Sequence2', 'Label']]


def pairWithoutLabel():
    apt1 = pd.DataFrame(columns=['Sequence1'])
    apt2 = pd.DataFrame(columns=['Sequence2'])

    df = pd.read_csv(args.h)

    for first in range(0,len(df)):
      x = pd.DataFrame.from_records({'Sequence1':[df.loc[first, 'Sequence']]})
      apt1 = apt1.append([x]*(len(df) - first - 1), ignore_index = True)
    
      y = pd.DataFrame({'Sequence2':df.loc[first+1:,'Sequence']})
      apt2 = apt2.append(y, ignore_index=True)

    dataset = apt1.join(apt2)

    return dataset[['Sequence1', 'Sequence2']]



def balanceData(dataset):
    counts = dataset['Label'].value_counts()

    if counts.loc[0] >= counts.loc[1]:
        change = int((counts.loc[0] - counts.loc[1])/2)
        value = 0
    else:
        change = int((counts.loc[1] - counts.loc[0])/2)
        value = 1

    zeros = dataset[(dataset['Label'] == value)]
    zerosIndexes = zeros.sample(change).index
    zeros.loc[zerosIndexes,'Label'] = int(abs(value - 1))
    
    dataset.update(zeros)
    dataset['Label'] = dataset['Label'].astype(int)

    return dataset


def main():

    if args.l:
        df = pd.read_csv(args.p)
        path = './datasets/training/'

        #  First of all we pair up every aptamer together, then balance number of accurancies of classes 1 and 0 to train those equally
        data = pairWithLabel(df)
        dataset = balanceData(data)

        #  80% training, 10% validating, 10% testing
        train, test, val = np.split(dataset, [int(.8*len(dataset)), int(.9*len(dataset))]) 
    
        #  Find the top N aptamers from the score_sequences.csv
        top = df.nlargest(200, 'Entropy')

        print("Migrating preprocessed training data to {}".format(path))

        dataset.to_csv('./datasets/training/full_comparison.csv', encoding='utf-8', index=False)
        train.to_csv('./datasets/training/train.csv', encoding='utf-8', index=False)
        test.to_csv('./datasets/training/test.csv', encoding='utf-8', index=False)
        val.to_csv('./datasets/training/val.csv', encoding='utf-8', index=False)


        folder = './datasets/ga_interim_data/{}'.format(args.o)
        if not os.path.exists(folder):
            os.mkdir(folder)  

        top.to_csv('{}/top_iter_0.csv'.format(folder), encoding='utf-8', index=False)
    else:
     
        dataset = pairWithoutLabel()
        print("Saving new generation {} to {}".format(args.i, args.o))
        dataset.to_csv('{}/iteration_{}.csv'.format(args.o, args.i), encoding='utf-8', index=False)
    

if __name__ == "__main__":
    main()