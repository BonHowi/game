import pygame, sys
from pygame.math import Vector2
import random
pygame.init()
# Create the window, saving it to a variable.
surface = pygame.display.set_mode((1200, 600))
clock = pygame.time.Clock()
bg = pygame.Surface((400, 200)).convert_alpha()
zoom_factor = 1.0
class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocity = [0, 0]
        self.speed = 100
        self.v = Vector2(self.x, self.y)


    def move(self):
        self.v += self.velocity
        self.x = self.v[0]
        self.y = self.v[1]

    def draw(self):
        pygame.draw.circle(surface, (255, 35, 120), self.v, 30 * zoom_factor)


player = Player(100, 100)
while True:
    dt = clock.tick(60)
    dt = dt / 400
    surface.fill((255,255,255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == pygame.K_w:
                player.velocity[1] = -player.speed * dt

            if event.key == pygame.K_s:
                player.velocity[1] = player.speed * dt

            if event.key == pygame.K_a:
                player.velocity[0] = -player.speed * dt

            if event.key == pygame.K_d:
                player.velocity[0] = player.speed * dt
            if event.key == pygame.K_z:
                zoom_factor += 0.25
        player.move()
        player.draw()
        pygame.display.update()
