import tkinter as tk
from random import shuffle
import numpy as np
import tkinter.messagebox

__author__ = 'ВЕЛИЧАЙШИЙ ИЗ ЖИВУЩИХ - AITENIR'

"""
ЕСТЬ ШАНС, ЧТО ВЫ ПЕРВЫМ НАЖАТИЕМ ПОПАДЕТЕ В МИНУ
ТАК ЧТО НЕ РЕКОМЕНДУЕТСЯ ДЕЛАТЬ ПЕРВОЕ НАЖАТИЕ ЛЮДЯМ С ПЛОХИМ ЧУТЬЕМ
"""


class Cell:
    def __init__(self, value):
        self.value = value
        self.state = False
        self.is_marked = False

    def __str__(self):
        return self.value

    def __eq__(self, other):
        return self.value == other


class Board:
    WIDTH = 720
    HEIGHT = 720

    def __init__(self, n, m, bomb_number):
        self.n = n
        self.m = m

        self.field = [Cell(0) for _ in range(n*m-bomb_number)] + [Cell(9) for _ in range(bomb_number)]
        shuffle(self.field)

        self.field = np.pad(np.array(self.field).reshape(n, m), pad_width=1, constant_values='*').tolist()

        self.block_width = Board.WIDTH / m
        self.block_height = Board.HEIGHT / n

        root = tk.Tk()
        root.geometry(f'{Board.WIDTH}x{Board.HEIGHT}')

        canvas = tk.Canvas(root, width=Board.WIDTH, height=Board.HEIGHT)
        canvas.bind("<Button-1>", self.click)
        canvas.bind("<Button-2>", self.mark_mine)

        canvas.pack()

        self.root = root
        self.c = canvas

        self.count_mines()
        self.draw()

    def __str__(self):
        return '\n'.join([' '.join([str(self.field[i][j].value) for j in range(1, self.m+1)])
                          for i in range(1, self.n+1)])

    def count_mines(self):
        for i in range(1, self.n+1):
            for j in range(1, self.m+1):
                if self.field[i][j] == 9:
                    continue

                d = [(i, j) for i in (-1, 0, 1) for j in (-1, -0, 1) if i or j]
                adjacent_bomb_number = 0

                for di, dj in d:
                    if self.field[i+di][j+dj] == 9:
                        adjacent_bomb_number += 1

                self.field[i][j].value = adjacent_bomb_number

    def draw(self):
        for i in range(self.n):
            for j in range(self.m):
                c = self.field[i+1][j+1]

                if c.state:
                    text = c.value if c.value else ''
                else:
                    text = '#' if c.is_marked else ''

                self.c.create_rectangle(
                    j * self.block_width,
                    i * self.block_height,
                    self.block_width * (j+1),
                    self.block_height * (i+1),
                    fill='#e6e6e6' if self.field[i+1][j+1].state else 'WHITE',
                    outline='#c4c4c4',
                )
                self.c.create_text(
                    j * self.block_width + self.block_width / 2,
                    i * self.block_height + self.block_height / 2,
                    text=text,
                    fill='orange',
                    font=f'Helvetica {int(self.block_height * 0.8)} bold'
                )

    def click(self, event):
        j, i = int(event.x // self.block_width + 1), int(event.y // self.block_height + 1)
        self.field[i][j].is_marked = False

        if self.field[i][j] == 9:
            tk.messagebox.showinfo(message='You lost')
            self.root.quit()
        else:
            self.field[i][j].state = True
            self.explore(i, j)

        self.draw()

    def explore(self, y, x):
        d = [(i, j) for i in (-1, 0, 1) for j in (-1, -0, 1) if i or j]

        self.field[y][x].state = True

        if self.field[y][x].value in range(1, 9):
            return

        for di, dj in d:
            if type(self.field[y+di][x+dj]) == Cell and not self.field[y+di][x+dj] == 9 and not self.field[y+di][x+dj].state:
                self.explore(y+di, x+dj)

    def mark_mine(self, event):
        j, i = int(event.x // self.block_width + 1), int(event.y // self.block_height + 1)

        if self.field[i][j].state:
            return 0
        self.field[i][j].is_marked = not self.field[i][j].is_marked
        self.draw()


b = Board(20, 20, 50)

b.root.mainloop()
