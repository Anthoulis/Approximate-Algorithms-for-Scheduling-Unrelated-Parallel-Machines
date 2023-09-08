from pulp import LpVariable


class SchedulingProblem:
    def __init__(self, P: list[list[int]]):
        """Constructor for the SchedulingProblem class."""
        self.P = P  # 2D array representing processing time
        self.m = len(P)  # Number of machines
        self.n = len(P[0]) if P else 0  # Number of jobs
        self.xij = [[0 for _ in range(self.n)] for _ in range(self.m)]  # Decision variable matrix initialized to zeros
        self.makespan = 0  # Initialize makespan to zero

    def update_xij(self, lp_xij: dict[tuple[int, int], LpVariable]) -> None:
        """
        Updates the decision variable matrix xij based on LP solutions.

        :param lp_xij: Dictionary of LpVariables from the LP solution
        """
        if lp_xij is not None:
            for i in range(self.m):
                for j in range(self.n):
                    if (i, j) in lp_xij:
                        self.xij[i][j] = lp_xij[(i, j)].varValue

    def calculate_makespan(self) -> int:
        """
        Calculates the makespan based on the Pij matrix and xij decision variables.

        :return: The calculated makespan.
        """
        # Initialize machine completion times to zeros
        completion_times = [0] * self.m

        # Calculate completion times for each machine
        for i in range(self.m):
            for j in range(self.n):
                completion_times[i] += self.xij[i][j] * self.P[i][j]

        # Update and return makespan
        self.makespan = max(completion_times)
        return self.makespan

    def print_info(self) -> None:
        """Prints basic scheduling info."""
        print(f'Pij: {self.m} machines x {self.n} jobs')

    def print_schedule(self) -> None:
        """Prints the scheduling results."""
        print(f"Makespan = {self.makespan}")
        max_job_width = len(f"Job{self.n - 1}")  # Determine max width for job names

        for i in range(self.m):
            # List jobs assigned to each machine
            assigned_jobs = [f"Job{j}".ljust(max_job_width) for j in range(self.n) if self.xij[i][j] == 1]
            print(f"Machine {i}: [ {', '.join(assigned_jobs)} ]")
