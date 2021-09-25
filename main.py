import random

import pygame

successes, failures = pygame.init()
print(f"Initializing pygame: {successes} successes and {failures} failures.")

FPS = 60
blit_objects = []  # table of objects to blit
SIZE = (1200, 800)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BROWN = (185, 100, 0)

# pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 15)


class Screen(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.image = pygame.Surface(SIZE)
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()  # Get rect of some size as 'image'.
        self.priority = 0
        blit_objects.append(self)


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
        # blit_objects.append(self)

        # Player Attacking
        self.attacking = False
        self.attack_range = pygame.Rect(0, 0, 0, 0)

    def attack(self):
        if self.attacking == True:
            self.attack_range = pygame.Rect(self.rect.x + self.rect.width, self.rect.y, 30, self.rect.height)
        else:
            self.attack_range = pygame.Rect(0, 0, 0, 0)

    def update(self):
        self.rect.move_ip(*self.velocity)
        self.attack()

    def render(self, display):
        # pygame.draw.rect(display, (255, 0, 0), self.rect)
        pygame.draw.rect(display, (0, 255, 0), self.attack_range)
        display.blit(self.image, self.rect)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.image = pygame.Surface((2, 2))
        self.image.fill(BLUE)
        self.image.set_colorkey(RED)
        self.rect = self.image.get_rect()
        self.velocity = [0, 0]
        self.priority = 100
        blit_objects.append(self)

    def update(self):
        self.rect.move_ip(*self.velocity)

    def move(self, dtick, collided):
        self.velocity[0] = random.randint(-50, 150) * dtick / 2
        self.velocity[1] = random.randint(-50, 150) * dtick / 2
        self.collision(collided)

    def collision(self, collided):
        if self.rect.colliderect(collided):
            self.image.fill(RED)
            self.kill()


class FPSCounter:
    def __init__(self, surface, font, cock, color, pos):
        self.surface = surface
        self.font = font
        self.clock = cock
        self.pos = pos
        self.color = color

        self.fps_text = self.font.render(str(int(self.clock.get_fps())) + "FPS", False, self.color)
        self.fps_text_rect = self.fps_text.get_rect(center=(self.pos[0], self.pos[1]))

    def render(self):
        self.surface.blit(self.fps_text, self.fps_text_rect)

    def update(self):
        text = f"{self.clock.get_fps():2.0f} FPS"
        self.fps_text = self.font.render(text, False, self.color)
        self.fps_text_rect = self.fps_text.get_rect(center=(self.pos[0], self.pos[1]))


all_sprites = pygame.sprite.Group()
screen = Screen(all_sprites)
player = Player(all_sprites)

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
                player.velocity[1] = -200 * dt
            elif event.key == pygame.K_s:
                player.velocity[1] = 200 * dt
            elif event.key == pygame.K_a:
                player.velocity[0] = -200 * dt
            elif event.key == pygame.K_d:
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

    coordinates = myfont.render(str(player.rect.x) + ', ' + str(player.rect.y), False, (255, 0, 0))

    for enemy in enemy_list:
        if enemy.priority > 0:
            enemy.move(dt, player)
            enemy.rect.clamp_ip(screen_rect)

    all_sprites.update()
    all_sprites.draw(screen)
    player.render(screen)

    screen.blit(coordinates, (0, 0))
    fps_counter.render()
    fps_counter.update()
    pygame.display.flip()

print("Exited the game loop. Game will quit...")
quit()
