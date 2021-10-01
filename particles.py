import pygame
import random
from pygame import colordict


# direction of the bullet, if the bullet shoots right, the particles should move on the right side of x axis

class Particle:
    def __init__(self, game, x, y):
        self.game = game
        self.x = x
        self.y = y
        self.radius = random.randint(3, 8)
        self.direction = 1
        self.color = (255, 0, 0)
        # self.color = [(227,207,87), (255,64,64), (139,35,35), (255,97,3), (255,185,15), (255,215,0),(255,246,143), (238,238,0)]

    def update(self):
        self.x += random.randint(-1, 1)
        self.y += random.randint(-1, 1)
        self.radius -= 0.20
        pygame.draw.circle(self.game.screen, self.color, (self.x, self.y), self.radius)
        ##########DEALING WITH SMALL PARTICLES##############
        if self.radius <= 0:
            self.game.particles.remove(self)
