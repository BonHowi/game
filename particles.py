import pygame
import random

class Particle(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.image = pygame.Surface([1, 1])
        self.image.fill(self.game.RED)
        self.rect = self.image.get_rect()
        self.direction = random.choice(['UP', 'DOWN', 'LEFT', 'RIGHT'])
        self.speed = random.randint(1, 10)

    def update(self):
        if self.direction == 'UP':
            self.rect.y -= self.speed
        elif self.direction == 'RIGHT':
            self.rect.x += self.speed
        elif self.direction == 'LEFT':
            self.rect.x -= self.speed
        elif self.direction == 'DOWN':
            self.rect.y += self.speed
