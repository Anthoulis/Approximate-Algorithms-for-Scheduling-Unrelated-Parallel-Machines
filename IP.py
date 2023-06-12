from pulp import *


# TODO: Modify like LP
def IP(Pij, di, t):
    m = len(Pij)  # Number of machines
    n = len(Pij[0])  # Number of jobs

    # Define the variables, objective function, and problem
    ip_prob = LpProblem("IP", LpMinimize)

    # Decision variables
    x = LpVariable.dicts("x", [(i, j) for i in range(m) for j in range(n)], lowBound=0, upBound=1, cat='Binary')

    # The objective function is to minimize the makespan, which is the maximum completion time among
    # all the jobs on the machines.
    Cmax = LpVariable("Cmax", lowBound=0, cat="Integer")
    ip_prob += Cmax

    # Constraints

    # Each job can be assigned to one machine
    for j in range(n):
        Mj_t = []  # Contains machines that can process job j in no more than t time units
        for i in range(m):
            if Pij[i][j] <= t:
                Mj_t.append(i)
        ip_prob += lpSum(x[i, j] for i in Mj_t) == 1  # Constraint: Each job can be assigned to one machine

    # Meet the deadline
    for i in range(m):
        Ji_t = []  # Contains jobs that require no more than t time units on machine i.
        for j in range(n):
            if Pij[i][j] <= t:
                Ji_t.append(j)
        ip_prob += lpSum(Pij[i][j] * x[i, j] for j in Ji_t) <= di[i]  # Constraint: Meet the machine deadline

    # Calculate the makespan
    for i in range(m):
        completion_time = 0
        for j in range(n):
            completion_time += Pij[i][j] * x[i, j]
        ip_prob += completion_time <= Cmax  # Constraint: Cmax is the maximum completion time among all the jobs

    # Solve the problem
    ip_prob.solve(PULP_CBC_CMD(msg=0))

    # If the problem is not feasible, return None
    if ip_prob.status != 1:
        return None

    makespan = value(Cmax)
    return makespan, x


def print_IP(Pij, ip_solution):
    print('-- IP --')
    print('Makespan:', ip_solution[0])

    m = len(Pij)  # Number of machines
    n = len(Pij[0])  # Number of jobs

    max_job_width = len(f"Job{n - 1}")  # Determine the maximum width of job names

    completion_times = [0] * m  # Initialize completion times for each machine
    x = ip_solution[1]
    for i in range(m):
        assigned_jobs = []
        for j in range(n):
            if round(x[i, j].varValue) == 1:  # Round the value and check if it is equal to 1
                job_name = f"Job{j}"
                padded_job_name = job_name.ljust(max_job_width)  # Pad the job name with spaces
                assigned_jobs.append(padded_job_name)
                completion_times[i] += Pij[i][j]  # Accumulate the processing time for assigned jobs
        print(f"Machine {i}: [ {', '.join(assigned_jobs)} ]")
