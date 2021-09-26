import pygame
import random
from player_dust import DustParticle

class RainParticle():
    def __init__(self, game, x, y):
        super().__init__()
        self.game = game
        self.length = random.randint(3, 18)
        self.x = x
        self.y = y
        self.color = (104 - self.length*5, 166 - self.length*8, 238 - self.length*10)
    def update(self):
        self.y += 1/ self.length * 15
        pygame.draw.line(self.game.screen, self.color, (self.x, self.y), (self.x, self.y + self.length))
        if self.y > self.game.SIZE[1] - 5:
            self.game.particles.remove(self)
            self.game.particles.append(DustParticle(self.game, self.x, self.y))


