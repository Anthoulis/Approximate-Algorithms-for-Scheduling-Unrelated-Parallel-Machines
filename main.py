from IP import *
from Procedure import *
from generate_data import read_csv_file


def run_main(filename_data):
    file_path = filename_data
    # Check if the file already exists
    if os.path.isfile(file_path):
        # Read and save the data from the existing file
        data = read_csv_file(file_path)
    else:
        print("Data file not found")
        return

    P = data
    m = len(data)  # number of machines
    n = len(data[0])  # number of jobs
    t = greedy_schedule(P)
    lp_solution, deadline = binary_search_procedure(P)  # lp_solution = makespan , xij
    ###############################################################################################
    print('|-----', filename_data, '----------------------------------------')
    # Our data
    print('Pij:', m, 'machines x', n, ' jobs')
    # Greedy Makespan
    print("Calculated Greedy makespan: t = ", t)
    print("Using Procedure best calculated Deadline: d = ", deadline)
    print()

    if lp_solution is not None:

        # Solution
        print("Solution ")
        # TODO: round lp_solution
        lp_solution_rounded = round_lp_solution(lp_solution)
        print_schedule(P, lp_solution_rounded[1])

        # IP
        print("IP Solution")
        di = [deadline] * m
        ip_solution = IP(P, di, t)
        # print_decision_array(ip_solution[1], m, n)
        print("IP Schedule")
        print_schedule(P, ip_solution[1])
    else:
        print("No feasible solution found.")
    print('|--- End of ', filename_data, '-----------------------------------------------------------|')


# Execute the main function
if __name__ == "__main__":
    run_main('data.csv')
