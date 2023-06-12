from pulp import *


def convert_decision_to_array(xij, m, n):
    """
    Converts the decision variables dictionary to a 2D array representation.

    Parameters:
    - xij: the decision variables representing the job assignments to machines.
    - m: the number of machines.
    - n: the number of jobs.

    Returns:
    - assignment_array: a 2D array with values indicating the job assignments to machines.
    """
    assignment_array = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            if (i, j) in xij:
                assignment_array[i][j] = xij[(i, j)].varValue
    return assignment_array


def round_decision(decision):
    rounded_xij = {}
    for key, xij_value in decision.items():
        if isinstance(xij_value, LpVariable):
            rounded_xij[key] = round(xij_value.varValue)
        else:
            rounded_xij[key] = round(xij_value)
    return rounded_xij


def print_decision_array(xij, m, n):
    """
    Prints the decision variable array representation.

    Parameters:
    - xij: the decision variables representing the job assignments to machines.
    - m: the number of machines.
    - n: the number of jobs.
    """
    x_array = convert_decision_to_array(xij, m, n)
    for row in x_array:
        print(row)


def print_schedule(xij, m, n):
    """
    Prints the schedule of job assignments to machines.

    Parameters:
    - xij: the decision variables representing the job assignments to machines.
    - m: the number of machines.
    - n: the number of jobs.
    """
    x = convert_decision_to_array(xij, m, n)
    max_job_width = len(f"Job{n - 1}")  # Determine the maximum width of job names
    for i in range(m):
        assigned_jobs = []
        for j in range(n):
            if round(x[i][j]) == 1:
                job_name = f"Job{j}"
                padded_job_name = job_name.ljust(max_job_width)
                assigned_jobs.append(padded_job_name)
        print(f"Machine {i}: [ {', '.join(assigned_jobs)} ]")


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

# #######################    Testing #################################################################################

def calculate_makespan(P, x_array):
    m = len(x_array)
    n = len(x_array)
    completion_times = [0] * m  # Initialize completion times for each machine

    # Calculate completion times for each machine
    for i in range(m):
        for j in range(n):
            completion_times[i] += x_array[i][j] * P[i][j]  # Add the processing time of the job if assigned to
            # the machine

    # Find the maximum completion time as the makespan
    makespan = max(completion_times)
    return makespan


def testLP():
    """
    Tests the LP.py module by solving a scheduling problem instance.
    """
    print('----------   Testing LP.py   --------------------')
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

    if result is not None:
        makespan, x = result
        print("Objective value (makespan):", makespan)
        print("Job assignments to machines:")
        print_schedule(x, m, n)
        print("Completion times:")
        print_decision_array(x, m, n)
    else:
        print("No feasible solution found.")

    # Calculate makespan using the LP solution
    if result is not None:
        _, x = result
        calculated_makespan = calculate_makespan(Pij, x)
        print("Calculated makespan:", calculated_makespan)
    else:
        print("Cannot calculate makespan as no feasible solution found.")

    print('----------   End of Testing LP.py   -------------')


# Run the test function
if __name__ == "__main__":
    testLP()
