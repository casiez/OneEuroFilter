# Gery Casiez
# August 2023

import math
import sys
import pandas
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('implementation')
parser.add_argument('filename')
args = parser.parse_args()

df = pandas.read_csv('groundTruth.csv')
df2 = pandas.read_csv(args.filename)

problem = False

if df.shape[0] != df2.shape[0]:
    print("The test file does not have the correct number of lines.")
    sys.exit()

for (index, row), (index2, row2) in zip(df.iterrows(), df2.iterrows()):
    if row['timestamp'] != row2['timestamp']:
        print("Timestamps are different!")
        problem = True
        break
    if row['noisy'] != row2['noisy']:
        print('noisy data is different!')
        problem = True
        break
    if math.fabs(row['filtered'] - row2['filtered']) > 0.001:
        print("The filtered value differs from the ground truth.")
        print("Check your parameters or your implementation")
        problem = True
        break

if problem:
    print("Problem with %s cheching"%args.implementation, file=sys.stderr)
else:
    print("%s implementation looks good."%args.implementation)