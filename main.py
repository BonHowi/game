import random

import pygame

successes, failures = pygame.init()
print(f"Initializing pygame: {successes} successes and {failures} failures.")

FPS = 60
SIZE = (1200, 800)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BROWN = (185, 100, 0)
KATANA_COLOR = (169,169,169)

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
    def __init__(self, damage, name, width, color,x, y,*groups):
        super().__init__(*groups)
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
            collision_obj.assign_weapon(self) # if collided, assigning weapon to player


class Player(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.image = pygame.Surface((20, 20))
        self.image.fill(BROWN)
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()  # Get rect of some size as 'image'.
        self.rect.x = SIZE[0] / 2
        self.rect.y = SIZE[1] / 2
        self.velocity = [0, 0]
        self.priority = 1000
        self.score = 0
        # Player Attacking
        self.direction = ''
        self.attacking = False
        self.attack_range = pygame.Rect(0, 0, 0, 0)
        self.hasWeapon = False

    def attack(self, collision_obj):
        if self.attacking and self.hasWeapon :
            if self.direction == 'RIGHT':
                self.attack_range = pygame.Rect(self.rect.x + self.rect.width, self.rect.y ,
                                                self.weapon.blade_length, self.rect.height)
                self.collision(collision_obj)
            elif self.direction == 'LEFT':
                self.attack_range = pygame.Rect(self.rect.x - self.weapon.blade_length, self.rect.y, self.weapon.blade_length, self.rect.height)
                self.collision(collision_obj)
            elif self.direction == 'UP':
                self.attack_range = pygame.Rect(self.rect.x, self.rect.y - self.weapon.blade_length,  self.rect.height, self.weapon.blade_length)
                self.collision(collision_obj)
            elif self.direction == 'DOWN':
                self.attack_range = pygame.Rect(self.rect.x, self.rect.y + self.rect.height, self.rect.height,self.weapon.blade_length)
                self.collision(collision_obj)
        else:
            self.attack_range = pygame.Rect(0, 0, 0, 0)

    def collision(self, collision_obj):
        if self.attack_range.colliderect(collision_obj.rect):
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
        self.image.set_colorkey(RED)
        self.rect = self.image.get_rect()
        self.velocity = [0, 0]
        self.priority = 100

    def update(self):
        self.rect.move_ip(*self.velocity)

    def move(self, dtick):
        self.velocity[0] = random.randint(-50, 150) * dtick / 2
        self.velocity[1] = random.randint(-50, 150) * dtick / 2

    # def collision(self, collided):
    #     if self.rect.colliderect(collided):
    #         self.image.fill(RED)


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






all_sprites = pygame.sprite.Group()
# screen = Screen(all_sprites)
player = Player(all_sprites)
######assigning weapon
sword = Weapon(15, 'Sword', 15, RED, 200, 50,all_sprites)
katana = Weapon(25, 'Katana', 36, KATANA_COLOR, 250, 50,all_sprites)
kij = Weapon(1, 'Kij', 5, BROWN,300, 50, all_sprites)

#player.assign_weapon(sword)

enemy_list = []
for _ in range(50):
    enemy_list.append(Enemy(all_sprites))

running = True
while running:
    screen = pygame.display.set_mode(SIZE)
    clock = pygame.time.Clock()
    screen_rect = screen.get_rect()
    fps_counter = FPSCounter(screen, myfont, clock, GREEN, (150, 10))
    dt = clock.tick(FPS) / 400  # Returns milliseconds between each call to 'tick'. The convert time to seconds.
    screen.fill(BLACK)  # Fill the screen with background color.

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                player.direction = 'UP'
                player.velocity[1] = -200 * dt
            elif event.key == pygame.K_s:
                player.direction = 'DOWN'
                player.velocity[1] = 200 * dt
            elif event.key == pygame.K_a:
                player.direction = 'LEFT'
                player.velocity[0] = -200 * dt
            elif event.key == pygame.K_d:
                player.direction = 'RIGHT'
                player.velocity[0] = 200 * dt
            elif event.key == pygame.K_SPACE:
                player.attacking = True

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_w or event.key == pygame.K_s:
                player.velocity[1] = 0
            elif event.key == pygame.K_a or event.key == pygame.K_d:
                player.velocity[0] = 0
            elif event.key == pygame.K_SPACE:
                player.attacking = False

    player.rect.clamp_ip(screen_rect)

    coordinates = myfont.render('SCORE: ' + str(player.score), False, (255, 0, 0))

    for enemy in enemy_list:
        enemy.move(dt)
        player.attack(enemy)

        enemy.rect.clamp_ip(screen_rect)

    sword.collision(player)
    katana.collision(player)
    kij.collision(player)

    all_sprites.update()
    all_sprites.draw(screen)
    player.render(screen)
    fps_counter.update()
    fps_counter.render()
    screen.blit(coordinates, (0, 0))
    pygame.display.flip()

print("Exited the game loop. Game will quit...")
quit()
