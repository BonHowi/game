import random

import pygame

successes, failures = pygame.init()
print(f"Initializing pygame: {successes} successes and {failures} failures.")

FPS = 120
blit_objects = []  # table of objects to blit
SIZE = (720, 720)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BROWN = (185, 100, 0)

# pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 15)


class Screen(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface(SIZE)
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()  # Get rect of some size as 'image'.
        self.priority = 0
        blit_objects.append(self)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(BROWN)
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()  # Get rect of some size as 'image'.
        self.rect.x = SIZE[0] / 2
        self.rect.y = SIZE[1] / 2
        self.velocity = [0, 0]
        self.priority = 1000
        #blit_objects.append(self)

        # Player Attacking
        self.attacking = False
        self.attack_range = pygame.Rect(0, 0, 0, 0)

    def attack(self):
        if self.attacking == True:
            self.attack_range = pygame.Rect(self.rect.x + self.rect.width,self.rect.y, 30, self.rect.height)
        else:
            self.attack_range = pygame.Rect(0, 0, 0, 0)

    def update(self):
        self.rect.move_ip(*self.velocity)
        self.attack()

    def render(self, display):
        #pygame.draw.rect(display, (255, 0, 0), self.rect)
        pygame.draw.rect(display, (0, 255, 0), self.attack_range)
        display.blit(self.image, self.rect)


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20, 20))
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
            self.priority = -10
        else:
            self.image.fill(BLUE)


screen = Screen()
player = Player()
enemy = Enemy()


def blit_all(blit_objects_list):
    blit_objects_list.sort(key=lambda x: x.priority, reverse=False)
    for blit_object in blit_objects_list:
        screen.blit(blit_object.image, blit_object.rect)


running = True
while running:
    screen = pygame.display.set_mode(SIZE)
    clock = pygame.time.Clock()
    screen_rect = screen.get_rect()
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
    player.update()

    coordinates = myfont.render(str(player.rect.x) + ', ' + str(player.rect.y), False, (255, 0, 0))

    enemy.move(dt, player)
    enemy.rect.clamp_ip(screen_rect)
    enemy.update()

    blit_all(blit_objects)
    player.render(screen)
    screen.blit(coordinates, (0, 0))

    pygame.display.update()  # Or pygame.display.flip()

print("Exited the game loop. Game will quit...")
quit()
