"""
Step1: Calculate t, which is the greedy makespan

Step2: Set upper u and lower l bound using t, upper_bound = t and lower_bound = t//m where m is number of machines

Step3: Create a linear problem LP(Pij, d⃗,t) where
    Pij = 2D array m machines and n jobs.
    Pij the process time of machine i to execute a job j.
    d⃗ = (d1,...,dm) ∈ Z. deadline
    t ∈ Z
    Constrains:
    i ∈ Mj(t)_Sum (xij = 1) for j=1,...,n
    j ∈ Ji(t)_Sum (pij*xij <= di) for i=1,...,m
    xij>=0 for j ∈ Ji(t), i=1,...,m

Step4: Create a decision_procedure LP(Pij, d) using the LP(Pij, d⃗,t) of the rounding theorem
        where d = d1 = d2 = ... = dm = t = d that returns solution if feasible and if not returns none.

Step5: While lower < upper use decision_procedure and search the deadline that gives the minimum makespan
        Return best_solution and the deadline for that solution.

Step6: Round solution using Bipartite Graph
"""
import numpy as np
from RoundingTheorem import *
from BipartiteGraph import *


def greedy_schedule(P: list[list[int]]):
    """
    Computes the makespan of a schedule by assigning each job to the machine with the minimum processing time.

    :param P: 2D array representing the processing times of jobs on different machines.
    :return: The makespan of the schedule, the maximum load among all machines.
    """
    P = np.array(P)  # Convert Pij to a NumPy array
    m = len(P)  # Number of machines
    n = len(P[0])  # Number of jobs

    machines_load = np.zeros(m)  # Initialize the load of each machine

    for j in range(n):
        machine = np.argmin(P[:, j])  # Find machine with minimum processing time for a job j
        machines_load[machine] += P[machine, j]  # Assign job j to the selected machine

    makespan = np.max(machines_load)  # Compute the makespan as the maximum load among machines
    return makespan


def two_relaxed_decision_procedure(P: list[list[int]], d: int):
    """
    A two-relaxed decision procedure LP(P, d) outputs either 'no' or 'almost'; more precisely, for the input (Pij, d):

    If the output is 'almost,' then there exists a solution with makespan at most d, and we return a solution with
    makespan at most p×d.
    If the output is 'no,' then there is no solution with makespan at most d.
    It uses the LP(Pij, d⃗,t) from the RoundingTheorem where d1 = d2 = … dm = t = d

    ***Note .The procedure uses linear programming to determine if such a feasible solution exists.
    However, linear programming can produce solutions that are real numbers, thereby bypassing the integer constraints
    necessary for the practical implementation of the program.
    Consequently, even if the linear problem produces a solution with a makespan of d, it is not guaranteed that there
    will be a corresponding integer solution.
    This is why we return a solution with a makespan at most 2*d.
    :param P:
    :param d: d1 = d2 = … dm = t = d
    """

    di = [d] * len(P)
    solution = LP(P, di, d)
    if solution is not None:
        return LP(P, 2 * di, 2 * d)
    return None


def binary_search_procedure(P: list[list[int]], t: int):
    """
    While lower bound < upper bound run the LP(d,t) decision procedure in order to find the deadline and solution with
    the minimum makespan
    :param P: 2D array m machines and n jobs.
    :param t:
    :return:
    """
    m = len(P)  # number of machines
    upper_bound = t
    lower_bound = t // m

    best_solution = None
    best_d = None
    while lower_bound < upper_bound:
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
    """
    We round the solution of the LP(Pij, d⃗,t) with the use of Bipartite Graph
    :param lp_solution_xij: linear solution
    :param m: machines
    :param n: jobs
    :return: rounded solution
    """
    bipartiteGraph = BipartiteGraph(lp_solution_xij, m, n)
    for i, j in bipartiteGraph.matching:
        lp_solution_xij[i, j].varValue = 1
    for key in lp_solution_xij:
        if lp_solution_xij[key].varValue != 1:
            lp_solution_xij[key].varValue = 0
    return lp_solution_xij
