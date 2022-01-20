# Graph Visualizer
# 20 Jan 2021
# Group 2 - CSE1014 Lab

import turtle
from graph import Graph

# The graph
graph = Graph()


def one_step():
    try:
        tur.clear()
        graph.draw(tur)
        screen.update()
        screen.ontimer(one_step, 50)
    except Exception as e:
        print("Exiting program")
        quit()


def onmove(self, fun, add=None):
    if fun is None:
        self.cv.unbind("<Motion>")
    else:
        def eventfun(event):
            fun(self.cv.canvasx(event.x) / self.xscale, -
                self.cv.canvasy(event.y) / self.yscale)
        self.cv.bind("<Motion>", eventfun, add)


# Setup the screen
screen = turtle.Screen()
screen.setup(1280, 720)
screen.setworldcoordinates(0, 720, 1280, 0)
screen.bgcolor("#333333")
screen.title("Graph Visualizer")

turtle.tracer(False)
tur = turtle.Turtle()
tur.speed(0)
tur.hideturtle()

# Events
screen.listen()
turtle.onscreenclick(graph.onleftclick, 1)
turtle.onscreenclick(graph.onrightclick, 3)
onmove(screen, graph.ondrag, 1)
screen.onkey(graph.onsave, "s")
screen.onkey(graph.onload, "l")
screen.onkey(graph.ondelete, "d")
exited = False

# Main loop
print("Graph Visualizer starting...")
one_step()
screen.mainloop()
