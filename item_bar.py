import pygame


class Items_bar(pygame.sprite.Sprite):
    def __init__(self, game ):
        super().__init__()
        self.game = game
        self.image = pygame.Surface((200, 50))
        self.image.fill(self.game.BROWN)
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 500


    def draw(self):
        s = pygame.Surface((250, 100))  # the size of your rect
        s.set_alpha(128)  # alpha level
        s.fill(self.game.BROWN)  # this fills the entire surface
        self.game.screen.blit(s, ( self.rect.x,  self.rect.y))  # (0,0) are the top-left coordinates