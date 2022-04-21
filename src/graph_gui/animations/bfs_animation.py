"""
File: bfs_animation.py
Author: Delano Lourenco
Repo: https://github.com/3ddelano/graph-visualizer-python
License: MIT
"""

from ..constants import (
    CURRENT_EDGE_COLOR,
    CURRENT_NODE_COLOR,
    SEEN_EDGE_COLOR,
    SEEN_NODE_COLOR,
    START_NODE_COLOR,
)
from ..interfaces.animation_interface import AnimationInterface


class BFSAnimation(AnimationInterface):
    def __init__(self, graph):
        self.graph = graph
        self.start_node = None
        self.queue = []
        self.visited = []  # used in the algorithm and for drawing the visited nodes
        self.edges = []
        self.prev_nodes = []

    def set_start_node(self, node):
        self.start_node = node
        self.queue = [node]

    def is_ended(self):
        return len(self.queue) == 0

    def one_step(self):
        # One step in the BFS algorithm

        if self.start_node is None:
            return

        if len(self.queue) > 0:
            node = self.queue.pop(0)

            self.visited.append(node)

            # Get the path from startnode to node
            for visited_node in self.visited:
                edge = self.graph.get_edge_between_nodes(visited_node, node)
                if edge:
                    self.edges.append(edge)
                    self.prev_nodes.append(node)
                    break

            for adj_node in self.graph.get_adjacent_nodes(node):
                if not adj_node in self.visited:
                    self.queue.append(adj_node)
                    self.visited.append(adj_node)
        else:
            # BFS Ended
            self.start_node = None

    def get_drawn_nodes(self):
        ret = []

        if self.start_node:
            ret.append({"node": self.start_node, "color": START_NODE_COLOR})

        length = len(self.prev_nodes)
        if length > 1:
            for i in range(length - 1):
                ret.append({"node": self.prev_nodes[i], "color": SEEN_NODE_COLOR})

        if length > 0:
            ret.append({"node": self.prev_nodes[-1], "color": CURRENT_NODE_COLOR})

        return ret

    def get_drawn_edges(self):
        ret = []

        length = len(self.edges)
        if length > 1:
            for i in range(length - 1):
                ret.append({"edge": self.edges[i], "color": SEEN_EDGE_COLOR})

        if length > 0:
            ret.append({"edge": self.edges[-1], "color": CURRENT_EDGE_COLOR})

        return ret

    def get_result_string(self):
        ret = []

        queue = [self.start_node]
        visited = []

        while len(queue) > 0:
            node = queue.pop(0)
            visited.append(node.id)

            ret.append(node.id)

            for adj_node in self.graph.get_adjacent_nodes(node):
                if not adj_node.id in visited:
                    queue.append(adj_node)
                    visited.append(adj_node.id)

        result_str = " -> ".join([str(i) for i in ret])
        print("BFS result:" + result_str)
        return result_str
