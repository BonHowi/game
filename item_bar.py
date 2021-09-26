import pygame


class Items_bar(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.image = pygame.Surface((200, 50))
        self.image.fill(self.game.BROWN)
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 1400


    def render(self):
