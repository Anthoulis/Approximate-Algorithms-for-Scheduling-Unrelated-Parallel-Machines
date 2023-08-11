import numpy as np

from RoundingTheorem import *
from BipartiteGraph import *

"""
Step1 : Calculate t which is the greedy makespan

Step2 : Set upper u and lower l bound using t , upper_bound = t and lower_bound = t//m where m is number of machines

Step3 : Create a linear problem LP(P,d⃗,t) where 
    P = 2D array m machines and n jobs. Pij the process time of machine i to execute job j.
    d⃗ = ( d1,...,dm ) ∈ Z .  deadline
    t ∈ Z
    Constrains:
    i ∈ Mj(t)_Sum ( xij = 1 ) for j=1,...,n
    j ∈ Ji(t)_Sum ( pij*xij <= di ) for i=1,...,m
    xij>=0 for j ∈ Ji(t),  i=1,...,m

Step4 : Create a decision_procedure LP(P,d) using the LP(P,d⃗,t) of the rounding theorem 
        where d = d1 = d2 = .. = dm = t = d that returns solution if feasible and if not returns none.
        
Step5 : While upper - lower > 1 use decision_procedure and search the deadline that gives the minimum makespan
        Return best_solution and the deadline for that solution.

Step6 : Round solution using Bipartite Graph
"""


def greedy_schedule(P: list[list[int]]):
    """
    Computes the makespan of a schedule by assigning each job to the machine with the minimum processing time.
    Args:
        P (numpy.ndarray): 2D array representing the processing times of jobs on different machines.
                           Shape: (m, n), where m is the number of machines and n is the number of jobs.
    Returns:
        int: The makespan of the schedule, i.e., the maximum load among all machines.
    """
    P = np.array(P)  # Convert P to a NumPy array
    m = len(P)  # Number of machines
    n = len(P[0])  # Number of jobs

    machines_load = np.zeros(m)  # Initialize the load of each machine

    for j in range(n):
        machine = np.argmin(P[:, j])  # Find machine with minimum processing time for a job j
        machines_load[machine] += P[machine, j]  # Assign job j to the selected machine

    makespan = np.max(machines_load)  # Compute the makespan as the maximum load among machines
    return makespan


def two_relaxed_decision_procedure(P: list[list[int]], d: int):
    # d1 = d2 = .... dm = t = d
    di = [d] * len(P)
    solution = LP(P, di, d)
    if solution is not None:
        return solution
    return None


def binary_search_procedure(P: list[list[int]], t: int):
    m = len(P)  # number of machines
    upper_bound = t
    lower_bound = t // m

    best_solution = None
    best_d = None
    while upper_bound - lower_bound > 1:
        d = (upper_bound + lower_bound) // 2
        solution = two_relaxed_decision_procedure(P, d)
        if solution is not None:
            upper_bound = d
            if best_solution is None or solution[0] < best_solution[0]:
                best_solution = solution
                best_d = d
        else:
            lower_bound = d + 1

    return best_solution, best_d


def round_lpSolution(lp_solution_xij: dict[tuple[int, int], LpVariable], m: int, n: int):
    bipartiteGraph = BipartiteGraph(lp_solution_xij, m, n)
    for i, j in bipartiteGraph.matching:
        lp_solution_xij[i, j].varValue = 1
    for key in lp_solution_xij:
        if lp_solution_xij[key].varValue != 1:
            lp_solution_xij[key].varValue = 0
    return lp_solution_xij
