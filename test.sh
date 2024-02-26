#!/bin/bash
#SBATCH --job-name=test
#SBATCH --output=test.out
#SBATCH --error=test.err
#SBATCH --mem=128g
#SBATCH --gres=gpu:A6000:1
#SBATCH --time=12:00:00
#SBATCH --mail-type=ALL
#SBATCH --mail-user=svarna@andrew.cmu.edu

# Your job commands go here
torchrun --nproc_per_node 1 train.py --dataset BLiSS --test --log_file log.txt \
        --data_root ../../../../data/tir/projects/tir4/users/svarna/A2Summ/data --checkpoint logs/BLiSS/exp_baseline_updated/BLiSS/checkpoint