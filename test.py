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
    if math.fabs(row['timestamp'] - row2['timestamp']) > 0.0001:
        print("Timestamps are different : %s != %s"%(row['timestamp'], row2['timestamp']), file=sys.stderr)
        problem = True
        break
    if math.fabs(row['noisy'] - row2['noisy']) > 0.0001:
        print("noisy data is different: %s != %s"%(row['noisy'], row2['noisy']), file=sys.stderr)
        problem = True
        break
    if math.fabs(row['filtered'] - row2['filtered']) > 0.0001:
        print("The filtered value differs from the ground truth: %s != %s"%(row['filtered'], row2['filtered']), file=sys.stderr)
        print("Check your parameters or your implementation")
        problem = True
        break

if problem:
    print("Problem with %s checking"%args.implementation, file=sys.stderr)
else:
    print("%s implementation looks good."%args.implementation)