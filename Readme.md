# Short-Term Load Forecasting Using Machine Learning

## Introduction

Short-Term Load Forecasting (STLF) is the process of predicting the electrical energy demand of residential and commercial buildings over short timeframes, ranging from the next hour to the next month [1][2][3]. STLF plays a vital role in efficient energy management [2][3], making it an important research area in the United States government's goal of achieving energy dominance. We leverage the BuildingsBench platform, developed by the National Renewable Energy Laboratory, a U.S. Department of Energy lab, to explore the role of deep learning in STLF [1]. This project will provide hands-on experience in object-oriented programming, working with the PyTorch and Matplotlib libraries, tuning model parameters, and training models on Graphics Processing Units (GPUs). It emphasizes practical implementation with minimal focus on theoretical foundations or extensive code development. Prior coding experience in Python is a plus, but no additional background is required.

References

[1] Emami, Patrick, Abhijeet Sahu, and Peter Graf. "BuildingsBench: A Large-Scale Dataset of 900K Buildings and Benchmark for Short-Term Load Forecasting." arXiv preprint arXiv:2307.00142 (2023). 

[2] Gross, George, and F. D. Galiana. "Short-Term Load Forecasting." Proceedings of the IEEE, vol. 75, no. 12, 1987, pp. 1558–1573.

[3] Akhtar, Saima, et al. "Short-Term Load Forecasting Models: A Review of Challenges, Progress, and the Road Ahead."Energies, vol. 16, no. 10, 2023, p. 4060. https://doi.org/10.3390/en16104060.


## Repository Structure
<pre> 
BuildingsBenchTutorial/
│
├── Tutorials/
│   │
│   ├── Intro-Modules/
│   │   ├── Develop-Conda-Kernel.ipynb
│   │   ├── Intro-Object-Oriented-Programming.ipynb
│   │   ├── Intro-Pytorch.ipynb
│   │   ├── Intro-SLURM.ipynb
│   │   └── Visualize-Time-Series-Data.ipynb
│   │
│   └── Deep-Learning-Modules/
│       ├── Pre-Trained-Transformer.ipynb
│       ├── [TBD]
│       └── [TBD]
│
├── BuildingBench/
│
└── README.md
</pre>

The BuildingsBenchTutorial repository contains two key subdirectories: (1) BuildingsBench and (2) Tutorials. You will not need to make any changes to the BuildingsBench directory; all development should take place within the Tutorials directory.

### Tutorials

The Tutorials directory contains two subdirectories: (1) Intro-Modules and (2) Deep-Learning-Modules. Please begin by reviewing the modules in Intro-Modules, as they cover foundational concepts that will help you complete the tutorials in the Deep-Learning-Modules directory.

#### Intro-Modules

Within Intro-Modules, you must first complete the Develop-Conda-Kernel.ipynb notebook and create a kernel, as this is required to run any of the remaining tutorials. After that, if you're already familiar with object-oriented programming, you may complete the tutorials in any order. However, the recommended sequence is:

- Develop-Conda-Kernel.ipynb
- Intro-Object-Oriented-Programming.ipynb
- Intro-PyTorch.ipynb
- Visualize-Time-Series-Data.ipynb
- Intro-SLURM.ipynb

##### Develop-Conda-Kernel.ipynb

#### Deep-Learning-Modules
[TBD]