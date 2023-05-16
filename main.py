import os

from approximate_polynomial_schedule import approximate_schedule
from brute_force import brute_force_scheduling
from csv_functions import *


def print_schedule(schedule):
    """
    Print the schedule in a clear format.
    Args: schedule (list): The schedule as a 2D array, where each row represents a machine and contains the scheduled
    jobs.
    """
    num_machines = len(schedule)
    num_jobs = len(schedule[0])
    print("Schedule:")
    for i in range(num_machines):
        machine_jobs = [str(j) for j in range(num_jobs) if schedule[i][j] == 1]
        job_sequence = ', '.join(machine_jobs)
        print(f"Machine {i}: Jobs [{job_sequence}]")


def run_test(test):
    file_path = test
    # Check if the file already exists
    if os.path.isfile(file_path):
        # Read and save the data from the existing file
        data = read_csv_file(file_path)
    else:
        # Create a new CSV file
        data = [
            [10, 20, 15, 40, 8],
            [20, 30, 10, 25, 18]
        ]
        write_csv_file(file_path, data)
    di = set_initial_deadlines(data, 1.5)
    print("|--------Running " + test + " -----------------------|")
    print_csv_file_data(data)

    # Solve the scheduling problem using brute-force enumeration
    best_schedule, best_makespan = brute_force_scheduling(data)

    # Brute Force -------------------------------------
    print("---Brute Force---:")
    print_schedule(best_schedule)  # Assuming you have the print_schedule function defined
    print("Makespan:", best_makespan)

    # Approximate Polynomial --------------------------------------
    schedule, makespan = approximate_schedule(data, di)
    print("---Approximate---")
    print_schedule(schedule)
    print("Makespan:", makespan)

    print("--------End of " + test + " -----------------------")
    print()


# Execute the main function
if __name__ == "__main__":
    run_test('data.csv')
    run_test('test1.csv')
