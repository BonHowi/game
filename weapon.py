import pygame


class Weapon(pygame.sprite.Sprite):#usuniete groups
    def __init__(self, damage, name, width, color, x, y,*groups):
        super().__init__(*groups)
        self.width = width
        self.damage = damage
        self.name = name
        self.blade_length = int(width)
        self.color = color
        self.image = pygame.Surface((20, 20))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def collision(self, collision_obj):
        if self.rect.colliderect(collision_obj.rect):
            collision_obj.assign_weapon(self)  # if collided, assigning weapon to player
