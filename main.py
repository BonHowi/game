import random

import pygame
from pygame.sprite import collide_rect

successes, failures = pygame.init()
print(f"Initializing pygame: {successes} successes and {failures} failures.")

FPS = 60
SIZE = (1200, 600)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BROWN = (185, 100, 0)
KATANA_COLOR = (169, 169, 169)

# pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 15)


# class Screen(pygame.sprite.Sprite):
#     def __init__(self, *groups):
#         super().__init__(*groups)
#         self.image = pygame.Surface(SIZE)
#         self.image.fill(BLACK)
#         self.rect = self.image.get_rect()  # Get rect of some size as 'image'.
#         self.priority = 0

class Weapon(pygame.sprite.Sprite):
    def __init__(self, damage, name, width, color, x, y, *groups):
        super().__init__(*groups)
        self.width = width
        self.damage = damage
        self.name = name
        self.blade_length = int(width)
        self.color = color
        self.image = pygame.Surface((20, 20))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def collision(self, collision_obj):
        if self.rect.colliderect(collision_obj.rect):
            collision_obj.assign_weapon(self)  # if collided, assigning weapon to player


class Player(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.image = pygame.Surface((10, 10))
        self.image.fill(BROWN)
        self.rect = self.image.get_rect()  # Get rect of some size as 'image'.
        self.rect.x = SIZE[0] / 2
        self.rect.y = SIZE[1] / 2
        self.velocity = [0, 0]
        self.old_velocity = [0, 0]
        self.speed = 100
        self.priority = 1000
        self.score = 0
        # Player Attacking
        self.direction = ''
        self.attacking = False
        self.attack_range = pygame.Rect(0, 0, 0, 0)
        self.hasWeapon = False
        self.weapon = Weapon(0, 'Gole piesci', 2, RED, 35000, 50000, all_sprites)
        self.hp = 100

    def attack(self, collision_obj):
        if self.attacking and self.hasWeapon:
            if self.direction == 'RIGHT':
                self.attack_range = pygame.Rect(self.rect.x + self.rect.width, self.rect.y,
                                                self.weapon.blade_length, self.rect.height)
                self.collision(collision_obj)
            elif self.direction == 'LEFT':
                self.attack_range = pygame.Rect(self.rect.x - self.weapon.blade_length, self.rect.y,
                                                self.weapon.blade_length, self.rect.height)
                self.collision(collision_obj)
            elif self.direction == 'UP':
                self.attack_range = pygame.Rect(self.rect.x, self.rect.y - self.weapon.blade_length, self.rect.height,
                                                self.weapon.blade_length)
                self.collision(collision_obj)
            elif self.direction == 'DOWN':
                self.attack_range = pygame.Rect(self.rect.x, self.rect.y + self.rect.height, self.rect.height,
                                                self.weapon.blade_length)
                self.collision(collision_obj)
        else:
            self.attack_range = pygame.Rect(0, 0, 0, 0)

    def collision(self, collision_obj):
        if self.attack_range.colliderect(collision_obj.rect):
            if collision_obj.hp >= 0:
                collision_obj.hp -= self.weapon.damage
            else:
                if collision_obj in all_sprites:
                    self.score += 1
                    self.image.fill(RED)
                collision_obj.kill()
        else:
            self.image.fill(BROWN)

    def update(self):
        self.rect.move_ip(*self.velocity)

    def render(self, display):
        if self.hasWeapon:
            pygame.draw.rect(display, self.weapon.color, self.attack_range)

    def assign_weapon(self, weapon: Weapon):
        self.weapon = weapon
        self.hasWeapon = True


class Enemy(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.image = pygame.Surface((2, 2))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = SIZE[0] / 2
        self.rect.y = SIZE[1] / 2

        self.velocity = [0, 0]
        self.old_velocity = [0, 0]
        self.priority = 100

        self.max_hp = 150
        self.hp = self.max_hp

    def update(self):
        self.rect.move_ip(*self.velocity)

    def move(self, dtick):
        self.old_velocity = self.velocity
        self.velocity[0] = random.randint(-150, 150) * dtick / 2
        self.velocity[1] = random.randint(-150, 150) * dtick / 2

    def collision(self, collided):
        if self.rect.colliderect(collided):
            self.image.fill(RED)

    def draw_health(self, surf):
        health_rect = pygame.Rect(0, 0, 15, self.image.get_width() + 1)
        health_rect.midbottom = self.rect.centerx, self.rect.top
        draw_health_bar(surf, health_rect.topleft, health_rect.size,
                        (0, 0, 0), (255, 0, 0), (0, 255, 0), self.hp / self.max_hp)


class Wall(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        if random.randint(1, 2) % 2:
            wall = (random.randint(40, 100), random.randint(1, 10))
        else:
            wall = (random.randint(1, 10), random.randint(40, 200))
        self.image = pygame.Surface(wall)
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        x = random.randint(100, SIZE[0] - 100)
        y = random.randint(100, SIZE[1] - 100)
        self.rect.x = x
        self.rect.y = y


class FPSCounter:
    def __init__(self, surface, font, cock, color, pos):
        self.surface = surface
        self.font = font
        self.clock = cock
        self.pos = pos
        self.color = color

        self.fps_text = self.font.render(str(int(60)) + "FPS", False, self.color)
        self.fps_text_rect = self.fps_text.get_rect(center=(self.pos[0], self.pos[1]))

    def render(self):
        self.surface.blit(self.fps_text, self.fps_text_rect)

    def update(self):
        text = f"{60:2.0f} FPS"
        self.fps_text = self.font.render(text, False, self.color)
        self.fps_text_rect = self.fps_text.get_rect(center=(self.pos[0], self.pos[1]))


class PlayerInfo:
    def __init__(self, surface, font, cock, color, pos):
        self.surface = surface
        self.font = font
        self.clock = cock
        self.pos = pos
        self.color = color
        self.space_between = 20

        self.hp_text = self.font.render("HP: " + str(player.hp), False, self.color)
        self.weapon_text = self.font.render("Weapon: " + str(player.weapon.name), False, self.color)
        self.damage_text = self.font.render("Damage: " + str(player.weapon.damage), False, self.color)

        self.hp_text_rect = self.weapon_text.get_rect(center=(self.pos[0], self.pos[1]))
        self.weapon_text_rect = self.weapon_text.get_rect(center=(self.pos[0], self.pos[1] + self.space_between))
        self.damage_text_rect = self.weapon_text.get_rect(center=(self.pos[0], self.pos[1] + 2 * self.space_between))

    def render(self):
        self.surface.blit(self.hp_text, self.hp_text_rect)
        self.surface.blit(self.weapon_text, self.weapon_text_rect)
        self.surface.blit(self.damage_text, self.damage_text_rect)

    def update(self):
        text = "Weapon: " + str(player.weapon.name)
        self.weapon_text = self.font.render(text, False, self.color)
        self.weapon_text_rect = self.weapon_text.get_rect(center=(self.pos[0], self.pos[1]))


def draw_health_bar(surf, pos, size, border_c, back_c, health_c, progress):
    pygame.draw.rect(surf, back_c, (*pos, *size))
    pygame.draw.rect(surf, border_c, (*pos, *size), 1)
    inner_pos = (pos[0] + 1, pos[1] + 1)
    inner_size = ((size[0] - 2) * progress, size[1] - 2)
    rect = (round(inner_pos[0]), round(inner_pos[1]), round(inner_size[0]), round(inner_size[1]))
    pygame.draw.rect(surf, health_c, rect)


all_sprites = pygame.sprite.Group()
# screen = Screen(all_sprites)
player = Player(all_sprites)
# assigning weapon
sword = Weapon(15, 'Sword', 15, RED, 200, 50, all_sprites)
katana = Weapon(25, 'Katana', 36, KATANA_COLOR, 250, 50, all_sprites)
kij = Weapon(1, 'Kij', 5, BLUE, 300, 50, all_sprites)

# player.assign_weapon(sword)

wall_list = []
for _ in range(random.randint(10, 30)):
    wall_list.append(Wall(all_sprites))

enemy_list = []
for _ in range(1000):
    enemy_list.append(Enemy(all_sprites))

running = True
while running:
    screen = pygame.display.set_mode(SIZE)
    clock = pygame.time.Clock()
    screen_rect = screen.get_rect()
    fps_counter = FPSCounter(screen, myfont, clock, GREEN, (150, 10))
    player_info = PlayerInfo(screen, myfont, clock, GREEN, (800, 10))

    dt = clock.tick(FPS) / 400  # Returns milliseconds between each call to 'tick'. The convert time to seconds.
    screen.fill(BLACK)  # Fill the screen with background color.
    player.old_velocity = player.velocity
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                player.direction = 'UP'
                player.velocity[1] = -player.speed * dt
            elif event.key == pygame.K_s:
                player.direction = 'DOWN'
                player.velocity[1] = player.speed * dt
            elif event.key == pygame.K_a:
                player.direction = 'LEFT'
                player.velocity[0] = -player.speed * dt
            elif event.key == pygame.K_d:
                player.direction = 'RIGHT'
                player.velocity[0] = player.speed * dt
            elif event.key == pygame.K_SPACE:
                player.image.fill(RED)
                player.attacking = True

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_w or event.key == pygame.K_s:
                player.velocity[1] = 0
            elif event.key == pygame.K_a or event.key == pygame.K_d:
                player.velocity[0] = 0
            elif event.key == pygame.K_SPACE:
                player.image.fill(BROWN)
                player.attacking = False

    player.rect.clamp_ip(screen_rect)

    coordinates = myfont.render('SCORE: ' + str(player.score), False, (255, 0, 0))

    for enemy in enemy_list:
        enemy.move(dt)
        player.attack(enemy)

        enemy.rect.clamp_ip(screen_rect)
        if enemy.hp > 0:
            enemy.draw_health(screen)

    sword.collision(player)
    katana.collision(player)
    kij.collision(player)

    all_sprites.update()
    for block in wall_list:
        if collide_rect(player, block):
            velocity = [i * (-1) for i in player.old_velocity]
            player.velocity = velocity
            player.update()
            player.velocity = [0, 0]
        for enemy in enemy_list:
            if collide_rect(enemy, block):
                velocity_en = [i * (-1) for i in enemy.old_velocity]
                enemy.velocity = velocity_en
                enemy.update()
                enemy.velocity = [0, 0]

    player.render(screen)

    fps_counter.update()
    fps_counter.render()
    # player_info.update() i think, niepotrzebne
    player_info.render()

    screen.blit(coordinates, (0, 0))

    all_sprites.draw(screen)
    pygame.display.update()

print("Exited the game loop. Game will quit...")
quit()
