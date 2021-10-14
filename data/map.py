import pygame, csv, os



class Spritesheet(object):
    def __init__(self, filename):
        self.sheet = pygame.image.load(filename).convert_alpha()

    # Load a specific image from a specific rectangle
    def image_at(self, rectangle, colorkey=None):
        "Loads image from x,y,x+offset,y+offset"
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert_alpha()
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image

    # # Load a whole bunch of images and return them as a list
    # def images_at(self, rects, colorkey=None):
    #     "Loads multiple images, supply a list of coordinates"
    #     return [self.image_at(rect, colorkey) for rect in rects]
    #
    # # Load a whole strip of images
    # def load_strip(self, rect, image_count, colorkey=None):
    #     "Loads a strip of images and returns them as a list"
    #     tups = [(rect[0] + rect[2] * x, rect[1], rect[2], rect[3])
    #             for x in range(image_count)]
    #     return self.images_at(tups, colorkey)


class Tile(pygame.sprite.Sprite):
    def __init__(self, rectangle, x, y, spritesheet):
        pygame.sprite.Sprite.__init__(self)
        self.image = spritesheet.image_at(rectangle)
        self.image = pygame.transform.scale(self.image, (64, 64))
        # Manual load in: self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))


class TileMap():
    def __init__(self, game, filename, spritesheet):
        self.game = game
        self.tile_size = 64
        self.spritesheet = spritesheet
        self.start_x, self.start_y = 0, 0
        self.tiles = self.load_tiles(filename)
        self.map_surface = pygame.Surface((1200, 11*64))
        self.map_surface.set_colorkey((0, 0, 0))
        self.load_map()

    def draw_map(self, surface):
        surface.blit(self.map_surface, (0, 0))
        for tile in self.tiles:
            pygame.draw.rect(self.game.screen, (255, 0, 0), tile.rect, 1)

    def load_map(self):
        for tile in self.tiles:
            tile.draw(self.map_surface)

    def read_csv(self, filename):
        map = []
        with open(os.path.join(filename)) as data:
            data = csv.reader(data, delimiter=',')
            for row in data:
                map.append(list(row))
        return map

    def location(self, number):
        a = number // 15
        b = number % 15
        x = b * 16, a * 16
        return x

    def load_tiles(self, filename):
        tiles = []
        map = self.read_csv(filename)
        x, y = 0, -64
        for row in map:
            x = -32
            for tile in row:
                tiles.append(Tile((*self.location(int(tile)), 16, 16), x, y, self.spritesheet))
                if int(tile) in (135, 15, 17, 60, 61, 62, 63, 1):
                    self.game.wall_list.append(tiles[-1])
                # Move to next tile in current row
                x += 64

            # Move to next row
            y += 64
            # Store the size of the tile map
        return tiles
