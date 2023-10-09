"""Step1 Linear Problem LP(P, d ⃗,t): In the first step, we formulate a linear problem (LP) that represents the
scheduling problem. Our objective is to ensure the correct ordering of tasks on machines and their compliance with
deadlines.

Step2 Rounding Methodology: We employ bipartite graphs to round the solution obtained from step 1 of the linear
problem to an integer solution. Initially, we construct a graph G according to the LP solution. If it is a pseudoforest,
we proceed; otherwise, this implies a better solution exists. Subsequently, a graph G' is derived from G by removing
job nodes with rank=1. Then, we perform matching and convert the non-integer solution.

Step3 2-Relaxed Decision Process LP(P, d): Utilizes LP(P, d ⃗,t) with d_1=d_2=⋯=ⅆ_m and the Rounding Methodology to
round the non-integer solution. It produces a solution if feasible, returning "almost" as observed; otherwise,
it returns "no."

Step4 Upper and Lower Limit Computation: Using the Greedy algorithm, we calculate a greedy schedule, and the makespan
of this greedy schedule constitutes the upper limit t. We set the lower limit t/m, where m is the number of machines.

Step5 Binary Search: The final step is to execute the binary search process. Until the lower limit equals the upper
limit, we set d=⌊1/2 (u+l)⌋. If the 2-Relaxed Decision Process LP(P, d) returns a solution, then the upper limit
becomes d; otherwise, the lower limit becomes d + 1. Simultaneously, we store the solution with the smallest
makespan."""
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
        bipartiteGraphG2 = BipartiteGraphG2(bipartiteGraphG.graph)  # Removing degree 1 jobs we get a graph G'
        # We round the solution according to the matching
        rounded_xij = lp_xij.copy()
        for i, j in bipartiteGraphG2.matching:
            rounded_xij[i, j].varValue = 1
        for key in lp_xij:
            if lp_xij[key].varValue != 1:
                rounded_xij[key].varValue = 0
        return rounded_xij, bipartiteGraphG, bipartiteGraphG2
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
    best_solution = None

    while lower_bound != upper_bound:
        d = (upper_bound + lower_bound) // 2
        if result := two_relaxed_decision_procedure(P, d):  # If it is a yes instance
            upper_bound = d
            if best_solution is None or best_solution.makespan < result.makespan:
                best_solution = result
        else:
            lower_bound = d + 1
    if best_solution:
        best_solution.t = t
    return best_solution
