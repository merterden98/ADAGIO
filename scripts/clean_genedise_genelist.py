# Usage: python3 clean_genedise_genelist.py -i <input filepath> -o <output filepath>
# Make sure input file path != output file path or will overwrite old data

import pandas as pd
import argparse

parser = argparse.ArgumentParser(description='genelist files')
parser.add_argument('-i', type=argparse.FileType('r')) # input file
parser.add_argument('-o', type=str) # output file

def main(args: argparse.Namespace):
    genelist = pd.read_csv(args.i)
    clean_genelist = pd.DataFrame(genelist.STRING_id)
    clean_genelist.to_csv(args.o, header=False, index=False)

if __name__ == '__main__':
    args = parser.parse_args()
    main(args)