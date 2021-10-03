import pygame
from particles import Particle
from pygame.math import Vector2

class Weapon(pygame.sprite.Sprite):
    def __init__(self, game, damage, name, width, color, *groups):
        super().__init__(*groups)
        self.width = width
        self.damage = damage
        self.name = name
        self.blade_length = int(width)
        self.color = color
        self.original_image = None
        self.image = None
        self.mask = None
        self.rect = None
        self.rect_mask = None
        self.hitbox = None
        self.game = game
        self.load_image()
        self.counter = 1
        self.angle = 0
        self.pivot = self.rect_mask.bottomleft
        self.offset = Vector2(4, -34)
        self.angle_change_factor_start = 1
        self.angle_change_factor = self.angle_change_factor_start
        self.is_finished = False


    def getMaskRect(self, surf, top=0, left=0):
        surf_mask = pygame.mask.from_surface(surf)
        rect_list = surf_mask.get_bounding_rects()
        surf_mask_rect = rect_list[0].unionall(rect_list)
        surf_mask_rect.move_ip(top, left)
        return surf_mask_rect

    def load_image(self):
        self.original_image = pygame.image.load('weapon/' + self.name + '.png')
        self.original_image = pygame.transform.scale(self.original_image, (75, 75))
        self.mask = pygame.mask.from_surface(self.original_image)
        self.rect = self.mask.get_rect()
        self.rect_mask = self.getMaskRect(self.original_image, *self.rect.topleft)
        self.hitbox = self.rect_mask
        self.image = self.original_image

    def collision(self, collision_obj):
        if self.rect_mask.colliderect(collision_obj.rect):
            collision_obj.assign_weapon(self)  # if collided, assigning weapon to player

    def attack_enemy(self, enemy):
        if self.rect_mask.colliderect(enemy.hitbox):
            pass

    def rotate(self):
        """Rotate the image of the sprite around a pivot point."""
        if self.angle >= 90 or self.angle < 0:
            self.counter = self.counter * (-1)
        # Rotate the image.
        self.image = pygame.transform.rotozoom(self.original_image, -self.angle, 1)
        # Rotate the offset vector.
        offset_rotated = self.offset.rotate(self.angle)
        # Create a new rect with the center of the sprite + the offset.
        self.rect = self.image.get_rect(center=self.game.player.hitbox.midright + offset_rotated)
        self.hitbox = self.getMaskRect(self.image, *self.rect.topleft)
        self.angle_change_factor = self.angle_change_factor * 1.02
        if not 0 > -self.angle > -90:
            self.angle_change_factor = self.angle_change_factor_start
            self.angle = 0
        self.angle -= self.angle_change_factor * self.counter
        '''Important to update mask'''
        # self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        if not self.is_finished:
            self.rotate()
        self.mask = pygame.mask.from_surface(self.image)
        # self.rect.bottomleft = self.game.player.hitbox.topright
        # self.rect_mask = self.getMaskRect(self.image, *self.rect.topleft)
        #
        # dx = self.rect_mask.x - self.game.player.hitbox.topright[0]
        # self.rect_mask.x -= dx
        # self.rect.x -= dx
        # self.hitbox = self.rect_mask
        # self.mask = pygame.mask.from_surface(self.image)

        pygame.Surface.blit(self.game.screen, self.image, self.rect, special_flags=pygame.BLEND_PREMULTIPLIED )
        pygame.draw.rect(self.game.screen, self.game.RED, self.hitbox, 1)
        pygame.draw.rect(self.game.screen, self.game.GREEN, self.rect, 1)
