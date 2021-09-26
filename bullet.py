import pygame
import math
import random
from particles import Particle

class Bullet(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__()
        self.game = game
        self.bullet_size = 7
        self.image = pygame.Surface([self.bullet_size, self.bullet_size])
        self.image.fill(self.game.WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y  = y
        self.speed = 2
        self.damage = 10 + self.game.player.score * 5

        self.pos = (x, y)

        mx, my = pygame.mouse.get_pos()
        self.dir = (mx - x, my - y)
        length = math.hypot(*self.dir)
        self.dir = (self.dir[0] / length, self.dir[1] / length)

    def update(self):
        self.pos = (self.pos[0] + self.dir[0] * self.speed,
                    self.pos[1] + self.dir[1] * self.speed)

        self.rect.x  = self.pos[0]
        self.rect.y  = self.pos[1]


    def collision(self, collision_obj):
        if self.rect.colliderect(collision_obj.rect):
            self.sparkle()
            self.kill()

    def collision_enemy(self, collision_enemy):
        if self.rect.colliderect(collision_enemy.rect):
            self.game.player.calculate_collison(collision_enemy, self.damage)
            self.sparkle()
            self.kill()

    def sparkle(self):
        for _ in range(random.randint(10, 25)):
            self.game.particles.append(Particle(self.game, self.rect.x, self.rect.y))

