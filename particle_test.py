import pygame

class ParticleTest:
    def __init__(self, game):
        self.particles = []
        self.game = game

    def emit(self):
        if self.particles:
            self.delete_particles()
            for particle in self.particles:
                particle[0][1] += particle[2]
                particle[1] -= 0.2
                pygame.draw.circle(self.game.screen, pygame.Color('WHITE'), particle[0], particle[1])

    def add_particles(self):
        pos_x = 250
        pos_y = 250
        radius = 10
        direction = -3
        particle_circle = [[pos_x, pos_y], radius, direction]
        self.particles.append(particle_circle)

    def delete_particles(self):
        particle_copy = [particle for particle in self.particles if particle[1] > 0]
        self.particles = particle_copy

