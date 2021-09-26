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
    def __init__(self, game, speed, max_hp, color, name, *groups):
        super().__init__(*groups)
        self.name = name
        self.game = game
        self.max_hp = max_hp
        self.hp = self.max_hp
        self.color = color
        enemy_side = self.set_side()
        self.image = pygame.Surface((enemy_side, enemy_side))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.spawn()
        self.speed = speed
        self.velocity = [0, 0]
        self.old_velocity = [0, 0]
        self.priority = 100

    def set_side(self):
        enemy_side = self.max_hp / 10
        return enemy_side

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
            health_rect = pygame.Rect(0, 0, 20, 5)
            health_rect.midbottom = self.rect.centerx, self.rect.top
            draw_health_bar(surf, health_rect.topleft, health_rect.size,
                            (0, 0, 0), (255, 0, 0), (0, 255, 0), self.hp / self.max_hp)


class EnemySlow(Enemy):
    def __init__(self, game, speed, max_hp, color, name, *groups):
        super().__init__(game, speed, max_hp, color, name, *groups)

    def move(self, dtick):
        self.old_velocity = self.velocity
        self.velocity[0] = random.randint(-(self.max_hp-self.hp), (self.max_hp-self.hp)) / 200
        self.velocity[1] = random.randint(-(self.max_hp-self.hp), (self.max_hp-self.hp)) / 200

    def set_side(self):
        enemy_side = int(self.hp / 10)
        return enemy_side

    def update_size(self):
        pos_x = self.rect.x
        pos_y = self.rect.y
        self.image = pygame.transform.smoothscale(self.image, (self.set_side(), self.set_side()))
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y

    def update(self):
        self.update_size()
        self.rect.move_ip(*self.velocity)
