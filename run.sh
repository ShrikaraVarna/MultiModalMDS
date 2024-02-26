#!/bin/bash
#SBATCH --job-name=Ubaseline
#SBATCH --output=Ubaseline.out
#SBATCH --error=Ubaseline.err
#SBATCH --mem=128g
#SBATCH --gres=gpu:A6000:1
#SBATCH --time=12:00:00
#SBATCH --mail-type=ALL
#SBATCH --mail-user=svarna@andrew.cmu.edu

# Your job commands go here
torchrun --nproc_per_node 1 train.py --dataset BLiSS --model_dir logs/BLiSS/exp_baseline_updated --log_file log.txt \
        --data_root ../../../../data/tir/projects/tir4/users/svarna/A2Summ/data --batch_size 32