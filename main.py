from BestSchedule import optimal_schedule
from Procedure import *
from SchedulingProblem import SchedulingProblem
from generate_data import read_csv_file
import time


# Using IP(Pij,d⃗,t) with deadline d from Procedure to compare results with Graph rounding
def run_ip_solution(P: list[list[int]], d: int):
    start_time = time.time()
    m = len(P)
    print("\nFrom the Rounding Theorem we use IP(Pij,d⃗,t) with deadline d from Procedure")
    print("We use this result for reference to our rounding.")
    print("*Note. This isn't the best possible makespan")
    di = [d] * m
    t = d
    ip_solution = IP(P, di, t)
    print("IP Schedule")
    print("IP Makespan = ", ip_solution[0])
    #print_schedule(P, ip_solution)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Time taken to solve IP(Pij,d⃗,t) with deadline d from Procedure: {elapsed_time:.4f} seconds")


# Find the best schedule exploring every possible solution
# It takes time to complete
def run_optimal_solution(P: list[list[int]]):
    start_time = time.time()
    # Initialize the scheduling problem
    sch = SchedulingProblem(P)
    # Solve the scheduling problem to get the optimal makespan and decision variables
    makespan_, xij = optimal_schedule(P)
    # Update the decision variables and the makespan in the SchedulingProblem object
    sch.update_xij(xij)
    sch.makespan = makespan_

    # Display results
    print("\nExploring all possible solution we find the best schedule")
    print(f"Optimal Makespan: {makespan_}")
    #sch.print_schedule()
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Time taken to find the best solution: {elapsed_time:.4f} seconds")


def run_main(filename):
    P = read_csv_file(filename)
    print('|-----', filename, '-------------------------------------------------------------------------------------|')

    # Initialize Scheduling Problem
    scheduling_prob = SchedulingProblem(P)
    scheduling_prob.print_info()

    start_time = time.time()  # Record the start time
    # Greedy Schedule makespan t
    t = greedy_schedule(scheduling_prob.P)
    print("Calculated Greedy makespan: t = ", t)

    # Run Binary Search Procedure
    lp_solution, deadline = binary_search_procedure(scheduling_prob.P, t)  # lp_solution = makespan , xij : dict

    if lp_solution is not None:

        scheduling_prob.makespan = lp_solution[0]
        scheduling_prob.update_xij(lp_solution[1])
        print("Using Procedure the deadline with minimum makespan: d = ", deadline)
        print("The Linear Programming LP(Pij,d⃗,t) with the deadline d creates a non-integer schedule with makespan = ",
              scheduling_prob.makespan)

        # Round Solution using Bipartite Graph
        print("\nIn order to round this solution we create a Bipartite Graph G")
        rounded_lpSolution = round_lpSolution(lp_solution[1], scheduling_prob.m, scheduling_prob.n)
        scheduling_prob.update_xij(rounded_lpSolution)
        scheduling_prob.calculate_makespan()
        print("This the final result. An approximate solution using Linear Programming, Decision Procedure and "
              "Bipartite Graph")
        #scheduling_prob.print_schedule()
        print("Makespan = ", scheduling_prob.makespan)
    else:
        print("No feasible solution found during Binary Search Procedure")
        return
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Time taken to find approximate solution: {elapsed_time:.4f} seconds")

    # Using IP(Pij,d⃗,t) with deadline d from Procedure to compare results with Graph rounding
    run_ip_solution(scheduling_prob.P, deadline)

    # Find the best schedule exploring every possible solution
    run_optimal_solution(scheduling_prob.P)
    print('|--- End of ', filename, '-----------------------------------------------------------|')


# Choose which data to run
if __name__ == "__main__":
    run_main('data30x100.csv')
