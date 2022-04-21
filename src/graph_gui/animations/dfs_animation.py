"""
File: dfs_animation.py
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


class DFSAnimation(AnimationInterface):
    def __init__(self, graph):
        self.graph = graph
        self.cur_node = None
        self.start_node = None
        self.stack = []  # used in the algorithm
        self.visited = []  # used in the algorithm and for drawing the visited nodes
        self.edges = []
        self.prev_nodes = []

    def set_start_node(self, node):
        self.cur_node = node

    def is_ended(self):
        return self.cur_node is None and len(self.stack) == 0

    def one_step(self):
        # One step in the DFS algorithm
        if self.cur_node is None:
            return

        # Dfs
        if not self.cur_node in self.visited:
            self.stack.append(self.cur_node)
            self.start_node = self.cur_node

        if len(self.stack) > 0:
            node = self.stack[-1]
            self.stack.pop()

            if not node in self.visited:
                self.cur_node = node
                for visited in self.visited:
                    edge = self.graph.get_edge_between_nodes(visited, node)
                    if edge:
                        self.edges.append(edge)
                        self.prev_nodes.append(node)
                self.visited.append(node)

            for neighbour in self.graph.get_adjacent_nodes(node):
                if not neighbour in self.visited:
                    self.stack.append(neighbour)
        else:
            self.cur_node = None

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
        visited = []
        stack = [self.cur_node]

        while len(stack) > 0:
            node = stack[-1]
            stack.pop()

            if not node.id in visited:
                ret.append(node.id)
                visited.append(node.id)

            for neighbour in self.graph.get_adjacent_nodes(node):
                if not neighbour.id in visited:
                    stack.append(neighbour)

        result_str = " -> ".join([str(i) for i in ret])
        print("DFS result:" + result_str)
        return result_str
