"""
File: main.py
Author: Delano Lourenco
Repo: https://github.com/3ddelano/graph-visualizer-python
License: MIT
"""

import turtle
from graph_gui.graphgui import GraphGUI, VERSION
from graph_gui.constants import SCREEN_BG_COLOR
import traceback


def one_step():
    try:
        canvas.delete("all")
        tur.clear()
        graphgui.draw(tur, canvas)
        screen.update()
        screen.ontimer(one_step, 50)
    except Exception as e:
        print(e)
        traceback.print_exc()
        print("Exiting program")
        quit()


def onmove(self, fun, add=None):
    if fun is None:
        self.cv.unbind("<Motion>")
    else:

        def eventfun(event):
            fun(
                self.cv.canvasx(event.x) / self.xscale,
                -self.cv.canvasy(event.y) / self.yscale,
            )

        self.cv.bind("<Motion>", eventfun, add)


# Setup the screen
screen = turtle.Screen()
screen.tracer(False)
screen.setup(1280, 720)
screen.setworldcoordinates(0, 720, 1280, 0)
screen.bgcolor(SCREEN_BG_COLOR)
canvas = screen.getcanvas()

# The graph
graphgui = GraphGUI(canvas)

screen.title(f"Graph Visualizer {VERSION} - 3ddelano")

# turtle.tracer(False)
turtle.tracer(False)
tur = turtle.Turtle()
tur.speed(0)
tur.hideturtle()

# Events
screen.listen()
turtle.onscreenclick(graphgui.on_left_click, 1)
turtle.onscreenclick(graphgui.on_right_click, 3)
onmove(screen, graphgui.ondrag, 1)
screen.onkey(graphgui.on_save, "s")
screen.onkey(graphgui.on_load, "l")
screen.onkey(graphgui.on_delete, "d")
screen.onkey(graphgui.on_bfs_start, "b")
screen.onkey(graphgui.on_dfs_start, "n")
screen.onkey(graphgui.on_help_toggle, "h")
screen.onkey(graphgui.on_nodeid_toggle, "f")
screen.onkey(graphgui.on_update_weight, "w")
exited = False

# Main loop
print("Graph Visualizer starting...")
one_step()
screen.mainloop()
