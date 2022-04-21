# Graph Visualizer
# 27 Jan 2021
# Group 2 - CSE1014 Lab

from time import time
from os import path
from graph_interface import GraphInterface
from node import Node
from edge import Edge
from bfs_animation import BFSAnimation
from dfs_animation import DFSAnimation

DOUBLE_CLICK_TIME = 0.3
NODELIST_FILEPATH = "nodelist.csv"
EDGELIST_FILEPATH = "edgelist.csv"

ANIMATION_FRAME_DURATION = 9


class Graph(GraphInterface):
    def __init__(self):
        self.nodes = []
        self.edges = []

        self.selected_node = None
        self.dragging_node = None
        self.dragging_edge = None
        self.selected_edge = None
        self.dragging_edge_nodeA_offset = [0, 0]
        self.dragging_edge_nodeB_offset = [0, 0]
        self.dragging_edge_start_offset = [0, 0]

        self.last_leftclick_time = time()
        self.last_rightclick_time = time()

        self.animation = None
        self.frames = 0
        self.help_visible = True
        self.node_id_visible = False

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

    def is_edge_exists(self, nodeA, nodeB):
        for edge in self.edges:
            if edge.nodeA == nodeA and edge.nodeB == nodeB:
                return True
            if edge.nodeB == nodeA and edge.nodeA == nodeB:
                return True
        return False

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

    def get_adjacent_edges(self, node):
        connected_edges = []

        for edge in self.edges:
            if edge.nodeA == node or edge.nodeB == node:
                connected_edges.append(edge)

        return connected_edges

    def get_adjacent_nodes(self, node):
        connected_nodes = []

        for edge in self.edges:
            if edge.nodeA == node:
                connected_nodes.append(edge.nodeB)
            elif edge.nodeB == node:
                connected_nodes.append(edge.nodeA)

        return connected_nodes

    def get_edge(self, nodeA, nodeB):
        for edge in self.edges:
            if edge.nodeA == nodeA and edge.nodeB == nodeB:
                return edge
            if edge.nodeB == nodeA and edge.nodeA == nodeB:
                return edge
        return None

    def get_node_by_id(self, id):
        for node in self.nodes:
            if node.id == id:
                return node
        return None

    def onrightclick(self, x, y):
        clicked_edge = self.get_clicked_edge(x, y)
        if clicked_edge:
            # Got a right click on an edge

            self.deselect_nodes()

            time_since_last_rightclick = time() - self.last_rightclick_time
            if time_since_last_rightclick <= DOUBLE_CLICK_TIME:
                # Got a double click on an edge
                # Start dragging this edge
                clicked_edge.is_dragging = True
                self.dragging_edge_nodeA_offset = [
                    clicked_edge.nodeA.pos[0],
                    clicked_edge.nodeA.pos[1],
                ]
                self.dragging_edge_nodeB_offset = [
                    clicked_edge.nodeB.pos[0],
                    clicked_edge.nodeB.pos[1],
                ]
                self.dragging_edge_start_offset = [x, y]
                self.dragging_edge = clicked_edge

                # If a edge was selected deselect it
                if self.selected_edge:
                    self.selected_edge.is_selected = False
                    self.selected_edge = None
            else:
                # It was a single right click

                if self.dragging_edge:
                    # An edge was being dragged stop the drag
                    self.dragging_edge.is_dragging = False
                    self.dragging_edge = None

                    # self.selected_edge = clicked_edge
                    # self.selected_edge.is_selected = True

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
        else:
            # Empty area was right clicked

            self.deselect_edges()

        self.last_rightclick_time = time()

    def onleftclick(self, x, y):
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
                        edge_exists = self.is_edge_exists(
                            self.selected_node, clicked_node
                        )

                        if not edge_exists:
                            edge = Edge(self.selected_node, clicked_node)
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

            node = Node(x, y)
            self.add_node(node)

            if self.selected_node:
                # A node is already selected

                # Draw an edge from selected node to new clicked node
                edge = Edge(self.selected_node, node)
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
            self.dragging_node.pos[0] = x
            self.dragging_node.pos[1] = y
        elif self.dragging_edge:
            nodeA = self.dragging_edge.nodeA
            nodeB = self.dragging_edge.nodeB

            nodeA.pos[0] = (
                self.dragging_edge_nodeA_offset[0]
                + x
                - self.dragging_edge_start_offset[0]
            )
            nodeA.pos[1] = (
                self.dragging_edge_nodeA_offset[1]
                + y
                - self.dragging_edge_start_offset[1]
            )
            nodeB.pos[0] = (
                self.dragging_edge_nodeB_offset[0]
                + x
                - self.dragging_edge_start_offset[0]
            )
            nodeB.pos[1] = (
                self.dragging_edge_nodeB_offset[1]
                + y
                - self.dragging_edge_start_offset[1]
            )

    def onsave(self):
        # Save the list of nodes to a csv file
        print(f"Saving graph to {NODELIST_FILEPATH} and {EDGELIST_FILEPATH}")
        with open(NODELIST_FILEPATH, "w") as file:
            for i, node in enumerate(self.nodes):
                # id,x,y
                line = f"{node.id},{node.pos[0]},{node.pos[1]}"
                if i != len(self.nodes) - 1:
                    line += "\n"

                file.write(line)

        with open(EDGELIST_FILEPATH, "w") as file:
            for i, edge in enumerate(self.edges):
                # id,nodeA_id,nodeB_id
                line = f"{edge.id},{edge.nodeA.id},{edge.nodeB.id}"
                if i != len(self.edges) - 1:
                    line += "\n"

                file.write(line)

    def onload(self):
        # Load nodes and edges from NODELIST_FILEPATH and EDGELIST_FILEPATH
        if not path.isfile(NODELIST_FILEPATH) and not path.isfile(EDGELIST_FILEPATH):
            # Savefiles dont exist
            print(f"No {NODELIST_FILEPATH} and {EDGELIST_FILEPATH} files found")
            return

        print(f"Loading graph from {NODELIST_FILEPATH} and {EDGELIST_FILEPATH}")
        self.deselect_edges()
        self.deselect_nodes()
        self.nodes = []
        self.edges = []
        with open(NODELIST_FILEPATH, "r") as file:
            for line in file:
                # id,x,y
                line = line.strip().split(",")
                node = Node(int(line[0]), float(line[1]), float(line[2]))
                self.add_node(node)

        with open(EDGELIST_FILEPATH, "r") as file:
            for line in file:
                # id,nodeA_id,nodeB_id
                line = line.strip().split(",")
                nodeA = self.get_node_by_id(int(line[1]))
                nodeB = self.get_node_by_id(int(line[2]))
                edge = Edge(int(line[0]), nodeA, nodeB)
                self.add_edge(edge)

    def ondelete(self):
        if self.selected_node:
            # Delete the node
            node = self.selected_node
            node.is_selected = False
            self.remove_node(node)

            # Delete connected edges
            connected_edges = self.get_adjacent_edges(node)
            for edge in connected_edges:
                self.remove_edge(edge)

            self.selected_node = None
        elif self.selected_edge:
            # Delete the edge
            edge = self.selected_edge
            edge.is_selected = False
            self.remove_edge(edge)
            self.selected_edge = None

    def draw(self, tur):
        # Check if animation ended
        if self.animation and self.animation.is_ended():
            self.animation = None

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
            animation_drew_edge = False
            for edge_data in animation_edges:
                if edge == edge_data["edge"]:
                    edge.draw(tur, color=edge_data["color"])
                    animation_drew_edge = True
                    break
            if not animation_drew_edge:
                edge.draw(tur)

        # Draw all nodes
        for node in self.nodes:
            animation_drew_node = False
            for node_data in animation_nodes:
                if node == node_data["node"]:
                    node.draw(tur, color=node_data["color"])
                    animation_drew_node = True
                    break
            if not animation_drew_node:
                node.draw(tur)

            if self.node_id_visible:
                node.draw_id(tur)

        self.frames += 1

        # Show help text
        self.draw_help(tur)

    def draw_help(self, tur):
        main_lines = [
            "Graph Visualizer v1.0",
            "H key - Toggle help text",
        ]
        lines = [
            "Single Left Click - Add node / Select Node",
            "Single Right Click - Select Edge",
            "Double Left Click - Move Node",
            "Double Right Click - Move Edge",
            "",
            "D key - Delete Node/Edge",
            "S key - Save data",
            "L key - Load data",
            "B key - Start BFS at selected node",
            "N key - Start DFS at selected node",
            "F key - Toggle node Id visibility",
            "github.com/3ddelano/graph-visualizer-python",
        ]

        font_size = 10
        font = ("Arial", font_size, "normal")

        draw_pos = [0, 16]
        tur.penup()
        tur.color("#fff")
        for line in main_lines:
            tur.goto(draw_pos[0], draw_pos[1])
            tur.write(line, font=font)
            draw_pos[1] += font_size + 10

        if not self.help_visible:
            return

        for line in lines:
            tur.goto(draw_pos[0], draw_pos[1])
            tur.write(line, font=font)

            draw_pos[1] += font_size + 10

    def onbfsstart(self):
        # Check if a node is selected
        if not self.selected_node:
            print("No node is selected for BFS")
            return

        # Start bfs from the selected node
        print("Starting BFS at node id=", self.selected_node.id)
        self.animation = BFSAnimation(self)
        self.animation.set_start_node(self.selected_node)
        self.deselect_nodes()

    def ondfsstart(self):
        # Check if a node is selected
        if not self.selected_node:
            print("No node is selected for DFS")
            return

        # Start dfs from the selected node
        print("Starting DFS at node id=", self.selected_node.id)
        self.animation = DFSAnimation(self)
        self.animation.set_start_node(self.selected_node)
        self.deselect_nodes()

    def onhelptoggle(self):
        self.help_visible = not self.help_visible

    def onnodeidtoggle(self):
        self.node_id_visible = not self.node_id_visible

    def add_node(self, node):
        self.nodes.append(node)

    def delete_node(self, node):
        self.nodes.remove(node)

    def add_edge(self, edge):
        self.edges.append(edge)

    def delete_edge(self, edge):
        self.edges.remove(edge)
