"""
File: graphgui.py
Author: Delano Lourenco
Repo: https://github.com/3ddelano/graph-visualizer-python
License: MIT
"""


import os
from time import time, sleep
import tkinter.filedialog as filedialog
import tkinter as tk

from .graph_data.graph import Graph
from .constants import START_NODE_COLOR, END_NODE_COLOR, SCREEN_BG_COLOR
from .animations.path_animation import PathAnimation
from .animations.bfs_animation import BFSAnimation
from .animations.dfs_animation import DFSAnimation
from .interfaces.drawable import Drawable
from .edgegui import EdgeGUI
from .nodegui import NodeGUI

VERSION = "v.1.2"

DOUBLE_CLICK_TIME = 0.3
NODELIST_FILEPATH = "nodelist.csv"
EDGELIST_FILEPATH = "edgelist.csv"

ANIMATION_FRAME_DURATION = 9


class GraphGUI(Graph, Drawable):
    def __init__(self, canvas):
        # Selected node
        self.selected_node = None
        self.dragging_node = None

        # Selected edge
        self.selected_edge = None
        self.dragging_edge = None
        # [nodeA_pos_x, nodeA_pos_y, nodeB_pos_x, nodeB_pos_y, drag_start_x, drag_start_y]
        self.dragging_edge_offsets = [0, 0, 0, 0, 0, 0]

        # Double click time
        self.last_leftclick_time = time()
        self.last_rightclick_time = time()

        self.animation = None
        self.frames = 0
        self.help_visible = False
        self.node_id_visible = False

        # Path finding UI
        self.path_algorithm_name = tk.StringVar(value="dijkstra")
        self.start_node = None
        self.goal_node = None
        self.path = []

        super().__init__()
        self.init_ui(canvas)

    def deselect_nodes(self):
        if self.selected_node:
            self.selected_node.is_selected = False
            self.selected_node = None
        if self.dragging_node:
            self.dragging_node.is_dragging = False
            self.dragging_node = None

    def deselect_edges(self):
        if self.selected_edge:
            self.selected_edge.is_selected = False
            self.selected_edge = None
        if self.dragging_edge:
            self.dragging_edge.is_dragging = False
            self.dragging_edge = None

    def deselect_path(self):
        for i in range(len(self.path)):
            node = self.get_node_by_id(self.path[i][0])
            edge = self.path[i][1]
            node.is_selected = False
            if edge:
                edge.is_selected = False
                edge.nodeA.is_selected = False
                edge.nodeB.is_selected = False
        if self.start_node and self.goal_node:
            self.start_node = None
            self.goal_node = None
        self.path = []

    def get_clicked_node(self, x, y):
        for node in self.nodes:
            if node.is_clicked(x, y):
                return node
        return None

    def get_clicked_edge(self, x, y):
        for edge in self.edges:
            if edge.is_clicked(x, y):
                return edge
        return None

    def on_right_click(self, x, y):
        self.deselect_path()
        clicked_edge = self.get_clicked_edge(x, y)
        if not clicked_edge:
            # Empty area was right clicked
            self.deselect_edges()
            self.last_rightclick_time = time()
            return

        # Got a right click on an edge
        self.deselect_nodes()

        is_double_click = False

        time_since_last_rightclick = time() - self.last_rightclick_time
        if time_since_last_rightclick <= DOUBLE_CLICK_TIME:
            # Got a double click on an edge
            is_double_click = True

        if is_double_click:
            # It was a double click

            # If a edge was previously selected deselect it
            if self.selected_edge:
                self.selected_edge.is_selected = False
                self.selected_edge = None

            # Start dragging this edge
            clicked_edge.is_dragging = True
            self.dragging_edge = clicked_edge
            self.dragging_edge_offsets = [
                clicked_edge.nodeA.pos[0],
                clicked_edge.nodeA.pos[1],
                clicked_edge.nodeB.pos[0],
                clicked_edge.nodeB.pos[1],
                x,
                y,
            ]
        else:
            # It was a single right click
            if self.dragging_edge:
                # An edge was being dragged stop the drag
                self.dragging_edge.is_dragging = False
                self.dragging_edge = None

            elif self.selected_edge:
                # There was already a selected edge
                if clicked_edge == self.selected_edge:
                    # The same edge was selected again

                    # Deselect it
                    self.selected_edge.is_selected = False
                    self.selected_edge = None
                else:
                    # A different edge was selected

                    # Deselect the selected edge and select the clicked edge
                    self.selected_edge.is_selected = False
                    self.selected_edge = clicked_edge
                    self.selected_edge.is_selected = True
            else:
                # There was no selected node

                # Store the node as selected node
                self.selected_edge = clicked_edge
                clicked_edge.is_selected = True

        self.last_rightclick_time = time()

    def on_left_click(self, x, y):
        self.deselect_path()
        clicked_node = self.get_clicked_node(x, y)
        self.deselect_edges()

        if clicked_node:
            # A node was left clicked

            time_since_last_leftclick = time() - self.last_leftclick_time
            if time_since_last_leftclick <= DOUBLE_CLICK_TIME:
                # Got a double left click

                # Start dragging this node
                clicked_node.is_dragging = True
                self.dragging_node = clicked_node

                # If a node was selected deselect it
                if self.selected_node:
                    self.selected_node.is_selected = False
                    self.selected_node = None
            else:
                # It was a single click

                if self.dragging_node:
                    # A node was being dragged stop the drag and select that node
                    self.dragging_node.is_dragging = False
                    self.dragging_node = None

                elif self.selected_node:
                    # There was already a selected node

                    if clicked_node == self.selected_node:
                        # The same node was clicked again

                        # Deselect it
                        self.selected_node.is_selected = False
                        self.selected_node = None
                    else:
                        # A different node was clicked

                        # Create an edge between the two nodes if there isnt one
                        edge_exists = self.get_edge_between_nodes(
                            self.selected_node, clicked_node
                        )

                        if not edge_exists:
                            edge = EdgeGUI(self.selected_node, clicked_node)
                            self.add_edge(edge)

                        # Deselect the selected node and select the clicked node
                        self.selected_node.is_selected = False
                        self.selected_node = clicked_node
                        self.selected_node.is_selected = True
                else:
                    # There was no selected node

                    # Store the node as selected node
                    self.selected_node = clicked_node
                    clicked_node.is_selected = True
        else:
            # Empty area was clicked

            node = NodeGUI(x, y)
            self.add_node(node)

            if self.selected_node:
                # A node is already selected

                # Draw an edge from selected node to new clicked node
                edge = EdgeGUI(self.selected_node, node)
                self.add_edge(edge)

                # Deselect the selected node
                self.selected_node.is_selected = False
                # Select the new node
                self.selected_node = node
                self.selected_node.is_selected = True
            else:
                # There was no selected node

                # Mark the new node as the selected one
                node.is_selected = True
                self.selected_node = node

        self.last_leftclick_time = time()

    def ondrag(self, x, y):
        if self.dragging_node:
            # Node is being dragged
            self.dragging_node.pos[0] = x
            self.dragging_node.pos[1] = y
        elif self.dragging_edge:
            # Edge is being dragged
            nodeA = self.dragging_edge.nodeA
            nodeB = self.dragging_edge.nodeB
            offsets = self.dragging_edge_offsets

            nodeA.pos[0] = offsets[0] + x - offsets[4]
            nodeA.pos[1] = offsets[1] + y - offsets[5]
            nodeB.pos[0] = offsets[2] + x - offsets[4]
            nodeB.pos[1] = offsets[3] + y - offsets[5]

    def on_delete(self):
        if self.selected_node:
            # Delete the node
            node = self.selected_node
            node.is_selected = False
            self.delete_node(node)

            # Delete connected edges
            connected_edges = self.get_adjacent_edges(node)
            for edge in connected_edges:
                self.delete_edge(edge)

            self.selected_node = None
        elif self.selected_edge:
            # Delete the edge
            edge = self.selected_edge
            edge.is_selected = False
            self.delete_edge(edge)
            self.selected_edge = None

    def draw(self, tur, canvas):
        # Check if animation ended
        if self.animation and self.animation.is_ended():
            self.animation = None
            self.deselect_path()
            sleep(1)

        # Animate the animation if any
        animation_nodes = []
        animation_edges = []
        if self.animation:
            if self.frames % ANIMATION_FRAME_DURATION == 0:
                # Take a animation step
                self.animation.one_step()

            # Get the drawn nodes and edges from animation
            animation_nodes = self.animation.get_drawn_nodes()
            animation_edges = self.animation.get_drawn_edges()

        # Draw all edges
        for edge in self.edges:
            if not isinstance(edge, EdgeGUI):
                continue
            animation_drew_edge = False
            for edge_data in animation_edges:
                if edge == edge_data["edge"]:
                    edge.draw(tur, color=edge_data["color"])
                    animation_drew_edge = True
                    break
            if not animation_drew_edge:
                edge.draw(tur)

            edge.draw_weight(canvas)

        # Draw all nodes
        for node in self.nodes:
            if not isinstance(node, NodeGUI):
                continue
            animation_drew_node = False
            for node_data in animation_nodes:
                if node == node_data["node"]:
                    node.draw(tur, color=node_data["color"])
                    animation_drew_node = True
                    break
            if not animation_drew_node:
                if node == self.start_node:
                    node.draw(tur, color=START_NODE_COLOR)
                elif node == self.goal_node:
                    node.draw(tur, color=END_NODE_COLOR)
                else:
                    node.draw(tur)

            if self.node_id_visible:
                node.draw_id(canvas)

        self.frames += 1

        # Show help text
        self.draw_help(canvas)

    def draw_help(self, canvas):
        main_lines = ["H key - Toggle help text"]
        lines = [
            "Single Left Click - Add node / Select Node",
            "Single Right Click - Select Edge",
            "Double Left Click - Move Node",
            "Double Right Click - Move Edge",
            "",
            "D key - Delete Node/Edge",
            "W key - Update Edge Weight",
            "S key - Save Data",
            "L key - Load Data",
            "B key - Start BFS at selected node",
            "N key - Start DFS at selected node",
            "F key - Toggle node Id visibility",
            "",
            "github.com/3ddelano/graph-visualizer-python",
        ]
        font_size = 10
        font = f"Arial {font_size} normal"

        draw_y = 50
        for line in main_lines:
            # Draw the text
            canvas.create_text(
                0, draw_y, text=line, font=font, fill="white", anchor="w"
            )
            draw_y += font_size + 10

        if not self.help_visible:
            return

        for line in lines:
            # Draw the text
            canvas.create_text(
                0, draw_y, text=line, font=font, fill="white", anchor="w"
            )
            draw_y += font_size + 10

    def on_bfs_start(self):
        # Check if a node is selected
        if not self.selected_node:
            print("No node is selected for BFS")
            tk.messagebox.showerror("Error", "No node is selected for BFS")
            return

        # Start bfs from the selected node
        print("Starting BFS at node id=", self.selected_node.id)
        self.animation = BFSAnimation(self)
        self.animation.set_start_node(self.selected_node)
        self.deselect_nodes()
        tk.messagebox.showinfo("BFS result", self.animation.get_result_string())

    def on_dfs_start(self):
        # Check if a node is selected
        if not self.selected_node:
            print("No node is selected for DFS")
            tk.messagebox.showerror("Error", "No node is selected for DFS")
            return

        # Start dfs from the selected node
        print("Starting DFS at node id=", self.selected_node.id)
        self.animation = DFSAnimation(self)
        self.animation.set_start_node(self.selected_node)
        self.deselect_nodes()
        tk.messagebox.showinfo("DFS result", self.animation.get_result_string())

    def on_help_toggle(self):
        self.help_visible = not self.help_visible

    def on_nodeid_toggle(self):
        self.node_id_visible = not self.node_id_visible

    def on_update_weight(self):
        if not self.selected_edge:
            print("No edge is selected to set weight")
            tk.messagebox.showerror(
                "Set Weight Error", "No edge is selected to set weight"
            )
            return

        default_weight = round(
            self.get_euclidean_distance(
                self.selected_edge.nodeA, self.selected_edge.nodeB
            ),
            2,
        )
        new_weight = tk.simpledialog.askstring(
            title="Set Edge Weight",
            prompt="Enter the new weight for the edge",
            initialvalue=str(default_weight),
        )
        if new_weight is None:
            return

        try:
            new_weight = float(new_weight)
            self.update_edge_weight(self.selected_edge, new_weight)
        except Exception as e:
            print("Invalid weight provided to update edge weight")
            tk.messagebox.showerror(
                "Update Weight Error",
                "Invalid weight. Weight should be a valid number.",
            )
            return

    def on_save(self):
        save_folder = filedialog.askdirectory(mustexist=True)
        if save_folder == "":
            # User cancelled the save
            return
        success = self.save_to_files(
            os.path.join(save_folder, NODELIST_FILEPATH),
            os.path.join(save_folder, EDGELIST_FILEPATH),
        )
        if success:
            tk.messagebox.showinfo(
                "Saving Graph", "Graph saved to nodelist.csv and edgelist.csv"
            )

    def on_load(self):
        load_folder = filedialog.askdirectory(mustexist=True)
        if load_folder == "":
            # User cancelled the laod
            return

        node_path = os.path.join(load_folder, NODELIST_FILEPATH)
        edge_path = os.path.join(load_folder, EDGELIST_FILEPATH)

        if not os.path.exists(node_path):
            tk.messagebox.showerror(
                "Loading Graph Error", "nodelist.csv file not found"
            )
            return
        if not os.path.exists(edge_path):
            tk.messagebox.showerror(
                "Loading Graph Error", "edgelist.csv file not found"
            )
            return

        self.deselect_nodes()
        self.deselect_edges()
        self.deselect_path()
        self.load_from_files(node_path, edge_path)
        self.convert_graph_to_gui()

    def on_set_start_node(
        self,
    ):
        if not self.selected_node:
            print("No node is selected")
            tk.messagebox.showerror("Set Start Node Error", "No node is selected")
            return
        self.start_node = self.selected_node
        self.deselect_nodes()
        tk.messagebox.showinfo("Set Start Node", "Start node set successfully")

    def on_set_end_node(
        self,
    ):
        if not self.selected_node:
            print("No node is selected")
            tk.messagebox.showerror("Set Goal Node Error", "No node is selected")
            return
        self.goal_node = self.selected_node
        self.deselect_nodes()
        tk.messagebox.showinfo("Set Goal Node", "Goal node set successfully")

    def on_find_path(self):
        if self.animation:
            self.animation = None

        # Ensure that start and goal nodes are set
        if not self.start_node:
            tk.messagebox.showerror("Find Path Error", "Start node not set")
            return
        if not self.goal_node:
            tk.messagebox.showerror("Find Path Error", "Goal node not set")
            return

        temp_start_node = self.start_node
        temp_end_node = self.goal_node
        self.deselect_path()
        self.start_node = temp_start_node
        self.goal_node = temp_end_node

        # Array of node ids to be used for the path
        self.path = []
        self.path = self.find_shortest_path(
            self.path_algorithm_name.get(), self.start_node, self.goal_node
        )

        if len(self.path) < 2:
            tk.messagebox.showerror("Find Path Error", "No path found")
            return

        for i in range(len(self.path)):
            node = self.get_node_by_id(self.path[i][0])
            edge = self.path[i][1]
            node.is_selected = True
            if edge:
                edge.is_selected = True

    def on_anim_find_path(self):
        # Ensure that start and goal nodes are set
        if not self.start_node:
            tk.messagebox.showerror("Find Path Error", "Start node not set")
            return
        if not self.goal_node:
            tk.messagebox.showerror("Find Path Error", "Goal node not set")
            return

        temp_start_node = self.start_node
        temp_end_node = self.goal_node
        self.deselect_path()
        self.start_node = temp_start_node
        self.goal_node = temp_end_node

        animate_data = self.animate_shortest_path(
            self.path_algorithm_name.get(), self.start_node, self.goal_node
        )

        path = animate_data["final_path"]
        if not path or (path and len(path) < 2):
            tk.messagebox.showerror("Animate Path Error", "No path found")
            return

        edges = animate_data["visited_edges"]

        print(f"Starting {self.path_algorithm_name.get()} path animation")
        tk.messagebox.showinfo(
            "Path Finding Statistics",
            f"Number of nodes visited: {len(animate_data['visited_nodes'])}",
        )
        self.animation = PathAnimation(
            self, self.start_node, self.goal_node, path, edges
        )

    def convert_graph_to_gui(self):
        self.nodes = [NodeGUI(node.id, node.pos[0], node.pos[1]) for node in self.nodes]
        self.edges = [
            EdgeGUI(
                edge.id,
                self.get_node_by_id(edge.nodeA.id),
                self.get_node_by_id(edge.nodeB.id),
                edge.weight,
            )
            for edge in self.edges
        ]

    def init_ui(self, canvas):
        frame = tk.Frame(canvas.master.master)
        frame.config(bg=SCREEN_BG_COLOR)
        frame.place(x=10, y=10)
        pad_x = 1
        tk.Button(frame, text="Help Text", command=self.on_help_toggle).pack(
            padx=pad_x, side=tk.LEFT
        )
        tk.Button(frame, text="Node Id", command=self.on_nodeid_toggle).pack(
            padx=pad_x, side=tk.LEFT
        )

        tk.Button(frame, text="Load", command=self.on_load).pack(
            padx=pad_x, side=tk.LEFT
        )
        tk.Button(frame, text="Save", command=self.on_save).pack(
            padx=pad_x, side=tk.LEFT
        )

        tk.Button(frame, text="Delete", command=self.on_delete).pack(
            padx=pad_x, side=tk.LEFT
        )
        tk.Button(frame, text="Set Weight", command=self.on_update_weight).pack(
            padx=pad_x, side=tk.LEFT
        )

        tk.Button(frame, text="BFS Anim", command=self.on_bfs_start).pack(
            padx=pad_x, side=tk.LEFT
        )
        tk.Button(frame, text="DFS Anim", command=self.on_dfs_start).pack(
            padx=pad_x, side=tk.LEFT
        )

        tk.Button(frame, text="Set Start Node", command=self.on_set_start_node).pack(
            padx=pad_x, side=tk.LEFT
        )
        tk.Button(frame, text="Set Goal Node", command=self.on_set_end_node).pack(
            padx=pad_x, side=tk.LEFT
        )

        tk.Button(frame, text="Find Path", command=self.on_find_path).pack(
            padx=pad_x, side=tk.LEFT
        )
        tk.Button(frame, text="Anim Find Path", command=self.on_anim_find_path).pack(
            padx=pad_x, side=tk.LEFT
        )

        # Create radio buttons
        tk.Radiobutton(
            frame,
            text="BFS",
            variable=self.path_algorithm_name,
            value="bfs",
        ).pack(side=tk.LEFT, padx=(5, 0))
        tk.Radiobutton(
            frame,
            text="DFS",
            variable=self.path_algorithm_name,
            value="dfs",
        ).pack(side=tk.LEFT)
        tk.Radiobutton(
            frame,
            text="Dijkstra",
            variable=self.path_algorithm_name,
            value="dijkstra",
        ).pack(side=tk.LEFT)
        tk.Radiobutton(
            frame,
            text="A*",
            variable=self.path_algorithm_name,
            value="astar",
        ).pack(side=tk.LEFT)
