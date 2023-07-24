class Graph:
    def __init__(self, lp_solution_xij: dict[tuple[int, int], float]):
        """
        Initialize a bipartite graph based on the LP solution.
        :param lp_solution_xij: Dictionary of LP solution decision variables { (i, j): variable, (i, j): variable, ... }
        """
        self.machine_nodes = set()  # Set of machine nodes
        self.job_nodes = set()  # Set of job nodes
        self.edges = set()  # Set of edges in the graph
        self.connected_components = []  # List to store connected components

        for (i, j), variable in lp_solution_xij.items():
            self.machine_nodes.add(i)  # Add machine node i to the set of machine nodes
            self.job_nodes.add(j)  # Add job node j to the set of job nodes

            if variable.varValue > 0:
                self.edges.add((i, j))  # Add edge (i, j) to the set of edges if the variable's value is greater than 0

        # Compute the connected components
        self.connected_components = self._compute_connected_components()

    def _compute_connected_components(self):
        """
        Helper method to find the connected components of the graph.
        :return: list: List of connected components, where each component is a set of edges.
        """
        visited = set()
        components = []

        for node in self.machine_nodes:
            if node not in visited:
                component = self._dfs(node, visited)
                components.append(component)

        return components

    def _dfs(self, start_node, visited):
        """
        Helper method for depth-first search (DFS) to find the connected component starting from a given node.
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
        for component in self.connected_components:
            machine_nodes = set()
            job_nodes = set()

            for edge in component:
                machine, job = edge
                machine_nodes.add(machine)
                job_nodes.add(job)

            if len(component) > len(machine_nodes) + len(job_nodes) - 1:  # Check if the condition is violated
                return False

        return True

    def is_tree_edge(self, edge):
        """
        Check if an edge is a tree edge. In the context of a graph, a "tree edge" refers to an edge that belongs to a
        tree within the graph. A tree is a type of graph where each node (or vertex) is connected to exactly one
        other node, except for one special node called the root that has no incoming edges. In a tree, there are no
        cycles or loops.
        The "tree edges" represent the edges within a connected component of the graph that form a tree structure.
        These edges connect the machine nodes to the job nodes in such a way that each job node has exactly one parent
        machine node. The tree edges are identified and used during the rounding process to create a matching that
        covers all the job nodes.
        The is_tree_edge method in the Graph class checks whether a given edge is a tree edge by examining the other
        edges in the graph. It compares the machine and job values of the input edge with the machine and job values
        of each other edge. If it finds a matching edge (i.e., an edge with the same machine and job values),
        it means that the input edge is not a tree edge. Otherwise, if no matching edge is found, it concludes that
        the input edge is a tree edge within the connected component of the graph.
        :param edge: The edge to check.
        :return: True if the edge is a tree edge, False otherwise.
        """
        machine, job = edge

        for other_edge in self.edges:
            if other_edge != edge:
                other_machine, other_job = other_edge
                if machine == other_machine and job == other_job:
                    return False

        return True
