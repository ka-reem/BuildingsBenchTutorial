# Develop a Conda Kernel

In this tutorial, you will create a `conda` kernel. Please do not skip this step, as the kernel you create in the final exercise will be required to complete the remaining tutorials and the final project. You will perform all tasks for this section in a terminal—not within this notebook.

To open a terminal:

- In the notebook interface, click the “+” symbol on the top menu bar.
- A new window will appear—scroll down and select the “Terminal” icon to launch a terminal session.

### `pip` 101

`pip` is the standard package installer for Python. It allows you to install and manage additional libraries and dependencies that are not included in the Python standard library. To use `pip` on Perlmutter, first load the Python module by running module load python. Once the module is loaded, you can access `pip` from the terminal. Below is a list of essential commands for installing and managing packages in your environment.

| Command         | Description                            |
|------------------|----------------------------------------|
| `pip install`    | Installs the specified Python package  |
| `pip uninstall`  | Uninstalls the specified package       |
| `pip show`       | Displays metadata about the package    |


### `conda` 101

`conda` is a package and environment manager that allows you to install software packages and manage isolated environments. It helps avoid version conflicts and keeps your projects organized. This tutorial requires the use of the terminal. To use `conda` on Perlmutter, first load the Python module by running `module load python`. Once the module is loaded, you can access `conda` by typing `conda`. Below is a list of essential commands needed to create a `conda` kernel for running your tutorials and training deep learning models.


| Command                       | Description                     |
|-------------------------------|---------------------------------|
| `conda create`                | Create a new environment        |
| `conda activate`              | Activate the environment        |
| `conda deactivate`            | Deactivate the environment      |
| `conda install`               | Install a package               |


### STEP 1: Create a Conda Environment

It is important to ensure that the Python module has been loaded before proceeding.

This step creates a new `conda` environment named `myEnv` with Python version 3.11:
- `-n myEnv`  specifies the name of the environment.
- `python=3.11` sets the Python version to 3.11.
- `-y` stands for "yes" and automatically confirms all prompts, so you won’t be asked for manual confirmation.

`conda create -n myEnv python=3.11 -y`

### STEP 2: Activate Environmnet

You activate a Conda environment to install and work with Python packages.
- Activate: `conda activate myEnv`

### STEP 3: Install Packages

Install the required packages using both `pip` and `conda` as needed. Some packages are available through `conda` channels, while others may need to be installed via `pip`.
- Using `pip`: `pip install ipykernel`
- Using `conda`: `conda install conda-forge::lightgbm`

### STEP 4: Create a conda Kernel

This command registers the `conda` environment as a Jupyter kernel, allowing it to be selected when running notebooks.
`python -m ipykernel install --user --name env --display-name MyEnvironment`

- python -m ipykernel install: Uses Python to install a new Jupyter kernel through the ipykernel module.
- `--user`: Installs the kernel for the current user only, without requiring administrative privileges.
- `--name env`: Sets the internal name of the kernel (used by Jupyter to identify the environment). Replace env with the actual environment name (e.g., buildings_bench).
- `--display-name MyEnvironment`: Sets the display name that will appear in the Jupyter interface. Replace MyEnvironment with a readable name, such as Buildings Bench.

### STEP 5: Confirm Kernel Creation
Navigate to the Launcher, and under the Notebook section, the MyEnvironment kernel will be listed.