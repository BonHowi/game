import pygame
import os
'''Parent class for characters'''
class Entity(pygame.sprite.Sprite):
    def __init__(self, game, *groups):
        super().__init__(*groups)
        self.animation_database = {"IDLE_LEFT": [],
                                   "IDLE_RIGHT": [],
                                   "WALK_LEFT": [],
                                   "WALK_RIGHT": []}




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
