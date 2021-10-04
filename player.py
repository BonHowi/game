import pygame
import os
from weapon import Weapon
from Entity import Entity
#import numpy as np


class Player(pygame.sprite.Sprite):
    def __init__(self, game, *groups):
        super().__init__(*groups)
        self.game = game
        self.animation_database = {"IDLE_LEFT": [],
                                   "IDLE_RIGHT": [],
                                   "WALK_LEFT": [],
                                   "WALK_RIGHT": []}

        self.image_size = (75, 75)
        self.image = pygame.image.load("player/idle/right_idle0.png")
        self.image = pygame.transform.scale(self.image, self.image_size)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.mask.get_rect(center=self.game.screen.get_rect().center)
        self.rect_mask = self.getMaskRect(self.image, *self.rect.topleft)  # Get rect of some size as 'image'.
        self.velocity = [0, 0]
        self.old_velocity = [0, 0]
        self.speed = 100
        self.priority = 1000
        self.score = 0
        self.direction = 'RIGHT'
        self.player_moving = False
        self.player_index = 0 #animation frames
        # Player Attacking
        self.attacking = False
        self.hasWeapon = True
        self.weapon = Weapon(self.game, 10, 'katana', 2, self.game.RED,
                             self.game.weapon_group)  # usuniete groups z self.game
        self.hp = 100
        self.max_stamina = 1000
        self.current_stamina = self.max_stamina
        self.attacked = False
        ########GUN PROPERTIES,########
        self.gun_length = 15
        self.gun_width = 5
        #Animation loading
        self.load_animation('player/')
        # hitbox
        self.hitbox = self.rect_mask

    def getMaskRect(self, surf, top=0, left=0):
        """

        :param surf:
        :type surf:
        :param top:
        :type top:
        :param left:
        :type left:
        :return:
        :rtype:
        """
        surf_mask = pygame.mask.from_surface(surf)
        rect_list = surf_mask.get_bounding_rects()
        surf_mask_rect = rect_list[0].unionall(rect_list)
        surf_mask_rect.move_ip(top, left)
        return surf_mask_rect

    def load_animation(self, path):
        """

        :param path:
        :type path:
        :return:
        :rtype:
        """
        animation_states = os.listdir(path)
        for state in animation_states:
            substates = os.listdir(path + state)
            for ss in substates:
                image_loc = ss
                elements = image_loc.split('_')
                key = state.upper() + '_' + elements[0].upper()  # key to dictionary
                animation_image = pygame.image.load(path + state + '/' + image_loc).convert()
                animation_image = pygame.transform.scale(animation_image, self.image_size)
                self.animation_database[key].append(animation_image)

    def moving(self):
        """

        :return:
        :rtype:
        """
        if self.velocity[0] != 0 or self.velocity[1] != 0:
            return True
        else:
            return False

    def animation(self):
        """

        :return:
        :rtype:
        """
        if self.moving():
            self.player_index += 1.0 / 15  # how fast animation changes
            if self.player_index >= 4:
                self.player_index = 0
            if self.direction == 'LEFT':
                self.image = self.animation_database["WALK_LEFT"][int(self.player_index)]

            elif self.direction == 'UP':
                self.image = self.animation_database["WALK_RIGHT"][int(self.player_index)]

            elif self.direction == "RIGHT":
                self.image = self.animation_database["WALK_RIGHT"][int(self.player_index)]

            elif self.direction == "DOWN":
                self.image = self.animation_database["WALK_RIGHT"][int(self.player_index)]
        else:  # if idle
            self.player_index += 1.0 / 15  # how fast animation changes
            if self.player_index >= 4:
                self.player_index = 0
            if self.direction == 'LEFT':
                self.image = self.animation_database["IDLE_LEFT"][int(self.player_index)]
            elif self.direction == 'RIGHT':
                self.image = self.animation_database["IDLE_RIGHT"][int(self.player_index)]
            elif self.direction == "UP":
                self.image = self.animation_database["IDLE_RIGHT"][int(self.player_index)]
            elif self.direction == "DOWN":
                self.image = self.animation_database["IDLE_RIGHT"][int(self.player_index)]



    def weapon_attack(self, enemy):#attacking enemy with sword/katan/kij
        pass
    # def attack(self, collision_obj):
    #
    #     """
    #
    #     :param collision_obj:
    #     :type collision_obj:
    #     :return:
    #     :rtype:
    #     """
    #     if self.attacking and self.hasWeapon and self.current_stamina >= 1000:
    #         if self.direction == 'RIGHT':
    #             self.attack_range = pygame.Rect(self.hitbox.x + self.hitbox.width, self.hitbox.y,
    #                                             self.weapon.blade_length, self.hitbox.height)
    #             self.attack_collision(collision_obj)
    #         elif self.direction == 'LEFT':
    #             self.attack_range = pygame.Rect(self.hitbox.x - self.weapon.blade_length, self.hitbox.y,
    #                                             self.weapon.blade_length, self.hitbox.height)
    #             self.attack_collision(collision_obj)
    #         elif self.direction == 'UP':
    #             self.attack_range = pygame.Rect(self.hitbox.x, self.hitbox.y - self.weapon.blade_length,
    #                                             self.hitbox.height,
    #                                             self.weapon.blade_length)
    #             self.attack_collision(collision_obj)
    #         elif self.direction == 'DOWN':
    #             self.attack_range = pygame.Rect(self.hitbox.x, self.hitbox.y + self.hitbox.height, self.hitbox.height,
    #                                             self.weapon.blade_length)
    #             self.attack_collision(collision_obj)

    def attack_collision(self, collision_obj):  # do zmiany
        """

        :param collision_obj:
        :type collision_obj:
        :return:
        :rtype:
        """
        if self.attack_range.colliderect(collision_obj.hitbox):
            self.calculate_collison(collision_obj, self.weapon.damage)

    def calculate_collison(self, collision_obj, damage):
        """

        :param collision_obj:
        :type collision_obj:
        :param damage:
        :type damage:
        :return:
        :rtype:
        """
        if collision_obj.hp > 0:
            collision_obj.hp -= damage
            collision_obj.hurt = True  # indicating that enemy is hurt
            if collision_obj.hp <= 0:
                self.score += 1
        self.attacked = True

    def set_velocity(self, velocity):
        self.velocity = velocity
        # print(np.linalg.norm(self.velocity))
        # if self.velocity != velocity
        # self.velocity = [0, 0]
        # self.velocity = [sum(x) for x in zip(self.velocity, velocity)]

    def update(self):
        """

        :return:
        :rtype:
        """
        self.animation()

        self.rect.clamp_ip(self.game.screen_rect)
        self.rect.move_ip(*self.velocity)

        self.rect_mask.clamp_ip(self.game.screen_rect)
        self.rect_mask.move_ip(*self.velocity)

        if self.current_stamina < self.max_stamina:
            self.current_stamina += 10

        self.attacked = False
        # self.hitbox = pygame.Rect(self.rect.x + 19, self.rect.y + 25, 37, 50)
        self.hitbox = self.rect_mask
        self.rect.midbottom = self.hitbox.midbottom
        pygame.draw.rect(self.game.screen, (0, 255, 0), self.rect, 1)
        pygame.draw.rect(self.game.screen, (255, 0, 0), self.hitbox, 1)

    def render(self):
        """

        :return:
        :rtype:
        """

        # start = pygame.math.Vector2(self.rect.midright)
        # mouse = pygame.mouse.get_pos()
        # end = start + (mouse - start).normalize() * self.gun_length

        # pygame.draw.lines(self.game.screen, (255, 255, 255), False, (start, end), width=self.gun_width)

    def gun_point(self):  # zmienic, bo brzydko
        """

        :return:
        :rtype:
        """
        start = pygame.math.Vector2(self.rect.midright)
        mouse = pygame.mouse.get_pos()
        end = start + (mouse - start).normalize() * self.gun_length
        return end

    def assign_weapon(self, weapon: Weapon):
        """

        :param weapon:
        :type weapon:
        :return:
        :rtype:
        """
        self.weapon = weapon
        self.hasWeapon = True

    def gun_line(self, ax, ay, bx, by, radius):
        """

        :param ax:
        :type ax:
        :param ay:
        :type ay:
        :param bx:
        :type bx:
        :param by:
        :type by:
        :param radius:
        :type radius:
        :return:
        :rtype:
        """
        pass
