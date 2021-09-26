import random
import time

import pygame
from pygame.sprite import collide_rect

from enemy import Enemy, EnemySlow
from environment import Wall
from player import Player
from utils import PlayerInfo, FPSCounter
from weapon import Weapon
from bullet import Bullet
from particle_test import ParticleTest
from particles import Particle

successes, failures = pygame.init()
print(f"Initializing pygame: {successes} successes and {failures} failures.")

particles = []
class Game:
    def __init__(self):
        self.FPS = 144
        self.SIZE = (1200, 600)

        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)
        self.BROWN = (185, 100, 0)
        self.KATANA_COLOR = (169, 169, 169)

        self.color = [self.BLACK,self.WHITE, self.RED, self.BLUE, self.BROWN, self.KATANA_COLOR]

        # pygame.font.init()
        self.myfont = pygame.font.SysFont('Comic Sans MS', 15)
        self.all_enemy = None
        self.all_environment = None
        self.all_player = None
        # screen = Screen(all_sprites)
        self.player = None
        # assigning weapon
        self.sword = None
        self.katana = None
        self.kij = None
        self.screen = None
        self.clock = None
        self.screen_rect = None
        self.fps_counter = None
        self.player_info = None
        self.wall_list = []
        self.enemy_list = []
        self.bullet_list = None

        self.last_shot = None

    def init_all(self):
        self.wall_list = []
        self.all_enemy = pygame.sprite.Group()
        self.all_environment = pygame.sprite.Group()
        self.all_player = pygame.sprite.Group()
        self.player = Player(self, self.all_player)
        # assigning weapon
        wp_spawn_x = self.SIZE[0] / 2
        wp_spawn_y = self.SIZE[1] / 2 + 40
        self.sword = Weapon(15, 'Sword', 15, self.RED, wp_spawn_x, wp_spawn_y,
                            self.all_environment)
        self.katana = Weapon(25, 'Katana', 36, self.KATANA_COLOR, wp_spawn_x + 50, wp_spawn_y,
                             self.all_environment)
        self.kij = Weapon(1, 'Kij', 5, self.BLUE, wp_spawn_x - 50, wp_spawn_y,
                          self.all_environment)

        self.screen = pygame.display.set_mode(self.SIZE)
        self.clock = pygame.time.Clock()
        self.screen_rect = self.screen.get_rect()

        self.fps_counter = FPSCounter(self, self.screen, self.myfont, self.clock, self.GREEN, (150, 10))
        self.player_info = PlayerInfo(self, (800, 10))

        self.wall_list = []
        for _ in range(random.randint(10, 30)):
            self.wall_list.append(Wall(self, self.all_environment))

        self.enemy_list = []
        for _ in range(10):
            self.enemy_list.append(Enemy(self, 200, 150, self.BLUE, "Ryszard", self.all_enemy))
        for _ in range(10):
            self.enemy_list.append(Enemy(self, 400, 50, self.RED, "Zbigniew", self.all_enemy))
        for _ in range(5):
            self.enemy_list.append(EnemySlow(self, 10, 1000, self.RED, "Zbigniew", self.all_enemy))

        self.bullet_list = pygame.sprite.Group()

    def game_over(self):
        self.init_all()
        pygame.display.flip()
        self.run_game()

    def run_game(self):
        self.init_all()
        running = True

        while running:
            dt = self.clock.tick(self.FPS) / 400
            self.last_shot = pygame.time.get_ticks()
            self.screen.fill(self.BLACK)  # Fill the screen with background color.
            self.player.old_velocity = self.player.velocity

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        self.player.direction = 'UP'
                        self.player.velocity[1] = -self.player.speed * dt
                    elif event.key == pygame.K_s:
                        self.player.direction = 'DOWN'
                        self.player.velocity[1] = self.player.speed * dt
                    elif event.key == pygame.K_a:
                        self.player.direction = 'LEFT'
                        self.player.velocity[0] = -self.player.speed * dt
                    elif event.key == pygame.K_d:
                        self.player.direction = 'RIGHT'
                        self.player.velocity[0] = self.player.speed * dt
                    elif event.key == pygame.K_SPACE:
                        self.player.image.fill(self.RED)
                        self.player.attacking = True
                    if event.key == pygame.K_r:
                        self.game_over()

                elif event.type == pygame.MOUSEBUTTONDOWN:  # strzelanie nabojami
                    bullet = Bullet(self,self.player.rect.x, self.player.rect.y)
                    self.all_environment.add(bullet)
                    self.bullet_list.add(bullet)

                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_w or event.key == pygame.K_s:
                        self.player.velocity[1] = 0
                    elif event.key == pygame.K_a or event.key == pygame.K_d:
                        self.player.velocity[0] = 0
                    elif event.key == pygame.K_SPACE:
                        self.player.image.fill(self.BROWN)
                        self.player.attacking = False

            self.player.attacked = False
            for enemy in self.enemy_list:
                enemy.move(dt)
                self.player.attack(enemy)
                for bullet in self.bullet_list:
                    bullet.collision(enemy)

                enemy.rect.clamp_ip(self.screen_rect)
                if enemy.hp > 0:
                    enemy.draw_health(self.screen)
                else:
                    enemy.kill()
                    self.enemy_list.remove(enemy)
            if self.player.attacked:
                self.player.current_stamina = 0

            self.sword.collision(self.player)
            self.katana.collision(self.player)
            self.kij.collision(self.player)

            self.all_environment.update()
            self.all_enemy.update()
            self.all_player.update()
            block = None

            for block in self.wall_list:
                if collide_rect(self.player, block):
                    velocity = [i * (-1) for i in self.player.old_velocity]
                    self.player.velocity = velocity
                    self.player.update()
                    self.player.velocity = [0, 0]

                for bullet in self.bullet_list:  ##shooting wall, bullet disapers
                    if collide_rect(block, bullet):
                        bullet.kill()
                        #--------------PARTICLES----------------#
                        for _ in range(15):
                            particles.append([[bullet.rect.x, bullet.rect.y], [random.randint(0, 20) / 10 - 1, 2], random.randint(4, 6)])
                        # particle animation

            for enemy in self.enemy_list:
                if collide_rect(enemy, block):
                    velocity_en = [i * (-1) for i in enemy.old_velocity]
                    enemy.velocity = velocity_en
                    enemy.update()
                    enemy.velocity = [0, 0]

            self.player.render(self.screen)
            self.fps_counter.update()
            self.fps_counter.render()
            self.player_info.update()
            self.player_info.render()
            #---------PARTICLE ANIMATION############
            for particle in particles:
                particle[0][0] +=particle[1][0]#x axis
                particle[0][1] += particle[1][1]#y axis
                particle[2] -=0.1
                pygame.draw.circle(self.screen, random.choice(self.color), particle[0], particle[2])
                if particle[2] <=0:
                    particles.remove(particle)
            #----------------------###############################
            self.all_environment.draw(self.screen)
            self.all_enemy.draw(self.screen)
            self.all_player.draw(self.screen)

            pygame.display.update()

        print("Exited the game loop. Game will quit...")
        quit()


def main():
    game = Game()
    game.run_game()


if __name__ == "__main__":
    main()
