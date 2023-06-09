import numpy as np
from linear_programming import *

"""
Step1 : Calculate t which is the greedy makespan
Step2 : Set upper and lower bound using t , upper_bound = t and lower_bound = t//m where m is number of machines
Step3 : Create a linear problem LP(P,d⃗,t)
Let P=(p!/)6Z+ , d=(d~,...,dm)cZ+ and
t 6 Z+. If the linear program LP(P, d, t), given by
Step3 : Create a decision_procedure LP(P,d) using the LP(P,d⃗,t) of the rounding theorem 
        where d = d1 = d2 = .. = dm = t = d
Step4 : While upper - lower > 1 use decision_procedure and search the deadline that gives the minimum makespan
"""


def greedy_schedule(P):
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
        machine = np.argmin(P[:, j])  # Find machine with minimum processing time for job j
        machines_load[machine] += P[machine, j]  # Assign job j to the selected machine

    makespan = np.max(machines_load)  # Compute the makespan as the maximum load among machines
    return makespan


def two_relaxed_decision_procedure(P, d):
    # d1 = d2 = .... dm = t = d
    di = [d] * len(P)
    solution = LP(P, di, d)
    if solution is not None:
        return solution
    return None


def binary_search_procedure(P):
    m = len(P)  # number of machines
    n = len(P[0])  # number of jobs
    t = greedy_schedule(P)  # t = makespan of greedy schedule
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


# TODO: Create the rounding method with the Graphs

def testProcedure():
    print('Testing Procedure.py')

    # Example input data
    Pij = [
        [3, 4, 2, 5, 2, 3, 4, 5, 3, 2, 4, 3, 2, 4, 3, 5, 4, 2, 3, 2, 4, 3, 5, 4, 2, 3, 2, 4, 3, 4],
        [2, 5, 1, 3, 2, 4, 3, 5, 1, 2, 3, 4, 2, 1, 5, 4, 3, 2, 4, 3, 1, 2, 3, 4, 2, 5, 1, 3, 2, 4],
        [4, 3, 2, 1, 5, 4, 2, 3, 1, 2, 3, 4, 2, 1, 5, 4, 3, 2, 4, 3, 1, 2, 3, 4, 2, 5, 1, 3, 2, 4],
        [1, 5, 4, 2, 3, 2, 4, 3, 5, 4, 2, 3, 2, 4, 3, 5, 4, 2, 3, 2, 4, 3, 5, 4, 2, 3, 2, 4, 3, 5],
        [2, 3, 1, 5, 4, 2, 3, 1, 2, 3, 4, 2, 1, 5, 4, 3, 2, 4, 3, 1, 2, 3, 4, 2, 5, 1, 3, 2, 4, 3],
        [3, 4, 2, 5, 2, 3, 4, 5, 3, 2, 4, 3, 2, 4, 3, 5, 4, 2, 3, 2, 4, 3, 5, 4, 2, 3, 2, 4, 3, 5],
        [4, 3, 2, 1, 5, 4, 2, 3, 1, 2, 3, 4, 2, 1, 5, 4, 3, 2, 4, 3, 1, 2, 3, 4, 2, 5, 1, 3, 2, 4],
        [1, 5, 4, 2, 3, 2, 4, 3, 5, 4, 2, 3, 2, 4, 3, 5, 4, 2, 3, 2, 4, 3, 5, 4, 2, 3, 2, 4, 3, 5]
    ]

    # Test greedy_schedule
    makespan = greedy_schedule(Pij)
    print("Makespan (Greedy Schedule):", makespan)

    # Test binary_search_procedure
    solution = binary_search_procedure(Pij)
    if solution is not None:
        objective_value, decision_vars = solution
        print("Optimal Objective Value:", objective_value)
        print("Decision Variables:")
    else:
        print("No feasible solution found.")


if __name__ == "__main__":
    testProcedure()
