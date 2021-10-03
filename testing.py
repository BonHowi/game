import pygame as pg
from pygame.math import Vector2


class Entity(pg.sprite.Sprite):

    def __init__(self, pos):
        super().__init__()
        self.image = pg.image.load('katana.png')  # pg.Surface((122, 70), pg.SRCALPHA)
        # pg.draw.polygon(self.image, pg.Color('dodgerblue1'),
        #  ((1, 0), (120, 35), (1, 70)))
        # A reference to the original image to preserve the quality.
        self.image = pg.transform.scale(self.image, (100, 100))
        self.orig_image = self.image
        self.rect = self.image.get_rect(center=pos)
          # The original center position/pivot point.
        self.offset = Vector2(4, -34)  # We shift the sprite 50 px to the right.
        self.angle = 0
        self.hitbox = self.getMaskRect(self.image, *self.rect.topleft)
        self.pos = Vector2(self.hitbox.midbottom)
        #self.pos[1] -=10
        #self.pos[0] -= 2
        #self.hitbox = getMaskRect(self.image, self.rect)

    def update(self):
        """

        :return:
        :rtype:
        """
        self.angle += 2
        self.rotate()

    def rotate(self):
        """

        :return:
        :rtype:
        """
        """Rotate the image of the sprite around a pivot point."""
        # Rotate the image.
        self.image = pg.transform.rotozoom(self.orig_image, -self.angle, 1)
        # Rotate the offset vector.
        offset_rotated = self.offset.rotate(self.angle)
        # Create a new rect with the center of the sprite + the offset.
        self.rect = self.image.get_rect(center=self.pos + offset_rotated)
        #self.hitbox = self.getMaskRect(self.image, *self.rect.topleft)

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
        surf_mask = pg.mask.from_surface(surf)
        rect_list = surf_mask.get_bounding_rects()
        surf_mask_rect = rect_list[0].unionall(rect_list)
        surf_mask_rect.move_ip(top, left)
        return surf_mask_rect


def main():
    screen = pg.display.set_mode((640, 480))
    clock = pg.time.Clock()
    entity = Entity((250, 250))
    all_sprites = pg.sprite.Group(entity)

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return

        keys = pg.key.get_pressed()
        if keys[pg.K_d]:
            entity.pos.x += 5
        elif keys[pg.K_a]:
            entity.pos.x -= 5

        all_sprites.update()
        screen.fill((30, 30, 30))
        all_sprites.draw(screen)
        pg.draw.circle(screen, (255, 128, 0), [int(i) for i in entity.pos], 3)
        #pg.draw.rect(screen, (255, 128, 0), entity.rect, 2)
        #pg.draw.rect(screen, (255, 0, 0), entity.hitbox, 1)
        pg.draw.line(screen, (100, 200, 255), (0, 240), (640, 240), 1)
        pg.display.flip()
        clock.tick(30)


if __name__ == '__main__':
    pg.init()
    main()
    pg.quit()
