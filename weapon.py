import pygame


class Weapon(pygame.sprite.Sprite):
    def __init__(self, game, damage, name, width, color,*groups):
        super().__init__(*groups)
        self.width = width
        self.damage = damage
        self.name = name
        self.blade_length = int(width)
        self.color = color
        self.image = None
        self.mask = None
        self.rect = None
        self.rect_mask = None
        self.game = game
        self.load_image()

    def getMaskRect(self, surf, top=0, left=0):
        surf_mask = pygame.mask.from_surface(surf)
        rect_list = surf_mask.get_bounding_rects()
        surf_mask_rect = rect_list[0].unionall(rect_list)
        surf_mask_rect.move_ip(top, left)
        return surf_mask_rect

    def load_image(self):
        self.image = pygame.image.load('weapon/' + self.name + '.png')
        self.image = pygame.transform.scale(self.image, (75, 75))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.mask.get_rect()
        self.rect_mask = self.getMaskRect(self.image, *self.rect.topleft)


    def collision(self, collision_obj):
        if self.rect.colliderect(collision_obj.rect):
            collision_obj.assign_weapon(self)  # if collided, assigning weapon to player

    def update(self):
        self.rect.midleft = self.game.player.hitbox.topright
        self.rect_mask = self.getMaskRect(self.image, *self.rect.topleft)
        dx = self.rect_mask.x - self.game.player.hitbox.midright[0]
        self.rect_mask.x -= dx
        self.rect.x -= dx
        pygame.Surface.blit(self.game.screen, self.image, self.rect)
        pygame.draw.rect(self.game.screen, self.game.RED, self.rect_mask, 1)
        pygame.draw.rect(self.game.screen, self.game.GREEN, self.rect, 1)
