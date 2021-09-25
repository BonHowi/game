import pygame


class Bullet(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.image = pygame.Surface([4, 10])
        self.image.fill(self.game.WHITE)
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
            if collision_obj.hp > 0:
                collision_obj.hp -= self.damage
                if collision_obj.hp <= 0:
                    self.game.player.score += 1
