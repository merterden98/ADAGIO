#
# brain_not_brain.py
# updated on: 09-16-2021
# updated on: 12-2-2022
#

import pandas as pd
import numpy as np
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--gtex_path', '-g', type=str, required=True, help="Path to GTex data.")
parser.add_argument('--output_prefix', '-o', type=str, required=True, help="Path dir where expression data should be stored")

# store one row of output information: Gene ID, Gene Name, and whether it has 
# been identified as a brain gene.
def apply_write(row, is_brain):
    output_list.append([row['ID'], row['Gene Name'], is_brain])

# records a 1 if a gene meets the "brain gene" cutoff, 0 otherwise. Retains 
# Gene ID (ENSEMBL) and Gene Name.
def apply_brain(row, cutoff, brain_regions):
    for x in brain_regions:
        if (float(row[x]) >= cutoff):
            apply_write(row, 1) 
            return
    apply_write(row, 0)

def get_cutoffs(input, quantiles):
    numeric_input = input.drop(['ID', 'Gene Name'], axis=1).astype(float)
    return np.nanquantile(a=numeric_input.to_numpy(), q=quantiles)

def main(gtex_path: str, output_prefix: str):
    # create a list of brain region keys
    brain_regions = ['Brodmann (1909) area 24', 
                    'Brodmann (1909) area 9', 
                    'C1 segment of cervical spinal cord',
                    'amygdala', 
                    'caudate nucleus', 
                    'cerebellar hemisphere', 
                    'cerebellum', 
                    'cerebral cortex',
                    'hippocampus proper', 
                    'hypothalamus', 
                    'nucleus accumbens', 
                    'pituitary gland', 
                    'putamen',
                    'substantia nigra']

    quantiles = [0.25, 0.5, 0.75, 0.95, 0.98]

    gtex_data = pd.read_csv(gtex_path)
    gtex_data.fillna(0, inplace=True) #fill empty values with 0s

    cutoffs = get_cutoffs(gtex_data, quantiles) 
    print(cutoffs)

    # output filename format: "is_brain_q<quantile>.tsv"
    for i in range(len(cutoffs)):
        global output_list
        output_list = []
        gtex_data.apply(apply_brain, axis=1, args=(cutoffs[i], brain_regions,))
        output_df = pd.DataFrame(output_list)
        filename = "is_brain_q" + str(quantiles[i]) + ".tsv" 
        output_df.to_csv(output_prefix + filename, sep='\t', index=False, header=False)

if __name__ == "__main__":
    args = parser.parse_args()
    main(args.gtex_path, args.output_prefix)