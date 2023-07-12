class Graph:
    def __init__(self, lp_solution_xij):
        """
        Initialize a bipartite graph based on the LP solution.
        :param lp_solution_xij: (dict): LP solution dictionary { (i, j): value, (i, j): value, ... }
        """
        self.machine_nodes = set()  # Set of machine nodes
        self.job_nodes = set()  # Set of job nodes
        self.edges = set()  # Set of edges in the graph

        for variable in lp_solution_xij:
            machine, job = variable
            self.machine_nodes.add(machine)
            self.job_nodes.add(job)
            if lp_solution_xij[machine, job] > 0:
                self.edges.add((machine, job))

    def get_connected_components(self):
        """
        Find the connected components of the graph.
        :return: list: List of connected components, where each component is a set of edges.
        """
        visited = set()
        components = []

        for node in self.machine_nodes:
            if node not in visited:
                component = self.dfs(node, visited)
                components.append(component)

        return components

    def dfs(self, start_node, visited):
        """
        Depth-first search (DFS) to find the connected component starting from a given node.
        :param start_node: The starting node for DFS.
        :param visited: A set of visited nodes.
        :return: set: The connected component as a set of edges.
        """
        stack = [start_node]
        component = set()

        while stack:
            node = stack.pop()
            if node not in visited:
                visited.add(node)
                component.add(node)
                stack.extend(self.job_nodes - visited)

        return component

    def is_pseudoforest(self):
        """
        Check if the graph is a pseudoforest.
        :return: bool: True if the graph is a pseudoforest, False otherwise.
        """
        components = self.get_connected_components()

        for component in components:
            machine_nodes = set()
            job_nodes = set()

            for edge in component:
                machine, job = edge
                machine_nodes.add(machine)
                job_nodes.add(job)

            if len(component) < len(machine_nodes) + len(job_nodes) - 1:
                return False

        return True

    def is_tree_edge(self, edge):
        """
        Check if an edge is a tree edge. In the context of a graph, a "tree edge" refers to an edge that belongs to a
        tree within the graph. A tree is a type of graph where each node (or vertex) is connected to exactly one
        other node, except for one special node called the root that has no incoming edges. In a tree, there are no
        cycles or loops.

        In the specific context of the algorithm you are working on, the "tree edges" represent the edges within a
        connected component of the graph that form a tree structure. These edges connect the machine nodes to the job
        nodes in such a way that each job node has exactly one parent machine node. The tree edges are identified and
        used during the rounding process to create a matching that covers all the job nodes.

        The is_tree_edge method in the Graph class checks whether a given edge is a tree edge by examining the other
        edges in the graph. It compares the machine and job values of the input edge with the machine and job values
        of each other edge. If it finds a matching edge (i.e., an edge with the same machine and job values),
        it means that the input edge is not a tree edge. Otherwise, if no matching edge is found, it concludes that
        the input edge is a tree edge within the connected component of the graph. :param edge: The edge to check.
        :return: True if the edge is a tree edge, False otherwise.
        """
        machine, job = edge

        for other_edge in self.edges:
            if other_edge != edge:
                other_machine, other_job = other_edge
                if machine == other_machine and job == other_job:
                    return False

        return True


"""
define a bipartite graph G(x) = (M, J, E) where M={1,..., m} and J={l,..., n} correspond
to the sets of machines and jobs,and  E = {(i, j) | xij > 0}
We have already indicated that G(£) has no more edges than nodes. We now show that each connected component of G(~x)
has this property; that is, G(~x) is a pseudoforest.

Let C be a connected component of G(~x).
Let ~x_C denote the restriction of ~x to components ~xij such that i e M_C and j e J_C




    1.  Start with a feasible LP solution x̃, which is a vertex of the LP polyhedron.
    2.  Construct a bipartite graph G(x̃) using the LP solution, where the machine nodes correspond to the set of
        machines (M) and the job nodes correspond to the set of jobs (J). The edges (E) in the graph are determined
        by the non-zero values of x̃.
    3.  Verify that each connected component of G(x̃) forms a pseudoforest, which means the number of edges is less than
        or equal to the number of nodes.
    4.  For each connected component C, divide the LP solution x̃ into x̃_C and x̃_C̅ based on the corresponding machines
        and jobs in C. Also, restrict the matrix P to the machines and jobs in C, resulting in P_C. Similarly, restrict
        the deadline vector d⃗ to the machines in C, resulting in d⃗_C.
"""


def create_matching(tree_edges, cycle_edges, unmatched_job_nodes):
    matching = {}

    for edge in tree_edges:
        machine, job = edge
        matching[(machine, job)] = 1
        unmatched_job_nodes.discard(job)

    for edge in cycle_edges:
        machine, job = edge
        if job in unmatched_job_nodes:
            matching[(machine, job)] = 1
            unmatched_job_nodes.remove(job)

    return matching


def round_lp_solution(lp_solution):
    # Step 1: Construct the bipartite graph G(Y)
    graph = Graph(lp_solution)  # Create an instance of the Graph class using the LP solution

    components = graph.get_connected_components()  # Identify the connected components of the graph
    if not graph.is_pseudoforest():  # Check if the graph is a pseudoforest
        raise ValueError("Graph is not a pseudoforest.")

    rounded_solution = {}  # Initialize the rounded solution dictionary
    matched_job_nodes = set()  # Track the job nodes that have been matched

    for component in components:
        tree_edges = []  # Edges belonging to a tree
        cycle_edges = []  # Edges belonging to a cycle
        unmatched_job_nodes = set()  # Unmatched job nodes within the component

        for edge in component:
            machine, job = edge
            if lp_solution[edge] == 1:
                rounded_solution[edge] = 1  # Add edge to the rounded solution (matching)
                matched_job_nodes.add(job)  # Mark the job node as matched
            else:
                if graph.is_tree_edge(edge):  # Check if the edge is a tree edge
                    tree_edges.append(edge)  # Store the edge in the tree edges list
                else:
                    cycle_edges.append(edge)  # Store the edge in the cycle edges list
                unmatched_job_nodes.add(job)  # Mark the job node as unmatched

        matching = create_matching(tree_edges, cycle_edges, unmatched_job_nodes)  # Create the matching
        rounded_solution.update(matching)  # Add the matching to the rounded solution

    for job in set(graph.job_nodes) - matched_job_nodes:
        rounded_solution[(None, job)] = 0  # Assign remaining unmatched job nodes to 0

    return rounded_solution
