"""
File: edge.py
Author: Delano Lourenco
Repo: https://github.com/3ddelano/graph-visualizer-python
License: MIT
"""


class Edge:
    _id = 0

    def __init__(self, *args):
        if len(args) <= 3:
            # args = [nodeA, nodeB, weigth?]
            # Give a unique id
            self.id = Edge._id
            Edge._id += 1

            self.nodeA = args[0]
            self.nodeB = args[1]
            if len(args) >= 3:
                self.weight = float(args[2])
            else:
                self.weight = 1.0
        else:
            # args = [id, nodeA, nodeB, weight]
            self.id = args[0]
            self.nodeA = args[1]
            self.nodeB = args[2]
            Edge._id = self.id + 1  # For the next edge
            self.weight = args[3]
