import pygame
import os
from weapon import Weapon

class Player(pygame.sprite.Sprite):
    def __init__(self, game, *groups):
        super().__init__(*groups)
        self.game = game
        self.animation_database = {"IDLE_LEFT":[],
                                   "IDLE_RIGHT":[],
                                   "WALK_LEFT":[],
                                   "WALK_RIGHT":[]}
        self.image_size = (75, 75)
        self.image = pygame.image.load("player/idle/right_idle0.png")
        self.image = pygame.transform.scale(self.image,self.image_size)
        self.rect = self.image.get_rect()  # Get rect of some size as 'image'.
        self.rect.x = self.game.SIZE[0] / 2
        self.rect.y = self.game.SIZE[1] / 2
        self.velocity = [0, 0]
        self.old_velocity = [0, 0]
        self.speed = 100
        self.priority = 1000
        self.score = 0
        self.direction = 'RIGHT'
        self.player_moving = False
        self.player_index = 0
        # Player Attacking
        self.attacking = False
        self.attack_range = pygame.Rect(0, 0, 0, 0)#zmienione tymczasowo
        self.hasWeapon = True
        self.weapon = Weapon(10, 'Gole piesci', 2, self.game.RED, self.game.all_environment)#usuniete groups z self.game
        self.hp = 100
        self.max_stamina = 1000
        self.current_stamina = self.max_stamina
        self.attacked = False
        ########GUN PROPERTIES, Moze tymczasowo########
        self.gun_length = 15
        self.gun_width = 5
        self.load_animation('player/')
        #hitbox
        self.hitbox = pygame.Rect(self.rect.x + 18, self.rect.y + 27, 40, 48)


    def load_animation(self, path):
        animation_states = os.listdir(path)
        for state in animation_states:
            substates = os.listdir(path+state)
            for ss in substates:
                image_loc = ss
                elements = image_loc.split('_')
                key = state.upper() +'_'+ elements[0].upper()#key to dictionary
                animation_image = pygame.image.load(path + state+ '/'+ image_loc).convert()
                animation_image = pygame.transform.scale(animation_image, self.image_size)
                self.animation_database[key].append(animation_image)

    def moving(self):
        if self.velocity[0] != 0 or self.velocity[1] != 0:
            return True
        else:
            return False

    def animation(self):
        if self.moving():
            self.player_index += 1.0/15 # how fast animation changes
            if self.player_index >= 4:
                self.player_index = 0
            if self.direction == 'LEFT':
                self.image = self.animation_database["WALK_LEFT"][int(self.player_index)]

            elif self.direction == 'UP':
                self.image = self.animation_database["WALK_RIGHT"][int(self.player_index)]

            elif self.direction == "RIGHT":
                self.image = self.animation_database["WALK_RIGHT"][int(self.player_index)]

            elif self.direction == "DOWN":
                self.image = self.animation_database["WALK_RIGHT"][int(self.player_index)]
        else:#if idle
            self.player_index += 1.0/15  # how fast animation changes
            if self.player_index >= 4:
                self.player_index = 0
            if self.direction == 'LEFT':
                self.image = self.animation_database["IDLE_LEFT"][int(self.player_index)]
            elif self.direction == 'RIGHT':
                self.image = self.animation_database["IDLE_RIGHT"][int(self.player_index)]
            elif self.direction == "UP":
                self.image = self.animation_database["IDLE_RIGHT"][int(self.player_index)]
            elif self.direction == "DOWN":
                self.image = self.animation_database["IDLE_RIGHT"][int(self.player_index)]



    def attack(self, collision_obj):
        if self.attacking and self.hasWeapon and self.current_stamina >= 1000:
            if self.direction == 'RIGHT':
                self.attack_range = pygame.Rect(self.rect.x + self.rect.width, self.rect.y,
                                                self.weapon.blade_length + 100, self.rect.height)
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


    def attack_collision(self, collision_obj):#do zmiany
        if self.attack_range.colliderect(collision_obj.rect):
            self.calculate_collison(collision_obj, self.weapon.damage)

    def calculate_collison(self, collision_obj, damage):
        if collision_obj.hp > 0:
            collision_obj.hp -= damage
            collision_obj.hurt = True #indicating that enemy is hurt
            if collision_obj.hp <= 0:
                self.score += 1
        self.attacked = True

    def update(self):
        self.animation()
        self.rect.clamp_ip(self.game.screen_rect)
        self.rect.move_ip(*self.velocity)
        if self.current_stamina < self.max_stamina:
            self.current_stamina += 10
        self.attacked = False
        self.hitbox = pygame.Rect(self.rect.x + 19, self.rect.y + 25, 37, 50)

        #pygame.draw.rect(self.game.screen, (255, 0, 0), self.rect, 1)
        #pygame.draw.rect(self.game.screen, (255, 0, 0), self.hitbox)


    def render(self):
        if self.hasWeapon:
            pygame.draw.rect(self.game.screen, self.weapon.color, self.attack_range)


        katana_image = pygame.image.load("weapon/katana.png")
        katana_image = pygame.transform.scale(katana_image, (100, 100))
        self.game.screen.blit(katana_image, (-10, 500))

        start = pygame.math.Vector2(self.rect.midright)
        mouse = pygame.mouse.get_pos()
        end = start + (mouse - start).normalize() * self.gun_length
        #pygame.draw.lines(self.game.screen, (255, 255, 255), False, (start, end), width=self.gun_width)

    def gun_point(self):#zmienic, bo brzydko
        start = pygame.math.Vector2(self.rect.midright)
        mouse = pygame.mouse.get_pos()
        end = start + (mouse - start).normalize() * self.gun_length
        return end

    def assign_weapon(self, weapon: Weapon):
        self.weapon = weapon
        self.hasWeapon = True

    def gun_line(self,ax, ay, bx, by, radius):
        pass

