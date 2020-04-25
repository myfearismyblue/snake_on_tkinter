from random import randrange as rnd, choice
import tkinter as tk
from collections import deque
import math as m
from random import randrange
import time
from global_vars import *


def main():
    global root, canvas

    root = tk.Tk()
    root.geometry(str(CANVAS_WIDTH) + 'x' + str(CANVAS_HEIGHT))
    canvas = tk.Canvas(root, background=CANVAS_BACKGROUND_COLOR)
    canvas.focus_set()

    grid, snake, food, directions_queue = init_game_objects()
    canvas.bind('<Key>', lambda event: key_handler(event, snake, directions_queue))
    canvas.pack(fill=tk.BOTH, expand=1)
    tick(grid, snake, food, directions_queue)
    root.mainloop()


def init_game_objects():
    grid = Grid(canvas)
    snake = Snake(grid)
    food = Food(snake, grid)
    directions_queue = deque()
    return grid, snake, food, directions_queue


def tick(grid, snake, food, directions_queue):
    """Moves and reshows everything on canvas."""
    check_collision(snake, grid)
    if snake.alive:
        snake.eat(grid, food)
        snake.move(grid, directions_queue)
        snake.show(grid)
    if food.alive:
        food.move(grid)
        food.show(grid)
    else:
        food = Food(snake, grid)

    root.after(TIME_REFRESH, tick, grid, snake, food, directions_queue)


def key_handler(event, snake, directions_queue):
    """If corresponding key have been pressed and direction is not opposite to the key"""
    if event.keysym == 'a' or event.keysym == 'Left' and snake.direction != 'right':
        directions_queue.append('left')
    elif event.keysym == 'd' or event.keysym == 'Right' and snake.direction != 'left':
        directions_queue.append('right')
    elif event.keysym == 's' or event.keysym == 'Down' and snake.direction != 'up':
        directions_queue.append('down')
    elif event.keysym == 'w' or event.keysym == 'Up' and snake.direction != 'down':
        directions_queue.append('up')
    elif event.keysym == 'space':
        pass


def check_collision(snake, grid):
    """Gets current head position and checks if next square is a part of body or in range of canvas """
    current_head_pos = [key for key, value in grid.mash.items() if value == snake.body[0]][0]
    current_head_pos_x = current_head_pos[0]
    current_head_pos_y = current_head_pos[1]

    if snake.direction == 'left':
        if current_head_pos_x - 1 < 0 or \
                is_square_in_snake(snake, grid, current_head_pos_x - 1, current_head_pos_y):
            game_over(snake, grid)
    elif snake.direction == 'right':
        if current_head_pos_x + 1 > GRID_WIDTH - 1 or \
                is_square_in_snake(snake, grid, current_head_pos_x + 1, current_head_pos_y):
            game_over(snake, grid)
    elif snake.direction == 'up':
        if current_head_pos_y - 1 < 0 or \
                is_square_in_snake(snake, grid, current_head_pos_x, current_head_pos_y - 1):
            game_over(snake, grid)
    elif snake.direction == 'down':
        if current_head_pos_y + 1 > GRID_HEIGHT - 1 or \
                is_square_in_snake(snake, grid, current_head_pos_x, current_head_pos_y + 1):
            game_over(snake, grid)


def is_square_in_snake(snake, grid, x, y):
    if grid.mash[(x, y)] in snake.body:
        return True
    return False


def game_over(snake, grid):
    global canvas
    canvas.create_text(CANVAS_WIDTH // 2, CANVAS_HEIGHT // 2, text="Game Over", font="Arial 36")
    snake.die(grid)


class Grid:
    def __init__(self, canvas):
        """Creates grid on canvas - the field for snake"""
        self.mash = dict()
        self.color = GRID_COLOR
        bar_width = ((CANVAS_WIDTH - 1) / GRID_WIDTH)    # two pixels to represent border
        bar_height = ((CANVAS_HEIGHT - 1) / GRID_HEIGHT)
        for j in range(GRID_HEIGHT):
            for i in range(GRID_WIDTH):  # FIXME: fix borders offset
                self.mash[(i, j)] = canvas.create_rectangle(2 + bar_width * i, 2 + bar_height * j,
                                                            2 + bar_width * (i + 1), 2 + bar_height * (j + 1))
                canvas.itemconfig(self.mash[(i, j)], fill=self.color)


class Snake:
    def __init__(self, grid):
        """Creates the snake with initial length, but less then a half of the grid width.
        Places it on a half of grid height. makes initial moving direction left
        """
        self.alive = True
        self.length = min(SNAKE_INIT_LENGTH, GRID_WIDTH // 2 - 1)
        self.body = deque()
        self.body_color = SNAKE_BODY_COLOR
        self.head_color = SNAKE_HEAD_COLOR
        self.dead_color = SNAKE_DEAD_COLOR
        for i in range(GRID_WIDTH // 2 - 1, GRID_WIDTH // 2 - 1 + self.length):
            self.body.append(grid.mash[i, (GRID_HEIGHT // 2)])
        self.head = self.body[0]
        self.last_square_not_in_the_body = grid.mash[GRID_WIDTH // 2 + self.length, (GRID_HEIGHT // 2)]
        self.direction = 'left'

    def move(self, grid, directions_queue):
        """Moves the snake in the direction self.direction"""
        if self.alive:
            if directions_queue:
                self.direction = directions_queue.pop()
            def _shift_the_body(self, grid, x, dx, y, dy):
                """Shifts snake's body by poping out tale and appending canvas cell in  the direction dx dy"""
                self.body.appendleft(grid.mash[x + dx, y + dy])
                self.head = self.body[0]
                self.last_square_not_in_the_body = self.body.pop()

            current_head_pos = [key for key, value in grid.mash.items() if value == self.body[0]][0]
            current_head_pos_x = current_head_pos[0]
            current_head_pos_y = current_head_pos[1]

            if self.direction == 'left':
                _shift_the_body(self, grid, current_head_pos_x, -1, current_head_pos_y, 0)
            elif self.direction == 'right':
                _shift_the_body(self, grid, current_head_pos_x, +1, current_head_pos_y, 0)
            elif self.direction == 'up':
                _shift_the_body(self, grid, current_head_pos_x, 0, current_head_pos_y, -1)
            elif self.direction == 'down':
                _shift_the_body(self, grid, current_head_pos_x, 0, current_head_pos_y, +1)

    def eat(self, grid, food):
        if self.alive:
            def _eat_food(self, grid, food, x, dx, y, dy):
                if food.x == x + dx and food.y == y + dy:
                    self.body.appendleft(grid.mash[x + dx, y + dy])
                    self.head = self.body[0]
                    self.length = len(self.body)
                    food.die()
                    print(self.length)

            current_head_pos = [key for key, value in grid.mash.items() if value == self.body[0]][0]
            current_head_pos_x = current_head_pos[0]
            current_head_pos_y = current_head_pos[1]

            if self.direction == 'left':
                _eat_food(self, grid, food, current_head_pos_x, -1, current_head_pos_y, 0)
            elif self.direction == 'right':
                _eat_food(self, grid, food, current_head_pos_x, +1, current_head_pos_y, 0)
            elif self.direction == 'up':
                _eat_food(self, grid, food, current_head_pos_x, 0, current_head_pos_y, -1)
            elif self.direction == 'down':
                _eat_food(self, grid, food, current_head_pos_x, 0, current_head_pos_y, +1)

    def show(self, grid):
        """Draw each member of the snake deque"""
        if self.alive:
            canvas.itemconfig(self.last_square_not_in_the_body, fill=grid.color)  # erasing last square
            canvas.itemconfig(self.body[0], fill=self.head_color)  # coloring head
            for i in range(1, self.length):  # coloring body not including the head
                canvas.itemconfig(self.body[i], fill=self.body_color)

    def die(self, grid):
        """Erases the snake, sets snake.alive = False"""
        self.alive = False
        canvas.itemconfig(self.last_square_not_in_the_body, fill=grid.color)  # erasing last square
        canvas.itemconfig(self.body[0], fill=self.dead_color)  # coloring head
        for i in range(1, self.length):  # coloring body not including the head
            canvas.itemconfig(self.body[i], fill=self.dead_color)


class Food:
    def __init__(self, snake, grid):
        self.x = randrange(0, GRID_WIDTH)
        self.y = randrange(0, GRID_HEIGHT)
        while is_square_in_snake(snake, grid, self.x, self.y):
            self.x = randrange(0, GRID_WIDTH)
            self.y = randrange(0, GRID_HEIGHT)
        self.alive = True
        self.color = FOOD_COLOR

    def show(self, grid):
        canvas.itemconfig(grid.mash[(self.x, self.y)], fill=self.color)

    def move(self, grid):
        pass

    def die(self):
        self.alive = False
        self.color = GRID_COLOR


if __name__ == '__main__':
    main()
