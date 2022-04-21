"""
File: edgegui.py
Author: Delano Lourenco
Repo: https://github.com/3ddelano/graph-visualizer-python
License: MIT
"""

from math import sqrt
import tkinter as tk
from .graph_data.edge import Edge
from .interfaces.clickable import Clickable
from .interfaces.drawable import Drawable
from .constants import (
    EDGE_SIZE,
    EDGE_WEIGHT_COLOR,
    EDGE_WEIGHT_BG_COLOR,
    EDGE_NORMAL_COLOR,
    EDGE_SELECTED_COLOR,
    EDGE_DRAGGING_COLOR,
)


class EdgeGUI(Edge, Drawable, Clickable):
    def __init__(self, *args):
        self.is_selected = False
        self.is_dragging = False
        super().__init__(*args)

    def is_clicked(self, x, y):
        denominator = self.nodeB.pos[0] - self.nodeA.pos[0]
        if denominator == 0:
            denominator = 0.00001
        slope = (self.nodeB.pos[1] - self.nodeA.pos[1]) / denominator
        c = self.nodeA.pos[1] - slope * self.nodeA.pos[0]

        center = [
            (self.nodeA.pos[0] + self.nodeB.pos[0]) * 0.5,
            (self.nodeA.pos[1] + self.nodeB.pos[1]) * 0.5,
        ]

        dist_from_center = sqrt((x - center[0]) ** 2 + (y - center[1]) ** 2)
        dist_from_line = abs(slope * x + -1 * y + c) / sqrt(slope * slope + -1 * -1)

        length = sqrt(
            (self.nodeB.pos[0] - self.nodeA.pos[0]) ** 2
            + (self.nodeB.pos[1] - self.nodeA.pos[1]) ** 2
        )
        if dist_from_line <= EDGE_SIZE * 0.5 and dist_from_center <= length * 0.5:
            return True
        else:
            return False

    def draw(self, tur, color=EDGE_NORMAL_COLOR):
        tur.penup()

        if self.is_selected:
            color = EDGE_SELECTED_COLOR
        elif self.is_dragging:
            color = EDGE_DRAGGING_COLOR
        tur.color(color)

        tur.pensize(EDGE_SIZE)
        # Goto nodeA's position
        tur.goto(self.nodeA.pos[0], self.nodeA.pos[1])
        tur.pendown()
        # Goto nodeB's position
        tur.goto(self.nodeB.pos[0], self.nodeB.pos[1])
        tur.penup()

    def draw_weight(self, canvas):
        mid_x = (self.nodeA.pos[0] + self.nodeB.pos[0]) * 0.5
        mid_y = (self.nodeA.pos[1] + self.nodeB.pos[1]) * 0.5
        if self.weight == 1.0:
            return

        # Draw the background for the text
        width = len(str(self.weight)) * 10 * 0.5
        canvas.create_rectangle(
            mid_x - width,
            mid_y - 10,
            mid_x + width,
            mid_y + 10,
            fill=EDGE_WEIGHT_BG_COLOR,
            outline="black",
        )
        # Draw the text
        canvas.create_text(
            mid_x,
            mid_y,
            text=str(self.weight),
            font=("Arial 10 normal"),
            justify=tk.CENTER,
            fill=EDGE_WEIGHT_COLOR,
        )
