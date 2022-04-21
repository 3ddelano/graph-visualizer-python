"""
File: node.py
Author: Delano Lourenco
Repo: https://github.com/3ddelano/graph-visualizer-python
License: MIT
"""


class Node:
    _id = 0

    def __init__(self, *args):
        if len(args) == 2:
            # args = [x, y]
            # Give a unique id
            self.id = Node._id
            Node._id += 1

            self.pos = [args[0], args[1]]
        else:
            # args = [id, x, y]
            self.id = args[0]
            self.pos = [args[1], args[2]]
            Node._id = self.id + 1  # For the next node
