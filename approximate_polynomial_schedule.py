from pulp import *

# Set the PuLP logger to a higher level (WARNING) to suppress unnecessary output
pulp_logger = logging.getLogger("pulp")
pulp_logger.setLevel(logging.WARNING)


def approximate_schedule(pij, di):
    """
    Solve the scheduling problem for unrelated parallel machines using an LP relaxation and rounding.

    Args:
        pij (list of lists): Processing times of jobs on machines. pij[i][j] represents the processing time of job
        j on machine i.
        di (list): Deadlines for machines. di[i] represents the deadline for machine i.

    Returns: tuple: A tuple containing the rounded schedule as a 2D array and the calculated makespan. The rounded
    schedule is represented as a list of lists, where each element is either 0 or 1. A value of 1 indicates that the
    corresponding job is assigned to the machine, and 0 indicates that it is not assigned. The makespan is a single
    value representing the completion time of the schedule.
    """

    m = len(pij)  # Number of machines
    n = len(pij[0])  # Number of jobs

    # Step 1: Create the LP problem
    lp_problem = LpProblem("Scheduling_Problem", LpMinimize)

    # Step 2: Define the objective function In this step, we create a new continuous decision variable Cmax using
    # LpVariable from the PuLP library. This variable represents the makespan or the completion time of the schedule.
    # The LpVariable function takes three arguments:
    # "Cmax": This is the name of the variable. We use "Cmax" to represent the makespan. lowBound=0: This specifies
    # the lower bound of the variable. In this case, the makespan cannot be negative, so we set the lower bound to 0.
    # cat="Continuous": This specifies the category or type of the variable. In this case, we set it as continuous
    # since the makespan can take any real value. After creating the Cmax variable, we add it to the LP problem using
    # the += operator. By adding the makespan as the objective, we are indicating that we want to minimize its value
    # during optimization.
    # In summary, step 2 sets up the objective function of the LP problem, which is to minimize the makespan of the
    # schedule.
    Cmax = LpVariable("Cmax", lowBound=0, cat="Continuous")
    lp_problem += Cmax

    # Step 3: Add constraints Add the constraints for job assignment to machines
    # In this part, we define the decision variables jobs_assigned as binary variables using LpVariable.
    # These variables represent whether a job is assigned to a machine or not. A value of 1 indicates that the job is
    # assigned, and 0 indicates that it is not assigned.
    # The nested list comprehension creates a 2D list of decision variables. Each row corresponds to a machine,
    # and each column corresponds to a job. So jobs_assigned[i][j] represents whether job j is assigned to machine i.
    # The next loop adds a constraint for each job. The constraint lpSum(jobs_assigned[i][j] for i in range(m)) == 1
    # ensures that each job is assigned to exactly one machine. The lpSum function calculates the sum of the decision
    # variables jobs_assigned[i][j] for all machines i, and it should be equal to 1.
    jobs_assigned = [[LpVariable(f"x{i}{j}", cat="Binary") for j in range(n)] for i in range(m)]
    # Each job can be assigned to one machine
    for j in range(n):
        lp_problem += lpSum(jobs_assigned[i][j] for i in range(m)) == 1

    # Add the constraints for processing times on machines
    # These constraints ensure that the processing times on machines satisfy the given deadlines.
    # For each machine i, we calculate the sum of the processing times of the assigned jobs multiplied by their
    # respective decision variables using the expression lpSum(pij[i][j] * jobs_assigned[i][j] for j in range(n)).
    # This sum represents the total processing time on machine i. The constraint <= di[i] ensures that the total
    # processing time on machine i is less than or equal to its corresponding deadline di[i].
    # It guarantees that the machine completes its assigned jobs within the given deadline.
    # Meet the deadline
    for i in range(m):
        lp_problem += lpSum(pij[i][j] * jobs_assigned[i][j] for j in range(n)) <= di[i]

    # These constraints ensure that each machine processes only one job at a time. We iterate over all machines and
    # jobs and add a constraint jobs_assigned[i][j] <= 1 for each job on machine i. This constraint limits the value
    # of the decision variable jobs_assigned[i][j] to be at most 1, indicating that at most one job is assigned to
    # machine i at any given time.
    # Add the constraints to
    # ensure each machine processes only one job at a time
    for i in range(m):
        for j in range(n):
            lp_problem += jobs_assigned[i][j] <= 1
    # In summary, the constraints in step 3 enforce the proper assignment of jobs to machines, ensure that processing
    # times meet the deadlines, and restrict each machine to process only one job at a time.

    # Step 4: Solve the LP relaxation
    lp_problem.solve()

    # Step 5: Handle infeasible solution by iteratively increasing the deadlines
    while LpStatus[lp_problem.status] == "Infeasible":
        # Increase the deadlines for all machines by a certain factor (e.g., 10%)
        di = [d * 1.1 for d in di]

        # Clear the existing constraints
        lp_problem.constraints.clear()

        # Re-add the constraints with the updated deadlines
        for j in range(n):
            lp_problem += lpSum(jobs_assigned[i][j] for i in range(m)) == 1
        for i in range(m):
            lp_problem += lpSum(pij[i][j] * jobs_assigned[i][j] for j in range(n)) <= di[i]
        for i in range(m):
            for j in range(n):
                lp_problem += jobs_assigned[i][j] <= 1

        # Solve the LP relaxation again
        lp_problem.solve()

    # Step 6: Round the LP solution to obtain an integral schedule
    rounded_jobs_assigned = [[round(value(jobs_assigned[i][j])) for j in range(n)] for i in range(m)]

    # Step 7: Calculate the makespan of the rounded schedule
    completion_times = [sum(pij[i][j] * rounded_jobs_assigned[i][j] for j in range(n)) for i in range(m)]
    makespan = max(completion_times)

    # Step 8: Return the rounded schedule and makespan
    return rounded_jobs_assigned, makespan
