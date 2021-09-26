import pygame

from weapon import Weapon


class Player(pygame.sprite.Sprite):
    def __init__(self, game, *groups):
        super().__init__(*groups)
        self.game = game
        self.image = pygame.Surface((10, 10))
        self.image.fill(self.game.BROWN)
        self.rect = self.image.get_rect()  # Get rect of some size as 'image'.
        self.rect.x = self.game.SIZE[0] / 2
        self.rect.y = self.game.SIZE[1] / 2
        self.velocity = [0, 0]
        self.old_velocity = [0, 0]
        self.speed = 100
        self.priority = 1000
        self.score = 0
        # Player Attacking
        self.direction = ''
        self.attacking = False
        self.attack_range = pygame.Rect(0, 0, 0, 0)
        self.hasWeapon = False
        self.weapon = Weapon(0, 'Gole piesci', 2, self.game.RED, 35000, 50000, self.game.all_environment)#usuniete groups z self.game
        self.hp = 100
        self.max_stamina = 1000
        self.current_stamina = self.max_stamina
        self.attacked = False
        ########GUN PROPERTIES, Moze tymczasowo########
        self.gun_length = 25
        self.gun_width = 5



    def attack(self, collision_obj):
        if self.attacking and self.hasWeapon and self.current_stamina >= 1000:
            if self.direction == 'RIGHT':
                self.attack_range = pygame.Rect(self.rect.x + self.rect.width, self.rect.y,
                                                self.weapon.blade_length, self.rect.height)
                self.attack_collision(collision_obj)
            elif self.direction == 'LEFT':
                self.attack_range = pygame.Rect(self.rect.x - self.weapon.blade_length, self.rect.y,
                                                self.weapon.blade_length, self.rect.height)
                self.attack_collision(collision_obj)
            elif self.direction == 'UP':
                self.attack_range = pygame.Rect(self.rect.x, self.rect.y - self.weapon.blade_length, self.rect.height,
                                                self.weapon.blade_length)
                self.attack_collision(collision_obj)
            elif self.direction == 'DOWN':
                self.attack_range = pygame.Rect(self.rect.x, self.rect.y + self.rect.height, self.rect.height,
                                                self.weapon.blade_length)
                self.attack_collision(collision_obj)
        else:
            self.attack_range = pygame.Rect(0, 0, 0, 0)

    def attack_collision(self, collision_obj):
        if self.attack_range.colliderect(collision_obj.rect):
            self.calculate_collison(collision_obj, self.weapon.damage)

    def calculate_collison(self, collision_obj, damage):
        if collision_obj.hp > 0:
            collision_obj.hp -= damage
            if collision_obj.hp <= 0:
                self.score += 1
        self.attacked = True

    def update(self):
        self.rect.clamp_ip(self.game.screen_rect)
        self.rect.move_ip(*self.velocity)
        if self.current_stamina < self.max_stamina:
            self.current_stamina += 10
        self.attacked = False

    def render(self, display):
        if self.hasWeapon:
            pygame.draw.rect(display, self.weapon.color, self.attack_range)
        ####render broni##### poprawic, zeby kule strzelaly z koncowki broni a nie ze srodka playera
        start = pygame.math.Vector2(self.rect.center)
        mouse = pygame.mouse.get_pos()
        end = start + (mouse - start).normalize() * self.gun_length
        pygame.draw.lines(self.game.screen, (255, 255, 255), False, (start, end), width=self.gun_width)

    def gun_point(self):#zmienic, bo brzydko
        start = pygame.math.Vector2(self.rect.center)
        mouse = pygame.mouse.get_pos()
        end = start + (mouse - start).normalize() * self.gun_length
        return end

    def assign_weapon(self, weapon: Weapon):
        self.weapon = weapon
        self.hasWeapon = True

    def gun_line(self,ax, ay, bx, by, radius):
        pass
