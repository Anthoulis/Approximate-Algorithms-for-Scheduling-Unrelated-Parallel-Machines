from pulp import *


def LP(Pij: list[list[int]], di: list[int], t: int) -> (int, dict[tuple[int, int]]):
    """
    LP(Pij, d⃗,t)
    Solves the scheduling problem using linear programming. We drop integrity constrains.
    :param Pij: A 2D array representing the processing times of jobs on machines.
    :param di: A list of machine deadlines.
    :param t: The maximum time units allowed for Ji(t) and Mj(t) sets.
    :return: The minimum makespan achieved, dictionary of the decision variables representing the job assignments
             to machines (i,j): LpVariable
    """
    m = len(Pij)  # Number of machines
    n = len(Pij[0])  # Number of jobs

    # Define the variables, objective function, and problem
    lp_prob = LpProblem("LP", LpMinimize)

    # Create xij decision variables
    # xij>=0  for j ∈ Ji(t),  i=1,...,m
    x = LpVariable.dicts("x", [(i, j) for i in range(m) for j in range(n) if Pij[i][j] <= t], lowBound=0, upBound=1,
                         cat='Continuous')

    # The objective function is to minimize the makespan, which is the maximum completion time among
    # all the jobs on the machines.
    Cmax = LpVariable("Cmax", lowBound=0, cat="Continuous")
    lp_prob += Cmax

    # Constraints-------------------------------------------------

    # i ∈ Mj(t) Sum(xij) = 1    for j=1,...,n
    # Mj(t) is the set of machines that can process job j in no more than t time units.
    for j in range(n):
        lp_prob += lpSum(x[i, j] for i in range(m) if Pij[i][j] <= t) == 1  # Constraint: Each job must be processed
        # exactly once

    # j ∈ Ji(t) Sum(pij*xij) <= di  for i=1,...,n
    # Ji(t) is the set of jobs that require no more than t time units on machine i.
    # Meet the deadline
    for i in range(m):
        lp_prob += lpSum(Pij[i][j] * x[i, j] for j in range(n) if Pij[i][j] <= t) <= di[i]  # Constraint: Meet the
        # machine deadline

    # Calculate the makespan
    for i in range(m):
        completion_time = 0
        for j in range(n):
            if Pij[i][j] <= t:
                completion_time += Pij[i][j] * x[i, j]
        lp_prob += completion_time <= Cmax  # Constraint: Cmax is the maximum completion time among all the jobs

    # Solve the problem
    lp_prob.solve(PULP_CBC_CMD(msg=False))

    # If the problem is not feasible, return None
    if lp_prob.status != 1:
        return None

    makespan = value(Cmax)
    return makespan, x


def IP(Pij: list[list[int]], di: list[int], t: int) -> (int, dict[tuple[int, int]]):
    """
        IP(Pij, d⃗,t)
        Solves the scheduling problem using integer programming.
        We keep integrity constrained.
        :param Pij: A 2D array representing the processing times of jobs on machines.
        :param di: A list of machine deadlines.
        :param t: The maximum time units allowed for Ji(t) and Mj(t) sets.
        :return: The minimum makespan achieved, dictionary of the decision variables representing the job assignments
                 to machines (i,j): LpVariable
        """
    m = len(Pij)  # Number of machines
    n = len(Pij[0])  # Number of jobs

    # Define the variables, objective function, and problem
    ip_prob = LpProblem("IP", LpMinimize)

    #   Create xij decision variables
    #   xij ∈ {0,1}  for j ∈ Ji(t),  i=1,...,m
    #   With xij ∈ {0,1} that means that each job can be executed in only one machine
    x = LpVariable.dicts("x", [(i, j) for i in range(m) for j in range(n) if Pij[i][j] <= t], lowBound=0, upBound=1,
                         cat='Binary')

    # The objective function is to minimize the makespan, which is the maximum completion time among
    # all the jobs on the machines.
    Cmax = LpVariable("Cmax", lowBound=0, cat="Integer")
    ip_prob += Cmax

    # Constraints-------------------------------------------------

    # i ∈ Mj(t) Sum(xij) = 1 for j=1,...,n
    # Mj(t) is the set of machines that can process job j in no more than t time units.
    for j in range(n):
        ip_prob += lpSum(x[i, j] for i in range(m) if Pij[i][j] <= t) == 1  # Constraint: Each job must be processed
        # exactly once

    # j ∈ Ji(t) Sum(pij*xij) <= di + t for i=1,...,n
    # Ji(t) is the set of jobs that require no more than t time units on machine i.
    # Meet the deadline
    for i in range(m):
        ip_prob += lpSum(Pij[i][j] * x[i, j] for j in range(n) if Pij[i][j] <= t) <= di[i] + t  # Constraint: Meet the
        # machine deadline

    # Calculate the makespan
    for i in range(m):
        completion_time = 0
        for j in range(n):
            if Pij[i][j] <= t:
                completion_time += Pij[i][j] * x[i, j]
        ip_prob += completion_time <= Cmax  # Constraint: Cmax is the maximum completion time among all the jobs

    # Solve the problem
    ip_prob.solve(PULP_CBC_CMD(msg=False))

    # If the problem is not feasible, return None
    if ip_prob.status != 1:
        return None

    makespan = value(Cmax)
    return makespan, x


# Helpful functions for converting data types of the solutions and printing methods------------------------------------
def calculate_makespan(P, xij: dict[tuple[int, int], LpVariable]):
    """
    :param P: a 2D array representing the processing times of jobs on machines.
    :param xij: dictionary of the decision variables representing the job assignments to machines.
    :return:
    """
    m = len(P)
    n = len(P[0])
    completion_times = [0] * m  # Initialize completion times for each machine
    # Calculate completion times for each machine
    for i in range(m):
        for j in range(n):
            if (i, j) in xij and xij[(i, j)].varValue == 1:  # Check if the job is assigned to the machine
                completion_times[i] += P[i][j]  # Add the processing time of the job

    # Find the maximum completion time as the makespan
    makespan = max(completion_times)
    return makespan


def convert_decision_to_array(xij: dict[tuple[int, int], LpVariable], m, n):
    """
    Convert xij to an array.
    :param xij: Dictionary of the decision variables representing the job assignments to machines.
    :param m: The number of machines.
    :param n: The number of jobs.
    :return: A 2D array with values indicating the job assignments to machines.
    """
    assignment_array = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            if (i, j) in xij:
                assignment_array[i][j] = xij[(i, j)].varValue
    return assignment_array


def print_decision_array(xij: dict[tuple[int, int], LpVariable], m, n):
    """
    :param xij: dictionary of the decision variables representing the job assignments to machines.
    :param m: the number of machines.
    :param n: the number of jobs.
    :return:
    """
    x_array = convert_decision_to_array(xij, m, n)
    for row in x_array:
        print(row)


def print_schedule(Pij, solution: (int, dict[tuple[int, int]])) -> None:
    """Prints the scheduling results."""
    m = len(Pij)  # Number of machines
    n = len(Pij[0])  # Number of jobs
    makespan = solution[0]
    xij = solution[1]
    print(f"Makespan = {makespan}")
    max_job_width = len(f"Job{n - 1}")  # Determine max width for job names

    for i in range(m):
        # List jobs assigned to each machine
        assigned_jobs = [f"Job{j}".ljust(max_job_width) for j in range(n) if (i, j) in xij if xij[(i, j)].varValue == 1]
        print(f"Machine {i}: [ {', '.join(assigned_jobs)} ]")
