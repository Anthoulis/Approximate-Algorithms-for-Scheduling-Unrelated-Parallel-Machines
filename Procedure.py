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
        where d = d1 = d2 = ... = dm = t = d that returns 'no' or 'almost'.

Step5: Use binary search procedure.
        While lower != upper, search the deadline that gives the minimum makespan while saving the best solution found
        Return best_solution and the deadline for that solution.
"""
import numpy as np
from RoundingTheorem import *
from BipartiteGraph import *
from SchedulingProblem import SchedulingProblem


def greedy_schedule(P: list[list[int]]) -> int:
    """
    Computes the makespan of a schedule by assigning each job to the machine with the minimum processing time.
    :param P: 2D array representing the processing times of jobs on different machines.
    :return: The makespan of the schedule, the maximum load among all machines.
    """
    P, m, n, machines_load = np.array(P), len(P), len(P[0]), np.zeros(len(P))
    for j in range(n):
        machine = np.argmin(P[:, j])  # Find machine with minimum processing time for a job j
        machines_load[machine] += P[machine, j]  # Assign job j to the selected machine
    return int(np.max(machines_load))  # Compute the makespan as the maximum load among machines


def round_lpSolution(lp_xij: dict[tuple[int, int], LpVariable], m: int, n: int):
    """
    We round the solution of the LP(Pij, d⃗,t) with the use of Bipartite Graph
    If the graph G we create doesn't have the property of a pseudoforest that means that there is a better solution.
    We stop the rounding and we return None.
    :param lp_xij: Linear decision xij
    :param m: machines
    :param n: jobs
    :return: rounded solution
    """
    # Using LP xij, we create a bipartite graph G
    bipartiteGraphG = BipartiteGraphG(lp_xij, m, n)
    if bipartiteGraphG.is_pseudoforest:

        # Removing degree 1 jobs we get a graph G'
        bipartiteGraphG2 = BipartiteGraphG2(bipartiteGraphG.graph)
        # We round the solution according to the matching
        for i, j in bipartiteGraphG2.matching:
            lp_xij[i, j].varValue = 1
        for key in lp_xij:
            if lp_xij[key].varValue != 1:
                lp_xij[key].varValue = 0
        return lp_xij, bipartiteGraphG, bipartiteGraphG2
    return None


def two_relaxed_decision_procedure(P: list[list[int]], d: int):
    """
    The decision process yields either 'no' or 'almost'; more precisely, in the input (P, d):
        If the output is 'almost,' it means that there is a solution with makespan at most d.
    This arises from the fact that the initial linear problem (LP) with parameters d_1=d_2=⋯=ⅆ_m=t has a solution with
    makespan at most d.
    Then, using bipartite graphs as discussed in the previous chapter, we proceed to round this solution.
        If the rounding is successful, and the generated graph is pseudoforest (indicating that the LP solution is
    an extreme point), we proceed to calculate the makespan from the rounded integer program.
    If the makespan is at most
    2*d, then this solution is considered successful.
    If the output is 'no,' then there is no solution with makespan at
    most d.
    :param P:
    :param d: D1 = d2 = … dm = t = d
    :return lp_solution_rounded_solution, GraphG, GraphG'
    """

    di = [d] * len(P)
    solution = LP(P, di, d)
    if solution:
        rounded = round_lpSolution(solution[1], len(P), len(P[0]))
        if rounded:
            if rounded[1].is_pseudoforest:
                makespan = calculate_makespan(P, rounded[0])
                if makespan <= 2 * d:
                    return SchedulingProblem(P, solution, d, (makespan, rounded[0]), rounded[1], rounded[2])
    return None


def binary_search_procedure(P: list[list[int]]):
    """
    While lower_bound != upper_bound run the LP(d,t) decision procedure in order to find the deadline and solution with
    the minimum makespan
    :param P: 2D array m machines and n jobs.
    :return: Final result.
    An approximate solution using Linear Programming, Bipartite Graph, 2-Relaxed Decision and Binary Search Procedure
    """
    t = greedy_schedule(P)
    m, upper_bound, lower_bound = len(P), t, t // len(P)
    best_solution, best_d = None, None

    best_makespan = None

    while lower_bound != upper_bound:
        d = (upper_bound + lower_bound) // 2
        if result := two_relaxed_decision_procedure(P, d):  # If it is a yes instance
            upper_bound = d
            if best_makespan is None or best_makespan < result.makespan:
                best_solution = result
        else:
            lower_bound = d + 1
    if best_solution:
        best_solution.t = t
    return best_solution
