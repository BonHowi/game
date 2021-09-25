import random

import pygame

successes, failures = pygame.init()
print(f"Initializing pygame: {successes} successes and {failures} failures.")

screen = pygame.display.set_mode((720, 720))
clock = pygame.time.Clock()
screen_rect = screen.get_rect()
FPS = 120
blit_objects = [] #table of objects to blit


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)




GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 15)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()  # Get rect of some size as 'image'.
        self.velocity = [0, 0]
        blit_objects.append([self.image,self.rect])


    def update(self):
        self.rect.move_ip(*self.velocity)


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.velocity = [0, 0]
        blit_objects.append([self.image,self.rect])

    def update(self):
        self.rect.move_ip(*self.velocity)

    def move(self, dtick):
        self.velocity[0] = random.randint(-150, 150) * dtick / 2
        self.velocity[1] = random.randint(-150, 150) * dtick / 2


player = Player()
enemy = Enemy()

def blit_all(objects):
    for object in objects:
        screen.blit(object[0], object[1])

running = True
while running:
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
                player.image.fill(RED)

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_w or event.key == pygame.K_s:
                player.velocity[1] = 0
            elif event.key == pygame.K_a or event.key == pygame.K_d:
                player.velocity[0] = 0
            elif event.key == pygame.K_SPACE:
                player.image.fill(WHITE)
    player.rect.clamp_ip(screen_rect)
    player.update()

    coordinates = myfont.render(str(player.rect.x) + ', ' + str(player.rect.y), False, (0, 0, 0))

    enemy.move(dt)
    enemy.rect.clamp_ip(screen_rect)
    enemy.update()

    #screen.blit(player.image, player.rect)
    #screen.blit(enemy.image, enemy.rect)
    blit_all(blit_objects)
    screen.blit(coordinates, (0, 0))

    pygame.display.update()  # Or pygame.display.flip()

print("Exited the game loop. Game will quit...")
quit()
