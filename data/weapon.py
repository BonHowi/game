import pygame
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
        self.angle = 0
        self.offset = Vector2(6, -34)
        self.angle_change_factor = 3.5 * 1.5

    def get_mask_rect(self, surf, top=0, left=0):
        """Returns minimal bounding rectangle around image"""
        surf_mask = pygame.mask.from_surface(surf)
        rect_list = surf_mask.get_bounding_rects()
        surf_mask_rect = rect_list[0].unionall(rect_list)
        surf_mask_rect.move_ip(top, left)
        return surf_mask_rect

    def load_image(self):  # Change name of the function
        """Load weapon image and initialize instance variables"""
        self.original_image = pygame.image.load('../assets/weapon/' + self.name + '.png')
        self.original_image = pygame.transform.scale(self.original_image, (75, 75))
        self.mask = pygame.mask.from_surface(self.original_image)
        self.rect = self.mask.get_rect()
        self.rect_mask = self.get_mask_rect(self.original_image, *self.rect.topleft)
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

        # Termination condition
        if self.angle >= 180 or self.angle < 0:
            self.game.player.attacking = False
            self.angle = 0
            self.image = self.original_image.copy()
            self.rect = self.image.get_rect(
                center=self.game.player.hitbox.midright + self.offset)  # offset to fit as close as possible
            self.rect_mask = self.get_mask_rect(self.image, *self.rect.topleft)
        else:
            # Different angle and position, depending on player's direction
            if self.game.player.direction in ("RIGHT", "UP", "DOWN"):
                angle = -self.angle
                position = self.game.player.hitbox.midright
            else:
                angle = self.angle
                position = self.game.player.hitbox.midleft
            # Rotate the image.
            self.image = pygame.transform.rotozoom(self.original_image, angle, 1)
            # Rotate the offset vector.
            offset_rotated = self.offset.rotate(-angle)
            # Create a new rect with the center of the sprite + the offset.
            self.rect = self.image.get_rect(center=position + offset_rotated)

            self.rect_mask = self.get_mask_rect(self.image, *self.rect.topleft)
            # Update angle
            self.angle += self.angle_change_factor
            # Update mask
            self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        """Update weapon position and state"""
        # If player attacks with weapon, it rotates
        if self.game.player.attacking:
            self.rotate()
        # else, it just follows the player
        else:
            if self.game.player.direction in ("RIGHT", "UP", "DOWN"):
                self.image = pygame.transform.flip(self.original_image.copy(), True, False)
                self.rect = self.image.get_rect(
                    center=self.game.player.hitbox.midright + self.offset)  # offset to fit as close as possible
            else:
                self.image = self.original_image.copy()
                offset_new = self.offset + Vector2(-10, 0)  # update offset
                self.rect = self.image.get_rect(
                    center=self.game.player.hitbox.midleft + offset_new)

            self.rect_mask = self.get_mask_rect(self.image, *self.rect.topleft)
            self.mask = pygame.mask.from_surface(self.image)
        # Draw hitbox and rect
        # pygame.draw.rect(self.game.screen, self.game.RED, self.rect_mask, 1)
        # pygame.draw.rect(self.game.screen, self.game.GREEN, self.rect, 1)
