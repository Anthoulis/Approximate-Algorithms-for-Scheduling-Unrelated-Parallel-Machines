"""
Step1: Define Bipartite Graph G(x) = (M, J, E), where M = {1,...,m} and J = {1,...,n} correspond to the sets of
        machines and jobs, respectively, and E={(i, j) | x_ij>0}

Step2: Find connected components

Step3: We have to check that G(x) is a pseudoforest.
        So we check that every connected component has this property.
        Each connected component has no more edges than nodes.
        
Step4: Each edge (i,j) with x_ij = 1.
        These jobs correspond to the job nodes of degree 1, so that by deleting all of
        these nodes we get a pseudoforest G'(x) with the additional property that each job node has degree at least 2.

Step5: This is the last step where the lp_solution_xij becomes the solution for our project through this procedure:

We show that G'(x) has a matching that covers all the job nodes.

For each component that is a tree, root the tree at any node, and match each job node with any one of its children.
* Note that each job node must have at least one child and that,
* since each node has at most one parent,
* no machine is matched with more than one job.

For each component that contains a cycle, take alternate edges of the cycle in the matching.
* Note that the cycle must be of even length.
If the edges of the cycle are deleted, we get a collection of trees which we think of as rooted at the node that had
been contained in the cycle.
For each job node that is not already matched, pair it with one of its children.

If (i, j) is in the matching, set xij = 1.
Each remaining xij that has not been assigned is set to 0.
"""
from pulp import *
import networkx as nx
import matplotlib.pyplot as plt


class BipartiteGraph:
    def __init__(self, lp_solution_xij: dict[tuple[int, int], LpVariable], num_machines: int, num_jobs: int):
        """
        Initializes the BipartiteGraph class with a given LP solution, number of machines, and number of jobs.

        :param lp_solution_xij: Dictionary containing LP solution variables.
        :param num_machines: Number of machines in the graph.
        :param num_jobs: Number of jobs in the graph.
        """

        # Step 1
        #   Fields
        self.graph = nx.Graph()  # Create an empty bipartite graph using NetworkX
        self.lp_solution_xij = lp_solution_xij
        self.m = num_machines
        self.n = num_jobs
        self.connected_components = []
        self.is_pseudoforest = True
        self.connected_subgraphs = []
        self.matching = []

        # Add machine nodes with names like "m0", "m1", ...
        for machine_id in range(num_machines):
            self.graph.add_node(f"m{machine_id}", bipartite=0)  # 'bipartite=0' indicates machine nodes

        # Add job nodes with names like "j0", "j1", ...
        for job_id in range(num_jobs):
            self.graph.add_node(f"j{job_id}", bipartite=1)  # 'bipartite=1' indicates job nodes

        # Add edges between machines and jobs based on lp_solution_xij
        for (i, j), variable in lp_solution_xij.items():
            if variable.varValue > 0:
                self.graph.add_edge(f"m{i}", f"j{j}")

        # Step 2
        self.find_connected_components()
        print("\nGraph G")
        self.print_graph_info()
        self.visualize_graph()
        # Step 3
        self.check_pseudoforest_property()

        # step 4
        self.remove_single_degree_jobs()
        self.find_connected_components()
        self.visualize_graph()
        print("\nGraph G'")
        self.print_graph_info()

        # step 5
        self.find_connected_subgraphs()
        self.matching_process()

    """---------    Step 2  ------------"""

    def find_connected_components(self):
        """
        Finds the connected components of the graph and stores them in the class attribute `connected_components`.
        """

        self.connected_components = list(nx.connected_components(self.graph))

    """---------    Step 3  ------------"""

    def check_pseudoforest_property(self):
        """
        Checks if the graph and its connected components have the pseudoforest property.
        Prints an error message if the property is not satisfied.
        """
        if self.graph.number_of_edges() > self.graph.number_of_nodes():
            print("Our Graph is not a pseudoforest. Number of edges > number of nodes")
            self.is_pseudoforest = False
        for component in self.connected_components:
            subgraph = self.graph.subgraph(component)
            if subgraph.number_of_edges() > subgraph.number_of_nodes():
                print("A subgraph doesnt have pseudoforest property.")
                self.print_subgraph_info()
                self.is_pseudoforest = False
                return

    """---------    Step 4  ------------"""

    def remove_single_degree_jobs(self):
        """
        Removes job nodes with degree 1 from the graph.
        """
        # Find job nodes with degree 1
        single_degree_jobs = [node for node in self.get_job_nodes() if self.graph.degree(node) == 1]

        # Remove job nodes with degree 1 along with their edges
        for job in single_degree_jobs:
            self.graph.remove_node(job)

    def find_connected_subgraphs(self):
        """
        Finds and stores the connected subgraphs of the graph after removing single-degree jobs.
        """
        for component in self.connected_components:
            subgraph = self.graph.subgraph(component)
            self.connected_subgraphs.append(subgraph)

    """---------    Step 5  ------------"""

    def match_tree_component(self, subgraph):
        """
        Performs the matching process for tree components in the graph.
        Updates the final matching.
        :param subgraph: A NetworkX subgraph representing a connected component of the graph.
        :return: True if the matching process is successful.
        """
        is_successful = True

        # Each job node must have at least one child
        job_nodes = [node for node in subgraph.nodes if node.startswith("j")]
        if not job_nodes:
            print("Error: No job nodes in the subgraph.")
            return False
        for job_node in job_nodes:
            neighbors = list(subgraph.neighbors(job_node))
            if not any(neighbor for neighbor in neighbors):
                print("Error: Each job node doesn't have at least one child")

        # Initialize a dictionary to store the matching
        matching = {}  # ex. mathing[j0] = m3
        matched_machines = set()  # Set to keep track of matched machines

        # Choose any node as the root of the tree
        root = job_nodes[0]

        # Depth-First Search (DFS)
        def dfs(node, parent):
            # For job nodes, match them with their child
            if node.startswith("j"):
                # Find the first child node that is not the parent
                for neighbor in subgraph.neighbors(node):
                    if neighbor != parent:
                        matching[node] = neighbor
                        matched_machines.add(neighbor)
                        break

            # Recursively visit children
            for neighbor in subgraph.neighbors(node):
                if neighbor != parent:
                    dfs(neighbor, node)

        # Start the DFS from the root
        dfs(root, None)

        # Checking for matched machines being paired with more than one job
        if len(matched_machines) != len(matching):
            print("Error: A machine node is matched with more than one job")
            is_successful = False

        # Each job node must be matched with a different machine
        if len(matched_machines) != len(job_nodes):
            print("Error: Each job isn't matched with different machine")
            is_successful = False

        # Update the final matching
        for job_node, machine_node in matching.items():
            # [1: ]: This is a slicing operation that starts from the character at index 1 and goes until the end of
            # the string.
            self.matching.append((int(machine_node[1:]), int(job_node[1:])))

        return is_successful

    def match_cycle_component(self, subgraph):
        """
        Performs the matching process for cycle components in the graph.
        Updates the final matching.
        :param subgraph: A NetworkX subgraph representing a connected component of the graph.
        :return: True if the matching process is successful, False otherwise.
        """
        # Check if the graph is empty
        if subgraph.number_of_nodes() == 0:
            print("Error: The graph is empty.")
            return False

        is_successful = True

        # Identify the cycle in the component
        cycles = list(nx.simple_cycles(subgraph.to_directed()))
        if not cycles or len(cycles[0]) % 2 != 0:
            print("Error: The component must contain one even-length cycle.")
            return False

        # If there is a cycle, remove one arbitrary edge from it.
        if len(cycles[0]) >= 2:
            u, v = cycles[0][0], cycles[0][1]
            subgraph.remove_edge(u, v)

        # Now the subgraph is a tree
        self.match_tree_component(subgraph)

        return is_successful

    def matching_process(self):
        """
        Main method to process the matching according to the described steps.
        """

        for component in self.connected_components:
            subgraph = self.graph.subgraph(component)
            # if number of edges < number of nodes
            if nx.is_tree(subgraph):
                self.match_tree_component(subgraph)
            # number of edges = number of nodes
            else:
                self.match_cycle_component(subgraph)

    # %-------------------------- Helpful Functions for printing and visualization    --------------------------------%
    def get_machine_nodes(self):
        return [node for node in self.graph.nodes if node.startswith("m")]

    def get_job_nodes(self):
        return [node for node in self.graph.nodes if node.startswith("j")]

    # Print   ------------------------------------
    def print_graph_info(self):
        if self.is_pseudoforest:
            print("Pseudoforest Property applies. Graph is a pseudoforest")
        print("Number of nodes:", len(self.graph.nodes))
        print("Number of edges:", len(self.graph.edges))
        # print("\nNodes in the graph:\n",self.graph.nodes)
        # print("\nEdges in the graph:\n",self.graph.edges)
        print("List size of different connected components:", len(self.connected_components), "\n")

    def print_subgraph_info(self):
        print("------------------ Subgraph Info ----------------")
        for idx, subgraph in enumerate(self.connected_subgraphs, start=1):
            print(f"Connected Subgraph {idx}: Nodes={subgraph}")
            subgraph_edges = self.graph.subgraph(subgraph).edges
            print("Edges:", subgraph_edges)

    #  Visualize    ------------------------------------

    def visualize_graph(self):
        plt.figure()  # Create a new figure
        pos = nx.bipartite_layout(self.graph, nodes=self.get_machine_nodes())
        nx.draw(self.graph, pos, with_labels=True, node_color="skyblue", node_size=500, font_size=8)
        plt.title("Bipartite Graph Representation")
        plt.show()  # Show the figure

    def visualize_connected_subgraphs(self):
        plt.figure(figsize=(12, 12))  # Create a new figure and adjust the size
        pos = nx.spring_layout(self.graph)
        colors = ['r', 'g', 'b', 'y', 'c', 'm', 'o', 'k']

        for idx, subgraph_nodes in enumerate(self.connected_components):
            subgraph = self.graph.subgraph(subgraph_nodes)
            nx.draw_networkx_nodes(subgraph, pos, nodelist=subgraph_nodes,
                                   node_color=colors[idx % len(colors)], node_size=500)
            nx.draw_networkx_edges(subgraph, pos, edgelist=subgraph.edges(), edge_color=colors[idx % len(colors)])
            nx.draw_networkx_labels(subgraph, pos, labels={n: n for n in subgraph_nodes}, font_size=8)

        plt.title("Connected Subgraphs of the Graph")
        plt.show()  # Show the figure
