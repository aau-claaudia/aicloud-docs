#!/usr/bin/env bash
#SBATCH --job-name MySlurmJob
#SBATCH --partition batch # equivalent to PBS batch
#SBATCH --time 0:05:00 # Run 5 minutes
##SBATCH --gres=gpu:1 #commented out
#SBATCH --qos=normal # possible values: short, normal, allgpus

srun echo hello world from sbatch on node $SLURM_NODELIST
