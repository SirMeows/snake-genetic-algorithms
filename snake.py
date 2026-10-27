import random
from collections import deque
from typing import Protocol
import pygame
from vector import Vector
from game_controller import HumanController
import math

class SnakeGame:
    def __init__(self, xsize: int=30, ysize: int=15, scale: int=17):
        self.grid = Vector(xsize, ysize)
        self.scale = scale
        self.snake = Snake(game=self)
        self.food = Food(game=self)

    def run(self):
        running = True
        while running:
            next_move = self.controller.update()
            if next_move: self.snake.v = next_move
            self.snake.move()
            if not self.snake.p.within(self.grid):
                running = False
                message = 'Game over! You crashed into the wall!'
            if self.snake.cross_own_tail:
                running = False
                message = 'Game over! You hit your own tail!'
            if self.snake.p == self.food.p:
                self.snake.add_apple()
                self.food = Food(game=self)
            if self.snake.moves_without_apple > 150:
                running = False
                message = 'Game over! You did not eat an apple for 100 moves!'
        print(f'{message} ... : Score: {self.snake.apples}, Moves: {self.snake.moves}')


class Food:
    def __init__(self, game: SnakeGame):
        self.game = game
        self.p = Vector.random_within(self.game.grid)


class Snake:
    def __init__(self, *, game: SnakeGame):
        self.game = game
        self.apples = 0
        self.moves = 0
        self.moves_without_apple = 0
        self.v = Vector(0, 0)
        self.body = deque()
        self.body.append(Vector.random_within(self.game.grid))

    def move(self):
        self.p = self.p + self.v
        self.moves += 1
        self.moves_without_apple += 1

    @property
    def cross_own_tail(self):
        try:
            self.body.index(self.p, 1)
            return True
        except ValueError:
            return False

    @property
    def p(self):
        return self.body[0]

    @p.setter
    def p(self, value):
        self.body.appendleft(value)
        self.body.pop()

    def add_apple(self):
        self.apples += 1
        self.moves_without_apple = 0
        tail = self.body.pop()
        self.body.append(tail)
        self.body.append(tail)

    def debug(self):
        print('===')
        for i in self.body:
            print(str(i))

    def fitness(self):
        try:
            return self.apples / math.log2(self.moves)
        except:
            return 0


