import random
import pygame


class Wall(pygame.sprite.Sprite):
    def __init__(self, game, *groups):
        super().__init__(*groups)
        self.game = game
        if random.randint(1, 2) % 2:
            wall = (random.randint(40, 100), random.randint(5, 15))
        else:
            wall = (random.randint(5, 15), random.randint(40, 200))
        self.image = pygame.Surface(wall)
        self.image.fill(game.WHITE)
        self.rect = self.image.get_rect()
        x = random.randint(100, game.SIZE[0] - 100)
        y = random.randint(100, game.SIZE[1] - 100)
        self.rect.x = x
        self.rect.y = y


class FPSCounter:
    def __init__(self, game, surface, font, cock, color, pos):
        self.game = game
        self.surface = surface
        self.font = font
        self.clock = cock
        self.pos = pos
        self.color = color
        self.fps_text = self.font.render(str(int(60)) + "FPS", False, self.color)
        self.fps_text_rect = self.fps_text.get_rect(center=(self.pos[0], self.pos[1]))

    def render(self):
        self.surface.blit(self.fps_text, self.fps_text_rect)

    def update(self):
        text = f"{60:2.0f} FPS"
        self.fps_text = self.font.render(text, False, self.color)
        self.fps_text_rect = self.fps_text.get_rect(center=(self.pos[0], self.pos[1]))

