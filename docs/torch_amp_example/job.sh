#!/usr/bin/env bash
#SBATCH --job-name torch_apex_example
#SBATCH --gres=gpu:1 #commented out
#SBATCH --qos=short # possible values: short, normal, allgpus
#SBATCH --mem=10G
srun singularity exec pytorch_20.11-py3.sif python torch_amp_example.py
