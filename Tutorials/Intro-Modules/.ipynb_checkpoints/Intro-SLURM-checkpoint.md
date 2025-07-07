# SLURM 101

The goals of this exercise are as follows:
- Familiarize yourself with batch scripts.
- Understand how to modify and submit an existing batch script.
- Learn how to run a job using Slurm.
- Explore job layout on a node and understand how to query the queue for your job’s status and interpret the results.

Perlmutter uses SchedMD's Slurm Workload Manager for job scheduling and management. Slurm provides functionality similar to other schedulers such as IBM’s LSF but offers unique control over Perlmutter’s resources through custom commands and options. Slurm documentation for each command is available via the man utility and online at: https://slurm.schedmd.com/man_index.html. Additional documentation can be found at: https://slurm.schedmd.com/documentation.html. 

Some common Slurm commands are summarized below:

Command     | Action/Task
------------|------------------------------
squeue      | Show the current job queue
sbatch      | Submit a batch script
srun        | Launch a parallel job
sacct       | View accounting information for jobs or job steps
scancel     | Cancel a job or job step

The most common way to interact with the batch system is via batch scripts. A batch script is simply a shell script with added directives to request various resources from, or provide specific information to, the scheduling system. Aside from these directives, the batch script consists of the series of commands needed to set up and run your job.

The example batch script, submit.sl looks like this:
```bash
#!/bin/bash

#SBATCH --job-name=<job_name>                   
#SBATCH --qos=<QOS>                             
#SBATCH --constraint=<architecture>             
#SBATCH --nodes=<nnodes>                        
#SBATCH --gpus=<num_gpus>                       
#SBATCH --time=hh:mm:ss                         
#SBATCH --account=<project_name>                
#SBATCH --output=%x-%j.out                     

srun -n <num_mpi_processes> <executable>
```

In the script, Slurm directives are preceded by `#SBATCH`, making them appear as comments to the shell. Slurm looks for these directives through the first non-comment, non-whitespace line. Options after that will be ignored by Slurm (and the shell).

| **Line** | **Script Content**                                     | **Short Form** | **Description**                                                               |
|----------|--------------------------------------------------------|----------------|-------------------------------------------------------------------------------|
| 1        | `#!/bin/bash`                                          | –              | Shell interpreter line — tells the system to use the Bash shell              |
| 2        | `#SBATCH --job-name=<job_name>`                        | `-J`           | Name for the job (shown in job queue)                                        |
| 3        | `#SBATCH --qos=<QOS>`                                  | `-q`           | Quality of Service — prioritization tier or job class                        |
| 4        | `#SBATCH --constraint=<architecture>`                  | `-C`           | Specifies required node architecture (e.g., CPU, GPU)                        |
| 5        | `#SBATCH --nodes=<nnodes>`                             | `-N`           | Number of compute nodes to allocate                                          |
| 6        | `#SBATCH --gpus=<num_gpus>`                            | `-G`           | Number of GPUs requested (optional; for GPU jobs only)                       |
| 7        | `#SBATCH --time=hh:mm:ss`                              | `-t`           | Walltime requested (hh:mm:ss format)                                         |
| 8        | `#SBATCH --account=<project_name>`                     | `-A`           | Project name to charge for compute usage                                     |
| 9        | `#SBATCH --output=%x-%j.out`                           | `-o`           | Output filename with job name (`%x`) and job ID (`%j`)                       |
| 10       | `srun -n <num_mpi_processes> <executable>`             | –              | Launches the application using `srun` with specified number of MPI tasks     |

A job transitions through several states during its lifetime. Common ones include:

| Code | State      | Description                                                            |
|------|------------|------------------------------------------------------------------------|
| CA   | Canceled   | The job was canceled (either by the user or an administrator)          |
| CD   | Completed  | The job completed successfully (exit code 0)                           |
| CG   | Completing | The job is in the process of completing (some processes still running) |
| PD   | Pending    | The job is waiting for resources to be allocated                       |
| R    | Running    | The job is currently running                                            |

You can view the current status of a job using the `squeue` command.

## Exercise 1: Create a SLURM Script

Create a batch script named `hello_world.sl`, open a terminal and type `vi hello_world.sl`. 

Press `i` to enter insert mode, then paste the following script and update all `<update>` fields with appropriate values before saving.

```bash
#!/bin/bash
#SBATCH --account=<update>               # Set your account name
#SBATCH --job-name=<update>              # Set a descriptive job name
#SBATCH --output=hello_world_output.out  # Fixed output filename (overwrites if job is rerun)
#SBATCH --time=<update>                  # Set the walltime to 2 minutes
#SBATCH --partition=<update>             # Use the regular partition
#SBATCH --nodes=<update>                 # Request 1 compute node
#SBATCH --constraint=<update>            # Set cpu constraint 

srun -n 4 -c 1 bash -c 'echo "Hostname: $(hostname), Task: $SLURM_PROCID says Hello World"'
```

Save and exit `vi`: Press `Esc`, then type `:wq` and press `Enter`

Submit the script:`sbatch hello_world.sl`

View output after completion: `cat hello_world_output.out`

## Exercise 2: Explore Slurm Commands

Follow the steps outlined in Exercise 1 to create a SLURM batch script named `explore_command.sl`, add the script below to the file, and save it.

```bash
#!/bin/bash
#SBATCH --account=<update>               # Set your account name
#SBATCH --job-name=<update>              # Set a descriptive job name
#SBATCH --output=explore_slurm.out       # Fixed output filename (overwrites if job is rerun)
#SBATCH --time=00:07:00                  # Set the walltime to 7 minutes
#SBATCH --partition=regular              # Use the regular partition
#SBATCH --nodes=1                        # Request 1 compute node
#SBATCH --constraint=<update>            # Set cpu constraint 

sleep 420
```
Now, execute the SLURM script using the following command: `sbatch explore_command.sl`

Note: This job runs for only 7 minutes. After that, it will no longer appear in active job queries. If needed, you can re-run the job by submitting the same script again with the same command.

- Monitor your job while it is running, use: `squeue -u $USER`.

The `squeue` command lists your active jobs. Look for the `JOBID` in the output. Once you have the `JOBID`, you can explore additional SLURM commands:
- View detailed information about the job, including allocated nodes, resources, and state: `scontrol show job <JOBID>`
- Cancel the job before it finishes if needed: `scancel <JOBID>`

## Exercise 3: Train a Deep Learning Model

Follow the steps outlined in Exercise 1 to create a SLURM batch script named train_model.sl, add the script below to the file, and save it. The script introduces four new SLURM flags, which are explained below.

| **SLURM Flag**      | **Description**                                                                 |
| ------------------- | ------------------------------------------------------------------------------- |
| `--ntasks-per-node` | Number of parallel tasks (e.g., MPI ranks) to launch on each node.              |
| `-c`                | Number of CPU cores allocated to each task. Uses 128 logical cores with SMT.    |
| `--gpus-per-task`   | Number of GPUs allocated per task. Here, each of 4 tasks gets 1 GPU.            |
| `--gpu-bind=none`   | No automatic GPU binding; all GPUs are visible to all tasks for manual control. |


```bash
#!/bin/bash
#SBATCH --account=<update>               # Set your account name
#SBATCH --job-name=<update>              # Set a descriptive job name
#SBATCH --output=train_model.out         # Fixed output filename (overwrites if job is rerun)
#SBATCH --time=<update>                  # Set the walltime to 5 minutes
#SBATCH --partition=<update>             # Use the regular partition
#SBATCH --nodes=<update>                 # Request 1 compute node
#SBATCH --constraint=<update>            # Set gpu constraint 
#SBATCH --ntasks-per-node=4              # Launch 4 tasks on the node
#SBATCH -c 32                            # Allocate 32 CPU cores per task
#SBATCH --gpus-per-task=1                # Assign 1 GPU to each task
#SBATCH --gpu-bind=none                  # Do not bind specific GPUs to tasks

module load python
conda activate BuildingsBenchEnv

export MASTER_ADDR=$(scontrol show hostname $SLURM_NODELIST | head -n 1)  # Use 1st node as master
export MASTER_PORT=29500
export WORLD_SIZE=$((SLURM_NNODES * SLURM_NTASKS_PER_NODE))
export BUILDINGS_BENCH=/pscratch/sd/n/nrushad/Dataset/

srun python3 scripts/pretrain.py \
	--model TransformerWithGaussian-S \
    --num_buildings=1000 \
	--disable_wandb 
```