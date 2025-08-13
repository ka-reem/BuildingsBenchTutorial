#!/bin/bash
#SBATCH --qos=shared
#SBATCH --time=2
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH -C cpu 
#SBATCH -A m4388

srun python /pscratch/sd/k/kareem8/BuildingsBenchTutorial/Tutorials/Final-Project-Modules/train-models.py


