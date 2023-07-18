class Graph:
    def __init__(self, lp_solution_xij):
        """
        Initialize a bipartite graph based on the LP solution.
        :param lp_solution_xij: (dict): LP solution dictionary { (i, j): LpVariable, (i, j): LpVariable, ... }
        """
        self.machine_nodes = set()  # Set of machine nodes
        self.job_nodes = set()  # Set of job nodes
        self.edges = set()  # Set of edges in the graph

        for variable, lp_variable in lp_solution_xij.items():
            machine, job = variable
            self.machine_nodes.add(machine)
            self.job_nodes.add(job)
            if lp_variable.varValue > 0:  # Compare the variable's value with 0
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
