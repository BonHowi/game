import random

import pygame
from pygame.sprite import collide_rect

from enemy import Enemy
from environment import Wall, FPSCounter
from player import Player
from utils import PlayerInfo
from weapon import Weapon
from bullet import Bullet

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

        self.all_sprites = pygame.sprite.Group()
        # screen = Screen(all_sprites)
        self.player = Player(self, self.all_sprites)
        # assigning weapon
        self.sword = Weapon(15, 'Sword', 15, self.RED, 200, 50, self.all_sprites)
        self.katana = Weapon(25, 'Katana', 36, self.KATANA_COLOR, 250, 50, self.all_sprites)
        self.kij = Weapon(1, 'Kij', 5, self.BLUE, 300, 50, self.all_sprites)

        # player.assign_weapon(sword)

        self.wall_list = []
        for _ in range(random.randint(10, 30)):
            self.wall_list.append(Wall(self, self.all_sprites))

        self.enemy_list = []
        for _ in range(10):
            self.enemy_list.append(Enemy(self, self.all_sprites))

        self.bullet_list = pygame.sprite.Group()

    def run_game(self):
        running = True
        while running:
            screen = pygame.display.set_mode(self.SIZE)
            clock = pygame.time.Clock()
            screen_rect = screen.get_rect()
            fps_counter = FPSCounter(screen, self.myfont, clock, self.GREEN, (150, 10))
            player_info = PlayerInfo(self.player, screen, self.myfont, clock, self.GREEN, (800, 10))

            dt = clock.tick(
                self.FPS) / 400  # Returns milliseconds between each call to 'tick'. The convert time to seconds.
            screen.fill(self.BLACK)  # Fill the screen with background color.
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
                elif event.type == pygame.MOUSEBUTTONDOWN:#strzelanie nabojami
                    bullet = Bullet()
                    bullet.rect.x = self.player.rect.x
                    bullet.rect.y = self.player.rect.y
                    bullet.direction = self.player.direction # kierunek strzału
                    self.all_sprites.add(bullet)
                    self.bullet_list.add(bullet)

                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_w or event.key == pygame.K_s:
                        self.player.velocity[1] = 0
                    elif event.key == pygame.K_a or event.key == pygame.K_d:
                        self.player.velocity[0] = 0
                    elif event.key == pygame.K_SPACE:
                        self.player.image.fill(self.BROWN)
                        self.player.attacking = False

            self.player.rect.clamp_ip(screen_rect)
            if self.player.current_stamina < self.player.max_stamina:
                self.player.current_stamina += 100

            coordinates = self.myfont.render('SCORE: ' + str(self.player.score), False, (255, 0, 0))

            self.player.attacked = False



            for enemy in self.enemy_list:
                enemy.move(dt)
                self.player.attack(enemy)
                for bullet in self.bullet_list:
                    bullet.collision(enemy)

                enemy.rect.clamp_ip(screen_rect)
                if enemy.hp > 0:
                    enemy.draw_health(screen)
            if self.player.attacked:
                self.player.current_stamina = 0

            self.sword.collision(self.player)
            self.katana.collision(self.player)
            self.kij.collision(self.player)

            self.all_sprites.update()
            for block in self.wall_list:
                if collide_rect(self.player, block):
                    velocity = [i * (-1) for i in self.player.old_velocity]
                    self.player.velocity = velocity
                    self.player.update()
                    self.player.velocity = [0, 0]

                for bullet in self.bullet_list: ##shooting wall, bullet disapers
                    if collide_rect(block, bullet):
                        bullet.kill()

            for enemy in self.enemy_list:
                if collide_rect(enemy, block):
                    velocity_en = [i * (-1) for i in enemy.old_velocity]
                    enemy.velocity = velocity_en
                    enemy.update()
                    enemy.velocity = [0, 0]


            self.player.render(screen)

            fps_counter.update()
            fps_counter.render()
            # player_info.update() i think, niepotrzebne
            player_info.render()

            screen.blit(coordinates, (0, 0))

            self.all_sprites.draw(screen)
            pygame.display.update()
        print("Exited the game loop. Game will quit...")
        quit()


def main():
    game = Game()
    game.run_game()


if __name__ == "__main__":
    main()
