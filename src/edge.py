# Graph Visualizer
# 27 Jan 2021
# Group 2 - CSE1014 Lab

from math import sqrt


EDGE_SIZE = 12
NORMAL_COLOR = "#bbb"
SELECTED_COLOR = "#f00"
DRAGGING_COLOR = "#ff0"


class Edge:
    _id = 0

    def __init__(self, *args):
        if len(args) == 2:
            # args = [nodeA_id, nodeB_id]
            # Give a unique id
            self.id = Edge._id
            Edge._id += 1

            self.nodeA = args[0]
            self.nodeB = args[1]
        else:
            # args = [id, nodeA_id, nodeB_id]
            self.id = args[0]
            self.nodeA = args[1]
            self.nodeB = args[2]
            Edge._id = self.id + 1  # For the next edge

        self.is_selected = False
        self.is_dragging = False

    def is_clicked(self, x, y):
        denominator = self.nodeB.pos[0] - self.nodeA.pos[0]
        if denominator == 0:
            denominator = 0.00001
        slope = (self.nodeB.pos[1] - self.nodeA.pos[1]) / denominator
        A = slope
        B = -1
        C = self.nodeA.pos[1] - slope * self.nodeA.pos[0]

        center = [(self.nodeA.pos[0] + self.nodeB.pos[0]) * 0.5,
                  (self.nodeA.pos[1] + self.nodeB.pos[1]) * 0.5]

        dist_from_center = sqrt((x - center[0])**2 + (y - center[1])**2)
        dist_from_line = abs(A * x + B * y + C) / sqrt(A * A + B * B)

        length = sqrt((self.nodeB.pos[0] - self.nodeA.pos[0])
                      ** 2 + (self.nodeB.pos[1] - self.nodeA.pos[1]) ** 2)
        if dist_from_line <= EDGE_SIZE * 0.5 and dist_from_center <= length * 0.5:
            return True
        else:
            return False

    def draw(self, tur, color=NORMAL_COLOR):
        tur.penup()

        if self.is_selected:
            color = SELECTED_COLOR
        elif self.is_dragging:
            color = DRAGGING_COLOR
        tur.color(color)

        tur.pensize(EDGE_SIZE)
        # Goto nodeA's position
        tur.goto(self.nodeA.pos[0], self.nodeA.pos[1])
        tur.pendown()
        # Goto nodeB's position
        tur.goto(self.nodeB.pos[0], self.nodeB.pos[1])
        tur.penup()
