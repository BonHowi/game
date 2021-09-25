class PlayerInfo:
    def __init__(self, game, pos):
        self.game = game
        self.pos = pos
        self.coordinates = None
        self.space_between = 20

        self.hp_text = None
        self.weapon_text = None
        self.damage_text = None
        self.stamina_text = None

        self.hp_text_rect = None
        self.stamina_text_rect = None
        self.weapon_text_rect = None
        self.damage_text_rect = None

    def render(self):
        self.game.screen.blit(self.coordinates, (0, 0))
        self.game.screen.blit(self.hp_text, self.hp_text_rect)
        self.game.screen.blit(self.weapon_text, self.weapon_text_rect)
        self.game.screen.blit(self.damage_text, self.damage_text_rect)
        self.game.screen.blit(self.stamina_text, self.stamina_text_rect)

    def update(self):
        self.coordinates = self.game.myfont.render('SCORE: ' + str(self.game.player.score), False, (255, 0, 0))
        self.hp_text = self.game.myfont.render("HP: " + str(self.game.player.hp),
                                               False, self.game.GREEN)
        self.weapon_text = self.game.myfont.render("Weapon: " + str(self.game.player.weapon.name),
                                                   False, self.game.GREEN)
        self.damage_text = self.game.myfont.render("Damage: " + str(self.game.player.weapon.damage),
                                                   False, self.game.GREEN)
        self.stamina_text = self.game.myfont.render("Stamina: " + str(self.game.player.current_stamina),
                                                    False, self.game.GREEN)

        self.hp_text_rect = self.weapon_text.get_rect(center=(self.pos[0], self.pos[1]))
        self.stamina_text_rect = self.weapon_text.get_rect(center=(self.pos[0], self.pos[1] + self.space_between))
        self.weapon_text_rect = self.weapon_text.get_rect(center=(self.pos[0], self.pos[1] + 2 * self.space_between))
        self.damage_text_rect = self.weapon_text.get_rect(center=(self.pos[0], self.pos[1] + 3 * self.space_between))