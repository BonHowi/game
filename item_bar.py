import pygame
from weapon import Weapon

class Items_bar(pygame.sprite.Sprite):
    def __init__(self, game ):
        super().__init__()
        self.game = game
        self.image = pygame.Surface((200, 50))
        self.image.fill(self.game.BROWN)
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 530
        self.weapon = ''


    def add_weapon(self, weapon):
        pass

    def draw_weapons(self):
        pygame.draw.rect(self.game.screen, self.game.WHITE, (20, 540, 50, 50))
        pygame.draw.rect(self.game.screen, self.game.BLUE, (80, 540, 50, 50))
        pygame.draw.rect(self.game.screen, self.game.BLACK, (140, 540, 50, 50))

        if self.weapon == 'katana':
            pygame.draw.rect(self.game.screen, self.game.RED, (20, 540, 50, 50), width=5)
        elif self.weapon == 'sword':
            pygame.draw.rect(self.game.screen, self.game.RED, (80, 540, 50, 50),width=5)
        elif self.weapon == 'kij':
            pygame.draw.rect(self.game.screen, self.game.RED, (140, 540, 50, 50), width=5)
        else:
            pass

    def draw(self):
        s = pygame.Surface((200, 70))  # the size of your rect
        s.set_alpha(128)  # alpha level
        s.fill(self.game.BROWN)  # this fills the entire surface
        self.game.screen.blit(s, ( self.rect.x,  self.rect.y))
        self.draw_weapons()



