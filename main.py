from random import randrange as rnd, choice
import tkinter as tk
import math as m
import time
from global_vars import *


def main():
    global root, canvas

    root = tk.Tk()
    root.geometry(str(CANVAS_WIDTH) + 'x' + str(CANVAS_HEIGHT))
    canvas = tk.Canvas(root, background=CANVAS_BACKGROUND_COLOR)
    grid, food, snake = init_game_objects()

    canvas.bind('<Button-1>', handler)

    canvas.pack(fill=tk.BOTH, expand=1)

    tick(grid, food, snake)
    root.mainloop()


def init_game_objects():
    grid = create_grid()
    food = create_food()
    snake = create_snake()
    return grid, food, snake


def tick(grid=None, food=None, snake=None):
    """Moves and reshows everything on canvas."""
    global root  # FIXME: make root local
    pass
    root.after(TIME_REFRESH, tick)


def create_grid():
    global canvas
    grid = Grid(canvas)
    return grid


def create_food():
    pass


def create_snake():
    pass


def handler(event):
    pass

class Grid:
    def __init__(self, canvas):
        pass



class Snake:
    def __init__(self):
        self.body = {}


class Food:
    pass





if __name__ == '__main__':
    main()
