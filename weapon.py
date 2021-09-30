import pygame
from particles import Particle
from pygame.math import Vector2

class Weapon(pygame.sprite.Sprite):
    def __init__(self, game, damage, name, width, color,*groups):
        super().__init__(*groups)
        self.width = width
        self.damage = damage
        self.name = name
        self.blade_length = int(width)
        self.color = color
        self.original_image = None
        self.image2 = None
        self.mask = None
        self.rect = None
        self.rect_mask = None
        self.hitbox = None
        self.game = game
        self.load_image()
        self.counter = 1
        self.angle = 0
        self.pivot = self.rect_mask.bottomleft


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
        self.image2 = self.original_image

    def collision(self, collision_obj):
        if self.rect_mask.colliderect(collision_obj.rect):
            collision_obj.assign_weapon(self)  # if collided, assigning weapon to player

    def attack_enemy(self, enemy):
        if self.rect_mask.colliderect(enemy.hitbox):
            pass

    def rotatePivoted(self):

        if self.angle <= -90 or self.angle >=1:
            self.counter = self.counter * (-1)

        self.image2 = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image2.get_rect()
        self.rect.center = self.pivot

    def blitRotate(self, surf, image, origin, pivot, angle):
        image_rect = image.get_rect(topleft=(origin[0] - pivot[0], origin[1] - pivot[1]))
        offset_center_to_pivot = pygame.math.Vector2(origin) - image_rect.center
        rotated_offset = offset_center_to_pivot.rotate(-angle)
        rotated_image_center = (origin[0] - rotated_offset.x, origin[1] - rotated_offset.y)
        rotated_image = pygame.transform.rotate(image, angle)
        rotated_image_rect = rotated_image.get_rect(center=rotated_image_center)
        surf.blit(rotated_image, rotated_image_rect)

    def update(self):

        self.rotatePivoted()
        self.rect.bottomleft = self.game.player.hitbox.topright
        self.rect_mask = self.getMaskRect(self.image2, *self.rect.topleft)

        dx = self.rect_mask.x - self.game.player.hitbox.topright[0]
        self.rect_mask.x -= dx
        self.rect.x -= dx
        self.hitbox = self.rect_mask
        self.mask = pygame.mask.from_surface(self.image2)

        pygame.Surface.blit(self.game.screen, self.image2, self.rect)
        pygame.draw.rect(self.game.screen, self.game.RED, self.hitbox, 1)
        pygame.draw.rect(self.game.screen, self.game.GREEN, self.rect, 1)

        self.angle -=1.5 * self.counter
        self.pivot = self.rect_mask.bottomleft
