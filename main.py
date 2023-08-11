from Procedure import *
from SchedulingProblem import SchedulingProblem
from generate_data import read_csv_file


def run_main(filename):
    P = read_csv_file(filename)

    print('|-----', filename, '-------------------------------------------------------------------------------------|')
    # Initialize Scheduling Problem
    scheduling_prob = SchedulingProblem(P)
    scheduling_prob.print_info()
    # Greedy Schedule makespan t
    t = greedy_schedule(scheduling_prob.P)
    print("Calculated Greedy makespan: t = ", t)
    # Run Binary Search Procedure
    lp_solution, deadline = binary_search_procedure(scheduling_prob.P, t)  # lp_solution = makespan , xij : dict
    scheduling_prob.makespan = lp_solution[0]
    scheduling_prob.update_xij(lp_solution[1])
    print("Using Procedure the deadline with minimum makespan: d = ", deadline)
    print()

    if lp_solution is not None:

        # Solution Linear Programming
        print("\nSolution using the Procedure with Linear Programming LP(P,d⃗,t) and Bipartite Graph for rounding "
              "solution")
        rounded_lpSolution = round_lpSolution(lp_solution[1], scheduling_prob.m, scheduling_prob.n)
        scheduling_prob.update_xij(rounded_lpSolution)
        scheduling_prob.calculate_makespan()
        scheduling_prob.print_schedule()

        # Solution Integer Programming
        print("\nSolution using Integer Programming IP(P,d⃗,t)")
        di = [deadline] * scheduling_prob.m
        ip_solution = IP(P, di, t)
        print("IP Schedule")
        print_schedule(P, ip_solution)
    else:
        print("No feasible solution found during Binary Search Procedure")
    print('|--- End of ', filename, '-----------------------------------------------------------|')


# Choose which data to run
if __name__ == "__main__":
    run_main('data.csv')
