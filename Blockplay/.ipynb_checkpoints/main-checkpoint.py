import random
import pygame

pygame.init()
screen = pygame.display.set_mode((1920, 1080), pygame.RESIZABLE)
pygame.display.set_caption("Blockplay")
clock = pygame.time.Clock()
running = True

x = 100
y = 500
menu = 1

class player:
    def __init__(self, id):
        self.x = 0 
        self.y = 0
        self.speed = 1
        self.jump_strength = 1
        self.id = id
        self.vis = 100
    def visible(self, v):
        self.vis = v

class camera:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.fov = 50

camera1 = camera()
player1 = player(1)
print("Hello World!")

def backround(width, height, tile_size):
    WIDTH, HEIGHT, TILE_SIZE = width, height, tile_size
    LIGHT_COLOR = (240, 217, 181)
    DARK_COLOR = (181, 136, 99)
    for x in range(0,WIDTH,TILE_SIZE):
        for y in range(0,HEIGHT,TILE_SIZE):
            row = y // TILE_SIZE
            col = x // TILE_SIZE
            if (row + col) % 2 == 0:
                color = LIGHT_COLOR
            else:
                color = DARK_COLOR
            pygame.draw.rect(screen, color, (x, y, TILE_SIZE, TILE_SIZE))

b1 = pygame.image.load('./Blockplay/textures/backround1.png').convert_alpha()
backround1 = pygame.transform.scale(b1, screen.get_size())

while running:
     #backround1 = pygame.transform.scale(b1, (1920, 1080))

    keys = pygame.key.get_pressed()
    # x += 5
    # if x > 1500:
    #    x = 100
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("Game stopped")
            running = False
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        x -= 5
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        x += 5
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        y += 5
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        y -= 5
    if menu == 1:
        pass
    for i in range(9):
        pass
    screen.fill("black")
    backround(1920,1080,100)
    #screen.blit(backround1, (0, 0))
    pygame.draw.rect(screen, (255,255,255), (x, y, 150, 150), 0)

    pygame.display.flip()
    clock.tick(60)
    
