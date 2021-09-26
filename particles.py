import pygame
import random

class Particle():
    def __init__(self, game, x, y):
        super().__init__()
        self.game = game
        self.x = x
        self.y = y
        self.radius = random.randint(10, 14)

    def update(self):
        self.x += random.randint(-1, 1) 
        self.y += random.randint(-1, 1)
        self.radius -= 0.1
        pygame.draw.circle(self.game.screen, random.choice(self.game.color), (self.x, self.y), self.radius)
        ##########DEALING WITH SMALL PARTICLES##############
        # if self.radius <= 0:
        #     self.particles.remove(self)
