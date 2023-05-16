import itertools


def brute_force_scheduling(processing_times):
    """
    Solve the scheduling problem using brute-force enumeration to find the best solution.

    Args:
        processing_times (list): 2D array with processing time of each job on each machine.
                                 Rows represent machines, and columns represent jobs.

    Returns:
        list: The best schedule as a 2D array, where each row represents a machine and contains the scheduled jobs.
        int: The makespan of the best schedule.
    """
    num_machines = len(processing_times)
    num_jobs = len(processing_times[0])
    best_schedule = None
    best_makespan = float('inf')

    # Generate all possible permutations of job scheduling
    job_permutations = itertools.permutations(range(num_jobs))

    # Iterate through each permutation
    for permutation in job_permutations:
        schedule = [[0] * num_jobs for _ in range(num_machines)]
        machine_times = [0] * num_machines

        # Assign jobs to machines based on the current permutation
        for job_index, job in enumerate(permutation):
            # Find the machine with the minimum accumulated processing time
            min_machine_time = float('inf')
            min_machine_index = None
            for machine_index in range(num_machines):
                if machine_times[machine_index] + processing_times[machine_index][job] < min_machine_time:
                    min_machine_time = machine_times[machine_index] + processing_times[machine_index][job]
                    min_machine_index = machine_index

            # Assign the job to the selected machine
            schedule[min_machine_index][job_index] = 1
            machine_times[min_machine_index] += processing_times[min_machine_index][job]

        # Calculate the makespan for the current schedule
        makespan = max(machine_times)

        # Update the best schedule if the current makespan is smaller
        if makespan < best_makespan:
            best_schedule = schedule
            best_makespan = makespan

    return best_schedule, best_makespan
