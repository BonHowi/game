import pygame
import random


class DustParticle():#w playerze if moving == True, spawn particle
    def __init__(self, game, x, y):
        super().__init__()
        self.game = game
        self.x = x
        self.y = y
        self.radius = random.randint(3, 18)
        self.direction = 1
        self.color = (191, 182, 182)

    def update(self):
        self.x += random.randint(-1, 1)
        self.y += random.randint(-1, 1)
        self.radius -= self.radius/20#min(0.2, self.radius/2)
        pygame.draw.circle(self.game.screen, self.color, (self.x, self.y), self.radius)
        ##########DEALING WITH SMALL PARTICLES##############
        if self.radius <= 0.1:
            self.game.particles.remove(self)
