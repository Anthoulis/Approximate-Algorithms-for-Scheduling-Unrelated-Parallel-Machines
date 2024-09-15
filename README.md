# Approximate Algorithms for Scheduling Unrelated Parallel Machines

## Description
This project explores the NP-hard problem of scheduling unrelated parallel machines, a significant challenge in optimizing resource utilization. Specifically, it focuses on efficiently assigning independent tasks to different machines to minimize the overall completion time (makespan), with each task having a unique processing time depending on the machine executing it. Due to the NP-hardness of the problem, finding practical solutions relies on approximation algorithms.

The central point of this research is to develop effective models and mechanisms that approximate optimal solutions, ensuring efficient resource utilization and improving the performance of parallel machines. This project employs linear programming methods for finding initial approximate solutions and applies mechanisms based on bipartite graphs for rounding and enhancing these solutions. The integration of these techniques seeks to provide more practical and effective solutions in the context of the problem's complexity.

This project is based on my thesis, **"Approximation Algorithms for Scheduling Unrelated Parallel Machines"**, which analyzes the challenges and potential solutions in task assignment to machines. The full thesis can be accessed [here](https://ikee.lib.auth.gr/record/351786/?ln=en).

## Problem Statement
The problem tackled in this project is scheduling a set of independent tasks on multiple machines, where each machine has different processing times for each task. The objective is to assign tasks to machines in a way that minimizes the makespan (the time at which the last task finishes).

## Features
- Implements several state-of-the-art approximation algorithms for unrelated machine scheduling.
- Includes tools for visualizing scheduling results with Gantt charts.
- Provides evaluations of algorithm performance based on makespan minimization and computational complexity.

## Technologies
- **Python** for the core implementation.
- **PuLP** for linear programming formulations.
- **NetworkX** for graph-based task scheduling models.
- **Matplotlib** for visualizing the task allocation.
- **NumPy** for mathematical operations.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/Anthoulis/Approximate-Algorithms-for-Scheduling-Unrelated-Parallel-Machines.git
2. Navigate to the directory and install the required dependencies:
   ```bash
   cd Approximate-Algorithms-for-Scheduling-Unrelated-Parallel-Machines
   pip install -r requirements.txt

# Approximate Algorithms for Scheduling Unrelated Parallel Machines

## Description
This project implements approximation algorithms for solving the problem of scheduling unrelated parallel machines, which is known to be NP-hard. The goal is to minimize the overall makespan by efficiently allocating tasks to machines, where each task has a different processing time depending on the machine that processes it. The algorithms employed here are inspired by influential research in the field of scheduling theory and optimization, providing efficient task allocations in scenarios with varying machine capabilities.

This project is based on my thesis, **"Approximation Algorithms for Scheduling Unrelated Parallel Machines"**, which dives deeper into algorithmic approaches for this problem. You can access the full thesis [here](https://ikee.lib.auth.gr/record/351786/?ln=en).

## Problem Statement
The problem tackled in this project is scheduling a set of independent tasks on multiple machines, where each machine has different processing times for each task. The objective is to assign tasks to machines in a way that minimizes the makespan (the time at which the last task finishes).

## Features
- Implements several state-of-the-art approximation algorithms for unrelated machine scheduling.
- Includes tools for visualizing scheduling results with Gantt charts.
- Provides evaluations of algorithm performance based on makespan minimization and computational complexity.

## Technologies
- **Python** for the core implementation.
- **PuLP** for linear programming formulations.
- **NetworkX** for graph-based task scheduling models.
- **Matplotlib** for visualizing the task allocation.
- **NumPy** for mathematical operations.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/Anthoulis/Approximate-Algorithms-for-Scheduling-Unrelated-Parallel-Machines.git
2. Navigate to the directory and install the required dependencies:
   ```bash
   cd Approximate-Algorithms-for-Scheduling-Unrelated-Parallel-Machines
   pip install -r requirements.txt

## Prerequisites
- Python 3.x (Make sure Python is installed on your system)
- Pip (Python package manager)

You can check if Python and pip are installed by running:
```bash
python --version
pip --version
```

If not installed, you can install Python from [here](https://www.python.org/downloads/).

## Using a Virtual Environment (Optional)
It's recommended to create a virtual environment to manage dependencies. Run the following commands to create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate     # On Windows

pip install -r requirements.txt
deactivate
python main.py --input data/input_example.txt
python visualize.py --input data/output_results.txt
python -m unittest discover tests/
```
