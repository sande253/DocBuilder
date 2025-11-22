from manim import *

class DFSScene(Scene):
    def construct(self):
        # 1. Define the Graph Structure
        # Adjacency list representation of the graph
        graph_data = {
            'A': ['B', 'C'],
            'B': ['A', 'D'],
            'C': ['A', 'B', 'E'],
            'D': ['B', 'E'],
            'E': ['C', 'D']
        }

        # Define node positions for a clear, non-overlapping layout
        # These are precomputed target positions corresponding to logical indices (node labels)
        node_positions = {
            'A': [-3, 2, 0],
            'B': [-1, 0, 0],
            'C': [1, 0, 0],
            'D': [-1, -2, 0],
            'E': [1, -2, 0]
        }

        # 2. Create Nodes
        node_mobjects = {} # Dictionary to store VGroup for each node label
        for label, pos in node_positions.items():
            # Create a circle for the node shape
            circle = Circle(radius=0.4, color=BLUE, fill_opacity=0.8)
            # Create text for the node label, initially white
            text = Text(label, color=WHITE).scale(0.7)
            # Combine shape and text into a VGroup as required
            node_vgroup = VGroup(circle, text)
            # Position the VGroup at the precomputed location
            node_vgroup.move_to(pos)
            node_mobjects[label] = node_vgroup

        # 3. Create Edges
        edges_vgroup = VGroup() # VGroup to hold all edge Mobjects
        edge_mobjects = {}     # Dictionary to store Line Mobjects for easy lookup during DFS
        drawn_edges = set()    # To prevent drawing duplicate edges (e.g., A-B and B-A)

        for u, neighbors in graph_data.items():
            for v in neighbors:
                # Ensure each unique edge is drawn only once
                if (u, v) not in drawn_edges and (v, u) not in drawn_edges:
                    # Get the center of the circle for start and end points of the line
                    start_point = node_mobjects[u][0].get_center()
                    end_point = node_mobjects[v][0].get_center()
                    # Create a line for the edge
                    line = Line(start_point, end_point, color=WHITE, stroke_width=3)
                    edges_vgroup.add(line)
                    # Store the line Mobject for both directions for easy access during DFS
                    edge_mobjects[(u, v)] = line
                    edge_mobjects[(v, u)] = line
                    drawn_edges.add((u, v)) # Mark this edge as drawn

        # Animate the creation of all nodes and edges
        self.play(
            LaggedStart(*[Create(node_mobjects[label]) for label in node_positions]),
            Create(edges_vgroup),
            run_time=2
        )
        self.wait(0.5)

        # 4. Initialize DFS State
        visited = set()          # Set to keep track of visited nodes
        dfs_path_labels = []     # List to store the order of visited nodes for display
        
        # Text Mobject to display the DFS traversal path, positioned at the upper-left corner
        dfs_path_text_display = Text("DFS Path: ", font_size=36).to_corner(UL)
        self.add(dfs_path_text_display)

        # Helper function to update the DFS path display
        def update_dfs_path_display():
            nonlocal dfs_path_text_display # Declare nonlocal to modify the outer scope variable
            # Create a new Text Mobject with the updated path
            new_text = Text("DFS Path: " + " -> ".join(dfs_path_labels), font_size=36).to_corner(UL)
            # Animate the transformation from the old text to the new text
            self.play(Transform(dfs_path_text_display, new_text), run_time=0.5)
            # Update the reference to the new Mobject for subsequent transformations
            dfs_path_text_display = new_text

        # 5. Animate DFS Algorithm (recursive function)
        def dfs_recursive(current_node_label):
            # Mark the current node as visited and add to the path list
            visited.add(current_node_label)
            dfs_path_labels.append(current_node_label)

            current_node_mobj = node_mobjects[current_node_label]

            # Animate visiting the current node: change circle color to RED, text to BLACK for contrast
            self.play(
                current_node_mobj[0].animate.set_color(RED), # Circle (first element of VGroup)
                current_node_mobj[1].animate.set_color(BLACK), # Text (second element of VGroup)
                run_time=0.7
            )
            update_dfs_path_display() # Update the path display on screen
            self.wait(0.3)

            # Explore neighbors
            for neighbor_label in graph_data[current_node_label]:
                if neighbor_label not in visited:
                    # Get the edge Mobject connecting current node and neighbor
                    edge_mobj = edge_mobjects[(current_node_label, neighbor_label)]
                    
                    # Animate traversing the edge: highlight it in YELLOW
                    self.play(
                        edge_mobj.animate.set_stroke(color=YELLOW, width=5), # Animate stroke color and width
                        run_time=0.7
                    )
                    self.wait(0.3)

                    # Recursive call to explore the neighbor
                    dfs_recursive(neighbor_label)

                    # Animate backtracking: reset edge color to original WHITE
                    self.play(
                        edge_mobj.animate.set_stroke(color=WHITE, width=3), # Reset stroke color and width
                        run_time=0.7
                    )
                    self.wait(0.3)

            # Animate finishing the current node (all its reachable neighbors explored)
            # Change circle color to GREEN to indicate completion, text back to WHITE
            self.play(
                current_node_mobj[0].animate.set_color(GREEN), # Circle
                current_node_mobj[1].animate.set_color(WHITE), # Text
                run_time=0.7
            )
            self.wait(0.3)

        # Start the DFS traversal from node 'A'
        self.wait(1)
        dfs_recursive('A')

        self.wait(2) # Keep the final state on screen for a bit
