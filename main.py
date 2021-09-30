import random
import time
import math
import pygame
from pygame.sprite import collide_rect

from enemy import Enemy, EnemySlow
from environment import Wall
from maploader import MapLoader
from player import Player
from utils import PlayerInfo, FPSCounter
from weapon import Weapon
from bullet import Bullet
from item_bar import Items_bar
from player_dust import DustParticle
from rain import RainParticle

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
        self.myfont = pygame.font.SysFont('Comic Sans MS', 15)
        self.all_enemy = None
        self.all_environment = None
        self.all_wall = None
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
        self.weapon_group = None
        self.map = None
        self.particles = []
        self.last_shot = None
        self.items_menu = None
        self.bg = None
        self.entity_size = (75, 75)  # size of the characters(player, enemy)

    def init_all(self):
        self.wall_list = []
        self.all_enemy = pygame.sprite.Group()
        self.all_environment = pygame.sprite.Group()
        self.all_wall = pygame.sprite.Group()
        self.all_player = pygame.sprite.Group()
        self.bullet_list = pygame.sprite.Group()
        self.weapon_group = pygame.sprite.Group()

        ############WEAPONS############################################################
        wp_spawn_x = self.SIZE[0] / 2
        wp_spawn_y = self.SIZE[1] / 2 + 40
        # self.sword = Weapon(self, 15, 'sword', 15, self.RED, self.all_environment)
        self.katana = Weapon(self, 25, 'katana', 36, self.KATANA_COLOR, self.weapon_group)
        # self.kij = Weapon(self, 1, 'kij', 5, self.BLUE, self.all_environment)
        # add weapons to the menu

        ##########################################################################
        self.screen = pygame.display.set_mode(self.SIZE)
        self.player = Player(self, self.all_player)
        self.clock = pygame.time.Clock()
        self.screen_rect = self.screen.get_rect()

        self.fps_counter = FPSCounter(self, self.screen, self.myfont, self.clock, self.GREEN, (150, 10))
        self.player_info = PlayerInfo(self, (800, 10))
        self.counter = 0
        self.map = MapLoader(self)
        self.enemy_list = []
        for _ in range(1):
            self.enemy_list.append(Enemy(self, 20, 150, self.BLUE, "Ryszard", self.all_enemy))
        for _ in range(0):
            self.enemy_list.append(Enemy(self, 50, 50, self.RED, "Zbigniew", self.all_enemy))
        for _ in range(0):
            self.enemy_list.append(EnemySlow(self, 5, 1000, self.RED, "Janusz", self.all_enemy))

        self.items_menu = Items_bar(self)


    def draw_text(self, text, size, x, y):

        font = pygame.font.SysFont('Comic Sans MS', size)
        text_surface = font.render(text, True, self.WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)


    def game_over(self):
        self.init_all()
        pygame.display.flip()
        self.run_game()

    def collided(self, sprite, other):
        """Check if the hitbox of one sprite collides with rect of another sprite."""
        return sprite.hitbox.colliderect(other.rect)

    def collided2(self, sprite, other):
        """Check if the hitbox of one sprite collides with rect of another sprite."""
        return sprite.hitbox.colliderect(other.hitbox)


    def getMaskRect(self, surf, top=0, left=0):
        surf_mask = pygame.mask.from_surface(surf)
        rect_list = surf_mask.get_bounding_rects()
        surf_mask_rect = rect_list[0].unionall(rect_list)
        surf_mask_rect.move_ip(top, left)
        return surf_mask_rect

    def run_game(self):
        self.init_all()
        running = True

        while running:
            dt = self.clock.tick(60)
            dt = dt / 400
            self.last_shot = pygame.time.get_ticks()
            self.screen.fill(self.BLACK)  # Fill the screen with background color.
            self.player.old_velocity = self.player.velocity
            if len(self.all_enemy) <=0:
                self.enemy_list.append(Enemy(self, 20, 150, self.BLUE, "Ryszard", self.all_enemy))



            self.draw_text("Adam ", 50, 250, 250)
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
                        self.player.attacking = True
                        # self.player.current_stamina = 0#zmienione
                    if event.key == pygame.K_r:
                        self.game_over()
                    if event.key == pygame.K_z:
                        pygame.Surface.blit(pygame.transform.scale(self.player.image, (100, 100)), self.screen)

                    if event.key == pygame.K_1:
                        self.player.assign_weapon(self.sword)
                        self.items_menu.weapon = 'sword'
                    if event.key == pygame.K_2:
                        self.player.assign_weapon(self.katana)
                        self.items_menu.weapon = 'katana'
                    if event.key == pygame.K_3:
                        self.player.assign_weapon(self.kij)
                        self.items_menu.weapon = 'kij'

                if pygame.mouse.get_pressed()[0] and self.counter > 60:  # strzelanie nabojami
                    bullet = Bullet(self, self.player.gun_point()[0],
                                    self.player.gun_point()[1])  # adding bullet at the end of rifle
                    # self.all_environment.add(bullet)
                    self.bullet_list.add(bullet)
                    self.counter = 0

                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_w or event.key == pygame.K_s:
                        self.player.velocity[1] = 0
                        self.player.player_moving = False  # changed from direction
                    elif event.key == pygame.K_a or event.key == pygame.K_d:
                        self.player.velocity[0] = 0
                        self.player.player_moving = False

                    elif event.key == pygame.K_SPACE:
                        self.player.attacking = False
            self.player.attacked = False

            for enemy in self.enemy_list:
                enemy.move(dt)
                self.player.attack(enemy)  # checking for attack
                for bullet in self.bullet_list:
                    bullet.collision_enemy(enemy)


                # enemy.rect.clamp_ip(self.screen_rect)

                if enemy.hp > 0:
                    enemy.draw_health(self.screen)
                else:
                    enemy.kill()
                    self.enemy_list.remove(enemy)

            if self.player.attacked:
                self.player.current_stamina = 0

            self.weapon_group.update()
            self.all_wall.update()
            self.all_environment.update()
            self.all_enemy.update()
            self.all_player.update()
            self.bullet_list.update()

            #CHECKING if player or player
            #'s weapon collided with enemy (by masks, not rects)
            for enemy in self.enemy_list:
                if pygame.sprite.collide_mask(enemy, self.player):
                    pass
                if pygame.sprite.collide_mask(self.player.weapon, enemy):
                    enemy.hurt = True
                # enemy.hp -= 10

            for enemy in self.enemy_list:
                if pygame.sprite.collide_mask(enemy, self.player):
                    pass

            #Instead of using player.rect, player.hitbox is used

            # Instead of using player.rect, player.hitbox is used

            # def collided(self, sprite, other):
            #     """Check if the hitbox of one sprite collides with rect of another sprite."""
            #     return sprite.hitbox.colliderect(other.rect)
            # Check for collision between player and wall
            collided_sprites_player = pygame.sprite.spritecollide(self.player, self.wall_list, False, self.collided)
            for sprite in collided_sprites_player:

                velocity = [i * (-0.5) for i in self.player.old_velocity]#how far from wall will you bounce

                velocity = [i * (-0.25) for i in self.player.old_velocity]  # how far from wall will you bounce

                self.player.velocity = velocity
                self.player.update()
                self.player.velocity = [0, 0]

            # Check for collision between enemy and walls
            for enemy in self.all_enemy:
                collided_sprites_enemy = pygame.sprite.spritecollide(enemy, self.wall_list, False, self.collided)
                for sprite in collided_sprites_enemy:
                    velocity_en = [i * (-1) for i in enemy.old_velocity]
                    enemy.velocity = velocity_en
                    enemy.update()
                    enemy.velocity = [0, 0]

            for block in self.wall_list:



                # Given our hitbox, we do not have to check collide_rect, cause
                # it exclusively uses rect attribute of Sprite class

                # if collide_rect(self.player, block):
                #     velocity = [i * (-1) for i in self.player.old_velocity]
                #     self.player.velocity = velocity
                #     self.player.update()
                #     self.player.velocity = [0, 0]

                for bullet in self.bullet_list:  # shooting wall, bullet disapers
                    bullet.collision(block)

                # for enemy in self.enemy_list:
                #     if collide_rect(enemy, block):
                #         velocity_en = [i * (-1) for i in enemy.old_velocity]
                #         enemy.velocity = velocity_en
                #         enemy.update()
                #         enemy.velocity = [0, 0]
            # for i in range(int(self.SIZE[0]/20)):
            #     for x in range(int(self.SIZE[1]/10)):
            #         pygame.draw.rect(self.screen, (102, 29, 102), (395,0,100,100))

            # self.bullet_list.draw(self.screen)
            # self.weapon_group.draw(self.screen)
            self.all_environment.draw(self.screen)
            self.all_enemy.draw(self.screen)
            self.all_player.draw(self.screen)
            self.all_wall.draw(self.screen)
            self.player.render()
            for bullet in self.bullet_list:
                bullet.draw()

            # ---------PARTICLE ANIMATION############
            for particle in self.particles:
                particle.update()
            ##########################################
            self.fps_counter.update()
            self.fps_counter.render()
            self.player_info.update()
            self.player_info.render()

            ##item bar display
            self.items_menu.draw()
            self.counter += 1
            pygame.display.update()
        print("Exited the game loop. Game will quit...")
        quit()


def main():
    game = Game()
    game.run_game()


if __name__ == "__main__":
    main()
