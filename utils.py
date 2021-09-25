class PlayerInfo:
    def __init__(self, player, surface, font, cock, color, pos):
        self.player = player
        self.surface = surface
        self.font = font
        self.clock = cock
        self.pos = pos
        self.color = color
        self.space_between = 20

        self.hp_text = self.font.render("HP: " + str(player.hp), False, self.color)
        self.weapon_text = self.font.render("Weapon: " + str(player.weapon.name), False, self.color)
        self.damage_text = self.font.render("Damage: " + str(player.weapon.damage), False, self.color)
        self.stamina_text = self.font.render("Stamina: " + str(player.current_stamina), False, self.color)

        self.hp_text_rect = self.weapon_text.get_rect(center=(self.pos[0], self.pos[1]))
        self.stamina_text_rect = self.weapon_text.get_rect(center=(self.pos[0], self.pos[1] + self.space_between))
        self.weapon_text_rect = self.weapon_text.get_rect(center=(self.pos[0], self.pos[1] + 2 * self.space_between))
        self.damage_text_rect = self.weapon_text.get_rect(center=(self.pos[0], self.pos[1] + 3 * self.space_between))

    def render(self):
        self.surface.blit(self.hp_text, self.hp_text_rect)
        self.surface.blit(self.weapon_text, self.weapon_text_rect)
        self.surface.blit(self.damage_text, self.damage_text_rect)
        self.surface.blit(self.stamina_text, self.stamina_text_rect)

    def update(self):
        text = "Weapon: " + str(self.player.weapon.name)
        self.weapon_text = self.font.render(text, False, self.color)
        self.weapon_text_rect = self.weapon_text.get_rect(center=(self.pos[0], self.pos[1]))
