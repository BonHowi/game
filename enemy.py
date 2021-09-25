import random
import pygame


def draw_health_bar(surf, pos, size, border_c, back_c, health_c, progress):
    pygame.draw.rect(surf, back_c, (*pos, *size))
    pygame.draw.rect(surf, border_c, (*pos, *size), 1)
    inner_pos = (pos[0] + 1, pos[1] + 1)
    inner_size = ((size[0] - 2) * progress, size[1] - 2)
    rect = (round(inner_pos[0]), round(inner_pos[1]), round(inner_size[0]), round(inner_size[1]))
    pygame.draw.rect(surf, health_c, rect)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, *groups):
        super().__init__(*groups)
        self.game = game
        self.image = pygame.Surface((2, 2))
        self.image.fill(self.game.BLUE)
        self.rect = self.image.get_rect()
        self.spawn()
        self.speed = 150
        self.velocity = [0, 0]
        self.old_velocity = [0, 0]
        self.priority = 100
        self.max_hp = 150
        self.hp = self.max_hp

    def spawn(self):
        pos_x = random.randint(1, self.game.SIZE[0])
        pos_y = random.randint(1, self.game.SIZE[1])
        self.rect.x = pos_x
        self.rect.y = pos_y

    def update(self):
        self.rect.move_ip(*self.velocity)

    def move(self, dtick):
        self.old_velocity = self.velocity
        self.velocity[0] = random.randint(-self.speed, self.speed) * dtick / 2
        self.velocity[1] = random.randint(-self.speed, self.speed) * dtick / 2

    def collision(self, collided):
        if self.rect.colliderect(collided):
            self.image.fill(self.game.RED)

    def draw_health(self, surf):
        if self.hp < self.max_hp:
            health_rect = pygame.Rect(0, 0, 15, self.image.get_width() + 1)
            health_rect.midbottom = self.rect.centerx, self.rect.top
            draw_health_bar(surf, health_rect.topleft, health_rect.size,
                            (0, 0, 0), (255, 0, 0), (0, 255, 0), self.hp / self.max_hp)
