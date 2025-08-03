# Short-Term Load Forecasting Using Machine Learning

## Introduction

Short-Term Load Forecasting (STLF) is the process of predicting the electrical energy demand of residential and commercial buildings over short timeframes, ranging from the next hour to the next month [1][2][3]. STLF plays a vital role in efficient energy management [2][3], making it an important research area in the United States government's goal of achieving energy dominance. We leverage the BuildingsBench platform, developed by the National Renewable Energy Laboratory, a U.S. Department of Energy lab, to explore the role of deep learning in STLF [1]. This project will provide hands-on experience in object-oriented programming, working with the PyTorch and Matplotlib libraries, tuning model parameters, and training models on Graphics Processing Units (GPUs). It emphasizes practical implementation with minimal focus on theoretical foundations or extensive code development. Prior coding experience in Python is a plus, but no additional background is required.

## Pre-requisites
We assume you have experience using the command line, as well as some coding experience in at least one programming language. If you're not familiar with Unix or Python, we recommend reviewing introductory material on these topics before proceeding with the tutorials.

- Basic Unix: `https://github.com/olcf/hands-on-with-frontier/tree/master/challenges/Basic_Unix_Vim#basic-unix-and-vim-skills`
- Intro to Python: `https://www.geeksforgeeks.org/python/python-programming-language-tutorial/`

## Repository Structure
<pre> 
BuildingsBenchTutorial/
│
├── Tutorials/
│   │
│   ├── Intro-Modules/
│   │   ├── Develop-Conda-Kernel.md
│   │   ├── Intro-Object-Oriented-Programming.ipynb
│   │   ├── Visualize-Time-Series-Data.ipynb
│   │   ├── Intro-Pytorch.ipynb    
│   │   └── Intro-NN.ipynb
│   │
│   └── Final-Project-Modules/
│       ├── EDA-Dataset.ipynb
│       ├── Train-Model.ipynb
│       └── Post-Data-Analysis.ipynb
│
├── BuildingBench/
│
└── README.md
</pre>

The BuildingsBenchTutorial repository contains two key subdirectories: (1) BuildingsBench and (2) Tutorials. You won’t need to make any changes to the BuildingsBench directory; all development should be done within the Tutorials directory or directly in the terminal. 

## Tutorials
The Tutorials directory contains two subdirectories: (1) Intro-Modules and (2) Final-Project-Modules. Please begin by reviewing the modules in Intro-Modules directory, as they cover foundational concepts that will help you successfully complete the final project task notebooks in the Final-Project-Modules section.

## Expectations
The final project will be a collaborative effort. We expect each group member to contribute their best in completing their assigned section of the project. However, we understand that many participants may not have prior experience in programming or computer science. Therefore, please don’t feel stressed if you’re unable to complete all the tasks—just do your best and support your team where you can. We encourage collaboration among team members, but we strongly discourage anyone from taking over or completing tasks assigned to other group members.

Tools like ChatGPT and Gemini are becoming more common in everyday work. Learning how to use AI effectively is becoming just as important as learning to code. We encourage you to use AI tools to help with your tasks. Using other online resources is also permitted and encouraged.


## Next --> Tutorials/Intro-Modules/Readme.md

## References

[1] Emami, Patrick, Abhijeet Sahu, and Peter Graf. "BuildingsBench: A Large-Scale Dataset of 900K Buildings and Benchmark for Short-Term Load Forecasting." arXiv preprint arXiv:2307.00142 (2023). 
[2] Gross, George, and F. D. Galiana. "Short-Term Load Forecasting." Proceedings of the IEEE, vol. 75, no. 12, 1987, pp. 1558–1573.
[3] Akhtar, Saima, et al. "Short-Term Load Forecasting Models: A Review of Challenges, Progress, and the Road Ahead."Energies, vol. 16, no. 10, 2023, p. 4060. https://doi.org/10.3390/en16104060.

## Authors 
- Nrushad Joshi (ntj@ornl.gov)