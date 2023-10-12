from generate_data import read_csv_file
from SearchProcedure import *
from OptimalSchedule import optimal_schedule
import time


def run_ip_solution(sch_problem):
    """
    We use IP(Pij, d⃗,t) (from the Rounding Theorem) with the deadline d we got from Binary Search Procedure.
    We use this result for reference to the rounding of the LP solution we achieved using Bipartite Graphs.
    """
    start_time = time.time()
    sch_problem.makespan, sch_problem.xij = IP(sch_problem.P, [sch_problem.d] * sch_problem.m, sch_problem.t)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print("\nWe use IP(Pij, d⃗,t) (from the Rounding Theorem) with the deadline d we got from Binary Search Procedure.")
    print("We use this result for reference to the rounding of the LP solution we achieved using Bipartite Graphs.")
    print("IP Makespan = ", sch_problem.makespan)
    print(f"Time taken to solve IP(Pij,d⃗,t) with deadline d from Procedure: {elapsed_time:.4f} seconds")
    # sch_problem.print_schedule()


def run_optimal_solution(sch_problem):
    """
    Find the best schedule exploring every possible solution.
    It takes time to complete for large data.
    """
    start_time = time.time()
    sch_problem.makespan, sch_problem.xij = optimal_schedule(sch_problem.P)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print("\nExploring all possible solution we find the best schedule", "Optimal Makespan = ", sch_problem.makespan)
    print(f"Time taken to find the best solution: {elapsed_time:.4f} seconds")
    # sch_problem.print_schedule()


def run_main(filename):
    P = read_csv_file(filename)
    print('|-----', filename, '-------------------------------------------------------------------------------------|')
    start_time = time.time()
    # Run Binary Search Procedure
    sch_problem = binary_search_procedure(P)
    end_time = time.time()
    elapsed_time = end_time - start_time
    if sch_problem is not None:
        sch_problem.print_info()
        sch_problem.print_schedule()
        print("\nGraph G"), print_graph_info(sch_problem.bipartite_graphG)
        print("\nGraph G'"), print_graph_info(sch_problem.bipartite_graphG2)
        sch_problem.visualize_graphG()
        sch_problem.visualize_graphG2()
        visualize_graph_components(sch_problem.bipartite_graphG2)
    else:
        print("No feasible solution found during Binary Search Procedure")
        return
    print(f"Time taken to find approximate solution: {elapsed_time:.4f} seconds")

    # Using IP(Pij,d⃗,t) to compare results
    run_ip_solution(sch_problem)

    # Find Optimal Schedule to compare results
    run_optimal_solution(sch_problem)
    print('|--- End of ', filename, '-----------------------------------------------------------|')


# Choose which data to run
if __name__ == "__main__":
    run_main('30x100.csv')
