"""
This file solves the minimum makespan scheduling problem using Integer Programming (IP).
It finds the optimal solution by searching the entire solution space.
It will require a lot of computational time for large-scale problems.
"""

from pulp import *
from generate_data import read_csv_file
from SchedulingProblem import SchedulingProblem


def integer_programming(Pij: []):
    """
    Solves the minimum makespan scheduling problem using Integer Programming.

    :param Pij: 2D list representing the time it takes for a job j to execute on machine i
    :return: Optimal makespan and the corresponding xij matrix
    """

    # Number of machines and jobs
    m = len(Pij)
    n = len(Pij[0])

    # Initialize the integer programming problem
    prob = LpProblem("Minimum_Makespan_Scheduling", LpMinimize)

    # Create a variable for the makespan (objective is to minimize this)
    makespan = LpVariable("makespan", 0, cat="Integer")

    # Objective Function: Minimize makespan
    prob += makespan, "Objective"

    # Create binary decision variables for the xij matrix
    x = LpVariable.dicts("x", [(i, j) for i in range(m) for j in range(n)], lowBound=0, upBound=1, cat='Binary')

    # Constraints to calculate the makespan
    for i in range(m):
        completion_time = 0
        for j in range(n):
            completion_time += Pij[i][j] * x[i, j]
        prob += completion_time <= makespan  # Constraint: makespan is the maximum completion time

    # Constraints: Each job must be processed by one and only one machine
    for j in range(n):
        prob += lpSum(x[i, j] for i in range(m)) == 1

    # Solve the integer programming problem
    prob.solve(PULP_CBC_CMD(msg=False))

    return value(makespan), x


if __name__ == "__main__":
    # Read the processing times from a CSV file
    P = read_csv_file("data2.csv")

    # Initialize the scheduling problem
    sch = SchedulingProblem(P)

    # Solve the scheduling problem to get the optimal makespan and decision variables
    makespan_, xij = integer_programming(P)

    # Update the decision variables and the makespan in the SchedulingProblem object
    sch.update_xij({(i, j): xij[i, j] for i in range(sch.m) for j in range(sch.n)})
    sch.makespan = makespan_

    # Display results
    print(f"Optimal Makespan: {makespan_}")
    sch.print_schedule()
