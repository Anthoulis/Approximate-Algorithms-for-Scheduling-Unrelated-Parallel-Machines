from BipartiteGraph import visualize_graph
from RoundingTheorem import print_schedule, LP


class SchedulingProblem:
    """
    A simple class for organizing our data, for printing and visualization
    """
    def __init__(self, P: list[list[int]], lp_solution: (float, dict[tuple[int, int]]), deadline,
                 rounded_solution: (int, dict[tuple[int, int]]),
                 graphG, graphG2):
        self.P = P.copy()  # 2D array representing processing time.
        self.m = len(P)  # Number of machines.
        self.n = len(P[0]) if P else 0  # Number of jobs.
        self.t = 0  # Greedy Schedule.
        self.lp_makespan = lp_solution[0]  # Linear Programming Makespan.
        self.lp_xij = dict(lp_solution[1])  # Linear Programming decision variables.
        self.d = deadline  # Deadline d we achieved using Binary Search Procedure.
        self.makespan = rounded_solution[0]  # The Makespan of our Approximate Solution.
        self.xij = rounded_solution[1].copy()  # The decision variables of our Approximate Schedule.
        self.bipartite_graphG = graphG  # Graph G created using LP decision variables.
        self.bipartite_graphG2 = graphG2  # Graph G' created form Graph G removing rank 1 job nodes.

    def print_info(self) -> None:
        print(f'Pij: {self.m} machines x {self.n} jobs')
        print("Using Greedy Algorithm, Greedy makespan: t = ", self.t)
        print("Using Binary Search Procedure the deadline d that results in the best solution for our program: d = ",
              self.d)
        print("The Linear Programming LP(Pij,d⃗,t) with the deadline d creates a non-integer schedule with makespan: "
              "LP makespan = ", self.lp_makespan)
        print("This the final result. An approximate solution using Linear Programming,Bipartite Graph, 2-Relaxed "
              "Decision and Binary Search Procedure")
        print("Makespan: ", self.makespan)

    def print_schedule(self) -> None:
        print_schedule(self.P, (self.makespan, self.xij))

    def visualize_graphG(self):
        visualize_graph(self.bipartite_graphG)

    def visualize_graphG2(self):
        visualize_graph(self.bipartite_graphG2)
