import random
import pygame
import math

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
        self.animation_database = {"LEFT_WALK": [],
                                   "RIGHT_WALK": []
                                   }

        self.player_index = 0
        self.game = game
        self.max_hp = max_hp
        self.hp = self.max_hp
        self.color = color
        enemy_side = int(self.set_side())
        self.image_size = (5*enemy_side, 5*enemy_side)
        self.image = pygame.image.load("goblin/idle/lIdle_0.png")
        self.image = pygame.transform.scale(self.image, self.image_size)
        self.rect = self.image.get_rect()
        self.spawn()
        self.speed = speed
        self.velocity = [0, 0]
        self.old_velocity = [0, 0]
        self.priority = 100
        self.step = 400
        self.load_animation('goblin/walk')
        self.hitbox = pygame.Rect(self.rect.x + 18, self.rect.y + 27, 40, 48)

    def load_animation(self, path):
        animation_name = path.split('/')[-1]
        for _ in range(4):
            image_loc = animation_name + "_left" + str(_) + ".png"
            animation_image = pygame.image.load(path + '/' + image_loc).convert()
            animation_image = pygame.transform.scale(animation_image, self.image_size)
            self.animation_database["LEFT_WALK"].append(animation_image)
        for _ in range(4):
            image_loc = animation_name + "_right" + str(_) + ".png"
            animation_image = pygame.image.load(path + '/' + image_loc).convert()
            animation_image = pygame.transform.scale(animation_image, self.image_size)
            self.animation_database["RIGHT_WALK"].append(animation_image)

    def animation(self):

        self.player_index += 0.07 # how fast animation changes
        if self.player_index >= 4:
            self.player_index = 0

        self.image = self.animation_database["LEFT_WALK"][int(self.player_index)]



    def set_side(self):
        enemy_side = self.max_hp / 10
        return enemy_side

    def spawn(self):
        spawned = False
        while not spawned:
            spawn_point = self.game.map.spawn_points[random.randint(0, len(self.game.map.spawn_points) - 1)]
            if spawn_point[1]:
                spawn_point_y = spawn_point[0]
                spawn_point_x = spawn_point[1][random.randint(0, len(spawn_point[1]) - 1)]
                self.rect.x = spawn_point_x
                self.rect.y = spawn_point_y
                spawned = True

    def update(self):
        self.animation()
        self.rect.move_ip(*self.velocity)
       # pygame.draw.rect(self.game.screen, (255, 0,0), self.rect, width=1)
        self.hitbox = pygame.Rect(self.rect.x + 19, self.rect.y + 23, 37, 52)

        # pygame.draw.rect(self.game.screen, (255, 0, 0), self.rect, 1)
        pygame.draw.rect(self.game.screen, (255, 0, 0), self.hitbox)

    def move(self, dtick):
        threshold = random.randrange(1, 20)
        if self.step >= threshold:
            self.old_velocity = self.velocity

            #self.velocity[0] = random.randint(-self.speed, self.speed) * dtick
            #self.velocity[1] = random.randint(-self.speed, self.speed) * dtick
            self.move_towards_player(self.game.player, dtick)
            self.step = 0
            # self.find_target(dtick, self.game.player)
        self.step += 1

    def move_towards_player(self, player, dtick):
        # Find direction vector (dx, dy) between enemy and player.
        dirvect = pygame.math.Vector2(player.rect.x - self.rect.x,
                                      player.rect.y - self.rect.y)
        if dirvect.length_squared() > 0:
            dirvect.normalize()
        # Move along this normalized vector towards the player at current speed.
            dirvect.scale_to_length(self.speed * 3 * dtick)
        self.rect.move_ip(dirvect)

    def find_target(self, dtick, target):
        dist_to_target_x = target.rect.x - self.rect.x
        dist_to_target_y = target.rect.x - self.rect.y

        self.velocity[0] = dist_to_target_x / self.speed * dtick * 10
        self.velocity[1] = dist_to_target_y / self.speed * dtick * 10

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
        self.velocity[0] = random.randint(-(self.max_hp - self.hp), (self.max_hp - self.hp)) / 200
        self.velocity[1] = random.randint(-(self.max_hp - self.hp), (self.max_hp - self.hp)) / 200

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
