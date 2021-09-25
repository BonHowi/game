import random

import pygame
from pygame.sprite import collide_rect

from enemy import Enemy
from environment import Wall, FPSCounter
from player import Player
from utils import PlayerInfo
from weapon import Weapon

successes, failures = pygame.init()
print(f"Initializing pygame: {successes} successes and {failures} failures.")


class Game:
    def __init__(self):
        self.FPS = 60
        self.SIZE = (1200, 600)

        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)
        self.BROWN = (185, 100, 0)
        self.KATANA_COLOR = (169, 169, 169)

        # pygame.font.init()
        self.myfont = pygame.font.SysFont('Comic Sans MS', 15)

        self.all_enemy = pygame.sprite.Group()
        self.all_environment = pygame.sprite.Group()
        self.all_player = pygame.sprite.Group()
        # screen = Screen(all_sprites)
        self.player = Player(self, self.all_player)
        # assigning weapon
        self.sword = Weapon(15, 'Sword', 15, self.RED, 200, 50, self.all_environment)
        self.katana = Weapon(25, 'Katana', 36, self.KATANA_COLOR, 250, 50, self.all_environment)
        self.kij = Weapon(1, 'Kij', 5, self.BLUE, 300, 50, self.all_environment)

        self.screen = pygame.display.set_mode(self.SIZE)
        self.clock = pygame.time.Clock()
        self.screen_rect = self.screen.get_rect()

        self.fps_counter = FPSCounter(self, self.screen, self.myfont, self.clock, self.GREEN, (150, 10))
        self.player_info = PlayerInfo(self, (800, 10))

        self.wall_list = []
        for _ in range(random.randint(10, 30)):
            self.wall_list.append(Wall(self, self.all_environment))

        self.enemy_list = []
        for _ in range(1000):
            self.enemy_list.append(Enemy(self, self.all_enemy))

    def run_game(self):
        running = True
        while running:
            dt = self.clock.tick(self.FPS) / 400
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

                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_w or event.key == pygame.K_s:
                        self.player.velocity[1] = 0
                    elif event.key == pygame.K_a or event.key == pygame.K_d:
                        self.player.velocity[0] = 0
                    elif event.key == pygame.K_SPACE:
                        self.player.image.fill(self.BROWN)
                        self.player.attacking = False

            for enemy in self.enemy_list:
                enemy.move(dt)
                self.player.attack(enemy)

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

            for block in self.wall_list:
                if collide_rect(self.player, block):
                    velocity = [i * (-1) for i in self.player.old_velocity]
                    self.player.velocity = velocity
                    self.player.update()
                    self.player.velocity = [0, 0]
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
