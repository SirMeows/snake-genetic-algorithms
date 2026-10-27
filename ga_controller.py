from typing import Protocol
from vector import Vector
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'
import pygame
from game_controller import GameController
from ga_models.ga_simple import SimpleModel
from ga_models.ga_crossbreeding import CrossBreedingModel
from ga_models.ga_tournament import TournamentModel
from snake import SnakeGame
import uuid


class GAController(GameController):
    def __init__(self, game, display=False):
        self.uuid = uuid.uuid4()
        self.display = display
        self.game = game
        self.game.controller = self
        self.action_space = (Vector(0, -1), Vector(0, 1), Vector(1, 0), Vector(-1, 0))
        self.model = TournamentModel(dims=(2, 16, 4))

        if self.display:
            pygame.init()
            self.screen = pygame.display.set_mode((game.grid.x * game.scale, game.grid.y * game.scale))
            self.clock = pygame.time.Clock()
            self.color_snake_head = (0, 255, 0)
            self.color_food = (255, 0, 0)
            self.action_space = (Vector(0, -1), Vector(0, 1), Vector(1, 0), Vector(-1, 0))

        

    def __lt__(self, other: GameController) -> bool:
        return self.game.snake.fitness() < other.game.snake.fitness()

    def __eq__(self, other: GameController) -> bool:
        return self.model.DNA == other.model.DNA

    def __del__(self):
        if self.display:
            pygame.quit()

    def update(self) -> Vector:
        # observation space

        # # delta north, east, south, west
        # dn = self.game.snake.p.y
        # de = self.game.grid.x - self.game.snake.p.x
        # ds = self.game.grid.y - self.game.snake.p.y
        # dw = self.game.snake.p.x

        # # delta food x and y
        dfx = self.game.snake.p.x - self.game.food.p.x
        dfy = self.game.snake.p.y - self.game.food.p.y

        if (dfx > 0):
            dfx = 1
        
        if (dfy > 0):
            dfy = 1

        # score
        s = self.game.snake.apples

        obs = (dfx, dfy)

        # original
        # obs = (dn, de, ds, dw, dfx, dfy, s)



        # action space
        next_move = self.action_space[self.model.action(obs)]

        # display
        if self.display:
            self.screen.fill('black')
            for i, p in enumerate(self.game.snake.body):
                pygame.draw.rect(self.screen, (0, max(128, 255 - i * 12), 0), self.block(p))
            pygame.draw.rect(self.screen, self.color_food, self.block(self.game.food.p))
            pygame.display.flip()
            self.clock.tick(20)
        return next_move

    def block(self, obj):
        return (obj.x * self.game.scale,
                obj.y * self.game.scale,
                self.game.scale,
                self.game.scale)
    
    def reset_game(self):
        self.game = SnakeGame()
        self.game.controller = self


    def set_display(self, display: bool, game: SnakeGame):
        self.display = display
        
        if self.display:
            pygame.init()
            self.screen = pygame.display.set_mode((game.grid.x * game.scale, game.grid.y * game.scale))
            self.clock = pygame.time.Clock()
            self.color_snake_head = (0, 255, 0)
            self.color_food = (255, 0, 0)
            self.action_space = (Vector(0, -1), Vector(0, 1), Vector(1, 0), Vector(-1, 0))
