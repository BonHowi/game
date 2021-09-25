import pygame
from player import Player
WHITE = (255, 255, 255)

class Bullet(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([4, 10])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.direction = ''
        self.damage = 10
        self.speed = 10

    def update(self):
        if self.direction == 'UP':
            self.rect.y -= self.speed
        elif self.direction == 'RIGHT':
            self.rect.x += self.speed
        elif self.direction == 'LEFT':
            self.rect.x -= self.speed
        elif self.direction == 'DOWN':
            self.rect.y += self.speed

    def collision(self, collision_obj):
        if self.rect.colliderect(collision_obj.rect):
            collision_obj.kill()
            self.kill()
