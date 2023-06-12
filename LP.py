from pulp import *


# TODO: Create def where given a decision x[i,j] returns a m x n 2D array.
def create_assignment_array(x, m, n):
    assignment_array = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            if (i, j) in x:
                assignment_array[i][j] = x[(i, j)].varValue
    return assignment_array


def LP(Pij, di, t):
    """
    Solves the scheduling problem using linear programming.

    Parameters:
    - Pij: a 2D array representing the processing times of jobs on machines.
    - di: a list of machine deadlines.
    - t: the maximum time units allowed for Ji(t) and Mj(t) sets.

    Returns:
    - objective_value: the minimum makespan achieved.
    - x: the decision variables representing the job assignments to machines.
    """

    m = len(Pij)  # Number of machines
    n = len(Pij[0])  # Number of jobs

    # Define the variables, objective function, and problem
    lp_prob = LpProblem("LP", LpMinimize)

    # TODO: Create xij decision variables only for Mj(t)
    #  Where Mj(t) is the set of machines that can process job j in no more than t time units.
    x = LpVariable.dicts("x", [(i, j) for i in range(m) for j in range(n)], lowBound=0, upBound=1, cat='Continuous')

    # The objective function is to minimize the makespan, which is the maximum completion time among
    # all the jobs on the machines.
    Cmax = LpVariable("Cmax", lowBound=0, cat="Continuous")
    lp_prob += Cmax

    # Constraints

    # Each job can be assigned to one machine
    for j in range(n):
        Mj_t = []  # Contains machines that can process job j in no more than t time units
        for i in range(m):
            if Pij[i][j] <= t:
                Mj_t.append(i)
        lp_prob += lpSum(x[i, j] for i in Mj_t) == 1  # Constraint: Each job can be assigned to one machine

    # Meet the deadline
    for i in range(m):
        Ji_t = []  # Contains jobs that require no more than t time units on machine i.
        for j in range(n):
            if Pij[i][j] <= t:
                Ji_t.append(j)
        lp_prob += lpSum(Pij[i][j] * x[i, j] for j in Ji_t) <= di[i]  # Constraint: Meet the machine deadline

    # Calculate the makespan
    for i in range(m):
        completion_time = 0
        for j in range(n):
            completion_time += Pij[i][j] * x[i, j]
        lp_prob += completion_time <= Cmax  # Constraint: Cmax is the maximum completion time among all the jobs

    # Solve the problem
    lp_prob.solve(PULP_CBC_CMD(msg=0))

    # If the problem is not feasible, return None
    if lp_prob.status != 1:
        return None

    makespan = value(Cmax)
    return makespan, x


# #####  ---  End of LP  ---   ########################################################################################

# Print x[i,j]
def print_x_decision(P, x):
    m = len(P)
    n = len(P[0])
    for i in range(m):
        row = []
        for j in range(n):
            row.append(x[i, j].varValue)
        print("Machine", i, ":", row)


def print_LP(Pij, solution):
    print('-- LP --')
    print('Makespan ', solution[0])
    print('LP decisions xij')
    print_x_decision(Pij, solution[1])


def print_LP_rounded(Pij, x):
    print("-- LP Rounded --")
    m = len(Pij)  # Number of machines
    n = len(Pij[0])  # Number of jobs

    max_job_width = len(f"Job{n - 1}")  # Determine the maximum width of job names

    completion_times = [0] * m  # Initialize completion times for each machine

    for i in range(m):
        assigned_jobs = []
        for j in range(n):
            if round(x[i, j].varValue) == 1:  # Round the value and check if it is equal to 1
                job_name = f"Job{j}"
                padded_job_name = job_name.ljust(max_job_width)  # Pad the job name with spaces
                assigned_jobs.append(padded_job_name)
                completion_times[i] += Pij[i][j]  # Accumulate the processing time for assigned jobs
        print(f"Machine {i}: [{', '.join(assigned_jobs)}]")

    makespan = max(completion_times)  # Calculate the new makespan

    print(f"\nLP Rounded Makespan: {makespan}")
    print()


# #######################    Testing #################################################################################
def calculate_makespan(P, x):
    machines = len(P)
    jobs = len(P[0])
    completion_times = [0] * machines  # Initialize completion times for each machine

    # Calculate completion times for each machine
    for i in range(machines):
        for j in range(jobs):
            completion_times[i] += x[i, j].varValue * P[i][j]  # Add the processing time of the job if assigned to
            # the machine

    # Find the maximum completion time as the makespan
    makespan = max(completion_times)
    return makespan


def testLP():
    print('Testing LP.py')
    # Example input data
    Pij = [
        [3, 4, 2, 5, 2, 3, 4, 5, 3, 2, 4, 3, 2, 4, 3, 5, 4, 2, 3, 2, 4, 3, 5, 4, 2, 3, 2, 4, 3, 4],
        [2, 5, 1, 3, 2, 4, 3, 5, 1, 2, 3, 4, 2, 1, 5, 4, 3, 2, 4, 3, 1, 2, 3, 4, 2, 5, 1, 3, 2, 4],
        [4, 3, 2, 1, 5, 4, 2, 3, 1, 2, 3, 4, 2, 1, 5, 4, 3, 2, 4, 3, 1, 2, 3, 4, 2, 5, 1, 3, 2, 4],
        [1, 5, 4, 2, 3, 2, 4, 3, 5, 4, 2, 3, 2, 4, 3, 5, 4, 2, 3, 2, 4, 3, 5, 4, 2, 3, 2, 4, 3, 5],
        [2, 3, 1, 5, 4, 2, 3, 1, 2, 3, 4, 2, 1, 5, 4, 3, 2, 4, 3, 1, 2, 3, 4, 2, 5, 1, 3, 2, 4, 3],
        [3, 4, 2, 5, 2, 3, 4, 5, 3, 2, 4, 3, 2, 4, 3, 5, 4, 2, 3, 2, 4, 3, 5, 4, 2, 3, 2, 4, 3, 5],
        [4, 3, 2, 1, 5, 4, 2, 3, 1, 2, 3, 4, 2, 1, 5, 4, 3, 2, 4, 3, 1, 2, 3, 4, 2, 5, 1, 3, 2, 4],
        [1, 5, 4, 2, 3, 2, 4, 3, 5, 4, 2, 3, 2, 4, 3, 5, 4, 2, 3, 2, 4, 3, 5, 4, 2, 3, 2, 4, 3, 5],
        [2, 3, 1, 5, 4, 2, 3, 1, 2, 3, 4, 2, 1, 5, 4, 3, 2, 4, 3, 1, 2, 3, 4, 2, 5, 1, 3, 2, 4, 3],
        [3, 4, 2, 5, 2, 3, 4, 5, 3, 2, 4, 3, 2, 4, 3, 5, 4, 2, 3, 2, 4, 3, 5, 4, 2, 3, 2, 4, 3, 5]
    ]
    di = [15, 10, 12, 13, 11, 14, 9, 16, 10, 12]
    t = 10
    m = len(Pij)
    n = len(Pij[0])
    # Call LP function to solve the scheduling problem
    result = LP(Pij, di, t)

    if result is None:
        print("No feasible solution found.")
    else:
        makespan, x = result
        print("LP Makespan:", makespan)
        print('Calculate Makespan for verification , calculate makespan = ', calculate_makespan(Pij, x))
        print("Job Assignments:")
        print_x_decision(Pij, x)
        print()
        print()
        xarray = create_assignment_array(x, m, n)
        for row in xarray:
            print(row)


if __name__ == "__main__":
    testLP()
