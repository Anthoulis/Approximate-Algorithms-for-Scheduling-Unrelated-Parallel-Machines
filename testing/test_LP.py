# #######################    Testing #################################################################################
from linear_programming import *


def testLP():
    """
    Tests the linear_programming.py module by solving a scheduling problem instance.
    """
    print('----------   Testing linear_programming.py   --------------------')
    # Example input data
    Pij = [
        [3, 4, 2, 5, 2, 3, 4, 5, 3, 2, 4, 3, 2, 4, 3, 5, 4, 2, 3, 2, 4, 3, 5, 4, 2, 3, 2, 4, 3, 4],
        [2, 5, 1, 3, 2, 4, 3, 5, 1, 2, 3, 4, 2, 1, 5, 4, 3, 2, 4, 3, 1, 2, 3, 4, 2, 5, 1, 3, 2, 4],
        [4, 3, 2, 1, 5, 4, 2, 3, 1, 2, 3, 4, 2, 1, 5, 4, 3, 2, 4, 3, 1, 2, 3, 4, 2, 5, 1, 3, 2, 4],
        [1, 5, 4, 2, 3, 2, 4, 3, 5, 4, 2, 3, 2, 4, 3, 5, 4, 2, 3, 2, 4, 3, 5, 4, 2, 3, 2, 4, 3, 5],
        [2, 3, 1, 5, 4, 2, 3, 1, 2, 3, 4, 2, 1, 5, 4, 3, 2, 4, 3, 1, 2, 3, 4, 2, 5, 1, 3, 2, 4, 3],
        [3, 4, 2, 5, 2, 3, 4, 5, 3, 2, 4, 3, 2, 4, 3, 5, 4, 2, 3, 2, 4, 3, 5, 4, 2, 3, 2, 4, 3, 5],
        [4, 3, 2, 1, 5, 4, 2, 3, 1, 2, 3, 4, 2, 1, 5, 4, 3, 2, 4, 3, 1, 2, 3, 4, 2, 5, 1, 3, 2, 4],
        [1, 5, 4, 2, 3, 2, 4, 3, 5, 4, 2, 3, 2, 4, 3, 5, 4, 2, 3, 2, 4, 3, 5, 4, 2, 3, 2, 4, 3, 5],
        [2, 3, 1, 5, 4, 2, 3, 1, 2, 3, 4, 2, 1, 5, 4, 3, 2, 4, 3, 1, 2, 3, 4, 2, 5, 1, 3, 2, 4, 3],
        [3, 4, 2, 5, 2, 3, 4, 5, 3, 2, 4, 3, 2, 4, 3, 5, 4, 2, 3, 2, 4, 3, 5, 4, 2, 3, 2, 4, 3, 5]
    ]
    di = [15, 10, 12, 13, 11, 14, 9, 16, 10, 12]
    t = 10
    m = len(Pij)
    n = len(Pij[0])
    # Call LP function to solve the scheduling problem
    result = LP(Pij, di, t)

    if result is not None:
        makespan, xij = result
        print("Objective value (makespan):", makespan)
        print("Job assignments to machines:")
        print_schedule(Pij, xij)
        print("Completion times:")
        print_decision_array(xij, m, n)
    else:
        print("No feasible solution found.")

    # Calculate makespan using the LP solution
    if result is not None:
        _, xij = result
        calculated_makespan = calculate_makespan(Pij, xij)
        print("Calculated makespan:", calculated_makespan)
    else:
        print("Cannot calculate makespan as no feasible solution found.")

    print('----------   End of Testing linear_programming.py   -------------')


# Run the test function
if __name__ == "__main__":
    testLP()
