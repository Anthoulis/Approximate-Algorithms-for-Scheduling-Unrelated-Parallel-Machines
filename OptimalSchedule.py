from pulp import *


def optimal_schedule(Pij: []):
    """
    Solves the minimum makespan scheduling problem using Integer Programming (IP).
    It finds the optimal solution by searching the entire solution space.
    It will require a lot of computational time for large-scale problems.
    """
    m, n = len(Pij), len(Pij[0])  # Number of machines and jobs
    # Initialize the integer programming problem (objective is to minimize this)
    prob = LpProblem("Minimum_Makespan_Scheduling", LpMinimize)
    # Create a variable for the makespan
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
