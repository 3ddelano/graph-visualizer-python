"""
File: path_animation.py
Author: Delano Lourenco
Repo: https://github.com/3ddelano/graph-visualizer-python
License: MIT
"""

from ..constants import (
    CURRENT_NODE_COLOR,
    SEEN_EDGE_COLOR,
    SEEN_NODE_COLOR,
    START_NODE_COLOR,
    START_EDGE_COLOR,
)
from ..interfaces.animation_interface import AnimationInterface


class PathAnimation(AnimationInterface):
    def __init__(self, graph, start_node, end_node, path, visited_edges):
        self.graph = graph
        self.start_node = start_node
        self.end_node = end_node
        self.path = path
        self.visited = visited_edges

        self.edge_index = 0
        self.path_index = -1
        self.path.pop(0)
        self.max_edge_index = len(self.visited) - 1
        self.max_path_index = len(self.path) - 1

        self.get_result_string()

    def is_ended(self):
        return self.edge_index == self.max_edge_index

    def one_step(self):
        self.edge_index += 1

        cur_node_id = self.visited[self.edge_index][1]
        cur_node_id2 = self.visited[self.edge_index][0]
        if self.path_index + 1 <= self.max_path_index:
            if (cur_node_id == self.path[self.path_index + 1][0]) or (
                cur_node_id2 == self.path[self.path_index + 1][0]
            ):
                self.path_index += 1

    def get_drawn_nodes(self):
        ret = []
        ret.append({"node": self.start_node, "color": START_NODE_COLOR})

        # Draw the nodes in the final path
        for i in range(self.path_index + 1):
            if len(self.path[i]) > 1:
                ret.append({"node": self.path[i][1].nodeA, "color": START_NODE_COLOR})
                ret.append({"node": self.path[i][1].nodeB, "color": START_NODE_COLOR})

        # Draw the nodes in the visited nodes
        for i in range(self.edge_index + 1):
            node = self.graph.get_node_by_id(self.visited[i][0])
            ret.append(
                {
                    "node": node,
                    "color": SEEN_NODE_COLOR
                    if i != self.edge_index
                    else CURRENT_NODE_COLOR,
                }
            )

        return ret

    def get_drawn_edges(self):
        ret = []
        for i in range(self.path_index + 1):
            if len(self.path[i]) > 1:
                ret.append({"edge": self.path[i][1], "color": START_EDGE_COLOR})

        for i in range(self.edge_index + 1):
            ret.append({"edge": self.visited[i][2], "color": SEEN_EDGE_COLOR})

        return ret

    def get_result_string(self):
        path = [self.start_node.id]
        for arr in self.path:
            path.append(arr[0])

        result_str = " -> ".join([str(i) for i in path])
        print("Path result: " + result_str)
        return result_str
