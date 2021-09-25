import pygame


class Bullet(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.image = pygame.Surface([3, 3])
        self.image.fill(self.game.WHITE)
        self.rect = self.image.get_rect()
        self.direction = ''
        self.damage = 10
        self.speed = 3

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
            self.game.player.calculate_collison(collision_obj, self.damage)
