#!/bin/bash
#SBATCH -J run_tissue_rwt
#SBATCH --time=00-12:00:00
#SBATCH --mem=128GB
#SBATCH --output=MyJob.%j.%N.out  #saving standard output to file, %j=JOBID,%N=NodeName
#SBATCH --error=MyJob.%j.%N.err   #saving standard error to file, %j=JOBID,%N=NodeName
#SBATCH --mail-type=ALL
#SBATCH --mail-user=megan.gelement@tufts.edu


./tissue_reweight_by_algs_exp.py -t /cluster/tufts/cowenlab/mgelem01/E-MTAB-5214/tissue_files -g /cluster/tufts/cowenlab/mgelem01/tmap/data/alzheimers -a all
