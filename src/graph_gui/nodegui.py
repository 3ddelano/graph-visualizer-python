"""
File: nodegui.py
Author: Delano Lourenco
Repo: https://github.com/3ddelano/graph-visualizer-python
License: MIT
"""

from .graph_data.node import Node
from .interfaces.clickable import Clickable
from .interfaces.drawable import Drawable
from .constants import (
    NODE_SIZE,
    NODE_ID_COLOR,
    NODE_ID_BG_COLOR,
    NODE_NORMAL_COLOR,
    NODE_SELECTED_COLOR,
    NODE_DRAGGING_COLOR,
)


class NodeGUI(Node, Drawable, Clickable):
    def __init__(self, *args):
        self.is_selected = False
        self.is_dragging = False
        super().__init__(*args)

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

    def draw(self, tur, color=NODE_NORMAL_COLOR):
        tur.penup()
        tur.goto(self.pos[0], self.pos[1])
        tur.pendown()

        if color == NODE_NORMAL_COLOR:
            if self.is_selected:
                color = NODE_SELECTED_COLOR
            if self.is_dragging:
                color = NODE_DRAGGING_COLOR

        tur.dot(NODE_SIZE, color)

    def draw_id(self, canvas):
        width = len(str(self.id)) * 8

        canvas.create_rectangle(
            self.pos[0] - width,
            self.pos[1] - 10,
            self.pos[0] + width,
            self.pos[1] + 10,
            fill=NODE_ID_BG_COLOR,
            outline="black",
        )
        text = canvas.create_text(
            self.pos[0],
            self.pos[1],
            text=str(self.id),
            font=("Arial 10 normal"),
            anchor="center",
            justify="center",
            fill=NODE_ID_COLOR,
        )
        coords = canvas.bbox(text)
        # canvas.move(text, -(coords[2] - coords[0]) * 0.5, -3)
