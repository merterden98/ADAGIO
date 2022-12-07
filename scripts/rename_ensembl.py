import argparse
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument('--gtex', '-g', type=str, required=True, help="Path to expression data")
parser.add_argument('--id_map', '-m', type=str, required=True, help="Path to ENSG-to-ENSP map")
parser.add_argument('--out', '-o', type=str, default="expression.txt",help="Path to output results")

def main(gtex: str, id_map: str, out: str):
    
    # load expression data
    data = pd.read_csv(gtex, sep='\t', skiprows=4)
    data.rename(columns={'Gene ID':'ID'}, inplace=True)
    
    # load ENSG-ENSP mapping data
    ensg_ensp_df = pd.read_csv(id_map, sep = '\t', header=None, names=['SP', 'ENSG', 'ENSP'])
    ensg_ensp_dict = dict(zip(ensg_ensp_df.ENSG, ensg_ensp_df.ENSP))
    
    # replace ENSG values with their ENSP counterparts
    data.replace(to_replace=ensg_ensp_dict, inplace=True)

    # remove genes with no match in STRING10 (only keep those that got ENSP values)
    data.drop(data[data['ID'].str.match('ENSG')].index, inplace=True)

    # prepend all genes with '9606.' to match network
    data['ID'] = '9606.' + data['ID']

    # produce reduced CSV of renamed expression data (without unmapped genes)
    data.to_csv(out)

    return(0)

if __name__ == '__main__':
    args = parser.parse_args()
    main(args.gtex, args.id_map, args.out)