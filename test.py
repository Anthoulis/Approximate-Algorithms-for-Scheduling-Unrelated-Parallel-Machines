from CSV_functions import *
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
        data = [
            [3, 4, 2, 5, 2, 3, 4, 5, 3, 2, 4, 3, 2, 4, 3, 5, 4, 2, 3, 2, 4, 3, 5, 4, 2, 3, 2, 4, 3, 4],
            [2, 5, 1, 3, 2, 4, 3, 5, 1, 2, 3, 4, 2, 1, 5, 4, 3, 2, 4, 3, 1, 2, 3, 4, 2, 5, 1, 3, 2, 4],
            [4, 3, 2, 1, 5, 4, 2, 3, 1, 2, 3, 4, 2, 1, 5, 4, 3, 2, 4, 3, 1, 2, 3, 4, 2, 5, 1, 3, 2, 4],
            [1, 5, 4, 2, 3, 2, 4, 3, 5, 4, 2, 3, 2, 4, 3, 5, 4, 2, 3, 2, 4, 3, 5, 4, 2, 3, 2, 4, 3, 5],
            [2, 3, 1, 5, 4, 2, 3, 1, 2, 3, 4, 2, 1, 5, 4, 3, 2, 4, 3, 1, 2, 3, 4, 2, 5, 1, 3, 2, 4, 3],
            [3, 4, 2, 5, 2, 3, 4, 5, 3, 2, 4, 3, 2, 4, 3, 5, 4, 2, 3, 2, 4, 3, 5, 4, 2, 3, 2, 4, 3, 5],
            [4, 3, 2, 1, 5, 4, 2, 3, 1, 2, 3, 4, 2, 1, 5, 4, 3, 2, 4, 3, 1, 2, 3, 4, 2, 5, 1, 3, 2, 4],
            [1, 5, 4, 2, 3, 2, 4, 3, 5, 4, 2, 3, 2, 4, 3, 5, 4, 2, 3, 2, 4, 3, 5, 4, 2, 3, 2, 4, 3, 5],
            [2, 3, 1, 5, 4, 2, 3, 1, 2, 3, 4, 2, 1, 5, 4, 3, 2, 4, 3, 1, 2, 3, 4, 2, 5, 1, 3, 2, 4, 3],
            [3, 4, 2, 5, 2, 3, 4, 5, 3, 2, 4, 3, 2, 4, 3, 5, 4, 2, 3, 2, 4, 3, 5, 4, 2, 3, 2, 4, 3, 5]]
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
    print("Calculated Greedy makespan: t = ", t)
    print("Using Procedure best calculated Deadline: d = ", deadline)
    print()

    if lp_solution is not None:
        # LP
        print("LP decision array")
        print("Makespan = ", lp_solution[0])
        print_decision_array(lp_solution[1], m, n)
        print()

        # LP ROUNDED
        print("LP Rounded ")
        # Makespan
        x_round = convert_decision_to_array(lp_solution[1], m, n)
        for i in range(m):
            for j in range(n):
                x_round[i][j] = round(x_round[i][j])
        x_round_makespan = calculate_makespan(P, x_round)
        print("Makespan = ", x_round_makespan)
        print("LP Rounded Schedule")
        print_schedule(lp_solution[1], m, n)
        print()

        # IP
        # print("IP Solution")
        di = [deadline] * m
        ip_solution = IP(P, di, t)
        print("IP Decision array")
        print("Makespan = ", ip_solution[0])
        print_decision_array(ip_solution[1], m, n)
        print("IP Schedule")
        print_schedule(ip_solution[1], m, n)
    else:
        print("No feasible solution found.")
    print('|--- End of ', test, '-----------------------------------------------------------|')


# Execute the main function
if __name__ == "__main__":
    run_test('data.csv')
