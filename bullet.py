import pygame
import math


class Bullet(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__()
        self.game = game
        self.image = pygame.Surface([3, 3])
        self.image.fill(self.game.WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 5
        self.damage = 10 + self.game.player.score * 5

        mouse = pygame.mouse.get_pos()
        start = pygame.math.Vector2(self.rect.center)
        distance = mouse - start
        position = pygame.math.Vector2(start)
        self.vel = distance.normalize() * self.speed

    def update(self):
        self.rect.x  += self.vel[0]
        self.rect.y  += self.vel[1]


    def collision(self, collision_obj):
        if self.rect.colliderect(collision_obj.rect): #zmienione bullet rect
            self.game.player.calculate_collison(collision_obj, self.damage)
            self.kill()
