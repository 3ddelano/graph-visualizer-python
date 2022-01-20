# Graph Visualizer
# 20 Jan 2021
# Group 2 - CSE1014 Lab

NODE_SIZE = 24
NORMAL_COLOR = "#fff"
SELECTED_COLOR = "#f00"
DRAGGING_COLOR = "#ff0"


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

        self.is_selected = False
        self.is_dragging = False

    def is_clicked(self, x, y):
        if x < self.pos[0] - NODE_SIZE * 0.5:
            return False
        if x > self.pos[0] + NODE_SIZE * 0.5:
            return False
        if y < self.pos[1] - NODE_SIZE * 0.5:
            return False
        if y > self.pos[1] + NODE_SIZE * 0.5:
            return False
        return True

    def draw(self, tur):
        tur.penup()
        tur.goto(self.pos[0], self.pos[1])
        tur.pendown()

        node_color = NORMAL_COLOR
        if self.is_selected:
            node_color = SELECTED_COLOR
        if self.is_dragging:
            node_color = DRAGGING_COLOR

        tur.dot(NODE_SIZE, node_color)
