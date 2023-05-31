from CSV_functions import *
from LP import *
from IP import *
from Procedure import *


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
    lp_solution, deadline = binary_search_procedure(P)
    ###############################################################################################
    print('|-----', test, '----------------------------------------')
    # Our data
    print('Pij:', m, 'machines x', n, ' jobs')
    for row in data:
        print(*row)
    print()
    # Greedy Makespan
    print("Calculated Greedy makespan t->", t)
    print("Using Procedure calculate Deadline d->", deadline)
    print()

    if lp_solution is not None:
        # LP
        print_LP(P, lp_solution)

        # Rounded LP
        print()
        print_LP_rounded(P, lp_solution[1])

        # IP
        di = [deadline] * m
        ip_solution = IP(P, di, t)
        print_IP(P, ip_solution)
    else:
        print("No feasible solution found.")
    print('|--- End of ', test, '-----------------------------------------------------------|')


# Execute the main function
if __name__ == "__main__":
    run_test('data.csv')
