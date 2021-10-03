import pygame
import random
from math import atan2, cos, sin, sqrt


# direction of the bullet, if the bullet shoots right, the particles should move on the right side of x axis

class Particle:
    def __init__(self, game, x, y):
        self.game = game
        self.x = x
        self.y = y
        self.life = None  # how long should particle live(frames)


class EnemyHitParticle(Particle):
    color = (255, 0, 0)
    radius = random.randint(3, 8)

    def update(self):
        self.x += random.randint(-1, 1)
        self.y += random.randint(-1, 1)
        self.radius -= 0.20
        if self.radius <= 0:
            self.game.particles.remove(self)

    def draw(self):
        pygame.draw.circle(self.game.screen, self.color, (self.x, self.y), self.radius)


class WallHitParticle(Particle):
    # color = (128, 148, 171)
    # radius = 10
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.color = (128, 148, 171)
        self.radius = 10

    def update(self):
        self.x += random.randint(-1, 1)
        self.y += random.randint(-1, 1)
        self.radius -= 0.7

        if self.radius <= 0:
            self.game.particles.remove(self)

    def draw(self):
        pygame.draw.circle(self.game.screen, self.color, (self.x, self.y), self.radius)


class Fireball(Particle):
    '''Besides some calculations and magic variables, there is a bsurf Surface in game class, which serves as screen to display fire plarticles,
    it is 4x times smaller than default window, but during blitting, it is resized to window size, as to achieve pixelated fire)'''
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.color = ((255, 255, 0),
                      (255, 173, 51),
                      (247, 117, 33),
                      (191, 74, 46),
                      (115, 61, 56),
                      (61, 38, 48))
        self.maxlife = random.randint(13, 27)
        self.life = self.maxlife
        self.sin = random.randint(-10, 10) / 7 # ???? XD
        self.sinr = random.randint(5, 10)
        self.radius = random.randint(0, 2)

        self.ox = random.randint(-1, 1)
        self.oy = random.randint(-1, 1)
        self.j = random.randint(0, 360)
        self.i = int(((self.life - 1) / self.maxlife) * 6)
        self.alpha = None
        self.draw_x = x
        self.draw_y = y
        self.counter = 0

    def update(self):
        if self.counter == 2:
            self.counter = 0;
            if self.j > 360: # Angle
                self.j = 0

            self.life -= 1
            if self.life == 0:
                self.game.particles.remove(self)

            self.i = int((self.life / self.maxlife) * 6)

            self.y -= 1.25  # rise
            self.x += ((self.sin * sin(self.j / self.sinr)) / 2) + 1  # spread

            if not random.randint(0, 5):
                self.radius += 1  # circle radius, set to 10 for big bang

            self.draw_x, self.draw_y = self.x, self.y

            self.draw_x += self.ox * (5 - self.i)
            self.draw_y += self.oy * (5 - self.i)

            self.alpha = 255
            if self.life < self.maxlife / 4:
                self.alpha = int((self.life / self.maxlife) * 255)
        else:
            self.counter += 1

    def draw(self):

        alpha = 255
        pygame.draw.circle(self.game.bsurf, self.color[self.i] + (alpha,), (self.draw_x, self.draw_y), self.radius, 0)
        if self.i == 0:
            pygame.draw.circle(self.game.bsurf, (0, 0, 0, 0), (self.draw_x + random.randint(-1, 1), self.draw_y - 4),
                               self.radius * (((self.maxlife - self.life) / self.maxlife) / 0.88), 0)
        else:
            pygame.draw.circle(self.game.bsurf, self.color[self.i - 1] + (alpha,),
                               (self.draw_x + random.randint(-1, 1), self.draw_y - 3),
                               self.radius / 1.5, 0)
