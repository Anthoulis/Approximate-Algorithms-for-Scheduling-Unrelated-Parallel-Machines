import os

from CSV_functions import *
from Procedure import *


def print_job_assignments(P, x):
    m = len(P)
    n = len(P[0])

    # Create a dictionary to store the job assignments for each machine
    machine_assignments = {}

    # Iterate over the decision variables and store the job assignments
    for key, var in x.items():
        machine, job = key
        if var.varValue == 1:
            if machine in machine_assignments:
                machine_assignments[machine].append(f"Job{job}")
            else:
                machine_assignments[machine] = [f"Job{job}"]

    # Print the job assignments for each machine
    for machine, assignments in machine_assignments.items():
        print(f"Machine {machine}:", assignments)


def run_test(test):
    file_path = test
    # Check if the file already exists
    if os.path.isfile(file_path):
        # Read and save the data from the existing file
        data = read_csv_file(file_path)
    else:
        # Create a new CSV file
        data = [[2, 4, 3, 2], [3, 1, 6, 2], [1, 3, 2, 5]]
        write_csv_file(file_path, data)

    P = data
    m = len(data)  # number of machines
    n = len(data[0])  # number of jobs

    t = greedy_schedule(P)
    # Calculate the initial upper and lower bounds
    # upper_bound = t
    # lower_bound = t // m

    # Run the binary search procedure
    # best_solution = binary_search_loop(P, t, lower_bound, upper_bound)
    # best_solution = binary_search_recursion(P, t, lower_bound, upper_bound, None)

    solution = binary_search_procedure(P)

    ###############################################################################################
    print('|-----', test, '----------------------------------------')
    # Our data
    print('Pij:', m, 'machines x', n, ' jobs')
    for row in data:
        print(*row)

    # Greedy Makespan
    print("Greedy makespan ", t)

    if solution is not None:
        makespan, schedule = solution[0], solution[1]
        print("Best Solution:")
        print("Makespan:", makespan)
        print("Schedule:")
        print_x_decision(P, schedule)
    else:
        print("No feasible solution found.")
    print('|--- End of ', test, '-----------------------------------------------------------|')


# Execute the main function
if __name__ == "__main__":
    run_test('data.csv')
