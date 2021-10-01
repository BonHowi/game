import pygame
pygame.init()

#Colors

white = (255,255,255)
green = (0,255,0)
blue = (0,0,255)


display_width, display_height = 800, 600
screen = pygame.display.set_mode((display_width, display_height))
screen.fill(white)

class Player():
    def __init__(self, x, y, color):
        self.player_surface = screen
        self.player_color = color
        self.player_radius = 25
        self.playerx = x
        self.playery = y
        self.player_width = 0
        self.speed = 0.1
        self.velocity = [0,0]

    def move(self):
        self.playerx +=self.velocity[0]
        self.playery += self.velocity[1]

    def draw(self):
        self.player_character = pygame.draw.circle(self.player_surface, self.player_color, (self.playerx, self.playery), self.player_radius, self.player_width)

    def input(self, event, dt):
    #for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                self.velocity[1] = -self.speed * dt
            elif event.key == pygame.K_s:
                self.velocity[1] = self.speed * dt
            elif event.key == pygame.K_a:
                self.velocity[0] = -self.speed * dt
            elif event.key == pygame.K_d:
                self.velocity[0] = self.speed * dt
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_w or event.key == pygame.K_s:
                self.velocity[1] = 0
            elif event.key == pygame.K_a or event.key == pygame.K_d:
                self.velocity[0] = 0
            print(event.key)

running = True

clock = pygame.time.Clock()
player = Player(250, 250, green)
player2 = Player(100, 100, blue)

while running:
    dt = clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print(event.type)
            running = False
        else:
            player.input(event, dt)


    screen.fill(white)

    player.move()
    player.draw()

    pygame.display.update()
