import random
import pygame
import math

pygame.init()
screen = pygame.display.set_mode((1920, 1080), pygame.RESIZABLE)
pygame.display.set_caption("Blockplay")
clock = pygame.time.Clock()
running = True

width,height=screen.get_size()
x = 100
y = 500
scale = 1
menu = 1
mouse1 = 0
font = pygame.font.SysFont(None, 32)
buttonfont = pygame.font.SysFont(None, 64)
exitfont = pygame.font.SysFont(None, 128)

class mouse_():
    def __init__(self):
        self.pos = (0,0)
        self.x = self.pos[0]
        self.y = self.pos[1]
    def update(self):
        self.pos = pygame.mouse.get_pos()
        self.x = self.pos[0]
        self.y = self.pos[1]
    def pressed(self,button):
        if events.type == pygame.MOUSEBUTTONDOWN:
            if events.button == 1:
                return True
        if events.type == pygame.MOUSEBUTTONUP:
            if events.button == 1:
                return False
mouse = mouse_()

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

class platform:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.pos = 0

class button:
    def __init__(self, texture_path, size_x, size_y):
        self.path = texture_path
        self.sizex = size_x
        self.sizey = size_y
        self.out_original = pygame.image.load(self.path).convert_alpha()
        self.lscale = 1
        self.pos = (0, 0)
    
    def update(self,x,y):
        self.pos = (midx+x-((self.sizex*self.lscale)/2), midy-y-(self.sizey*self.lscale)/2) 

    def hitbox(self,input):
        temp_rect = pygame.Rect(self.pos[0], self.pos[1], self.sizex*self.lscale,self.sizey*self.lscale) 
        return temp_rect.collidepoint(input)
            
    def show(self,x,y,responsive):
        self.update(x,y)
        if self.hitbox(mouse.pos) and responsive==1:
            self.lscale = 1.05
        else:
            self.lscale = 1
        self.out = pygame.transform.scale(self.out_original, (self.sizex*self.lscale,self.sizey*self.lscale))
        screen.blit(self.out, self.pos)
    
    def text(self,x,y,text):
        output = buttonfont.render(text, True, (255, 255, 255))
        text_rect = output.get_rect()
        button_center_x = self.pos[0] + (self.sizex * self.lscale) / 2
        button_center_y = self.pos[1] + (self.sizey * self.lscale) / 2
    
        text_rect.center = (button_center_x, button_center_y)
        screen.blit(output, text_rect) # text_rect

    def click(self,x,y,input):
        self.update(x,y)
        if input == 1 and self.hitbox(mouse.pos):
            return True
        else:
            return False
#and self.hitbox(mouse.pos)


camera1 = camera()
player1 = player(1)
button1 = button('./Blockplay/textures/pixel-48x16.png',400,100)
button2 = button('./Blockplay/textures/pixel-48x16.png',400,100)
print("Hello World!")

def update():
    global width,height
    width,height=screen.get_size()
    mouse.update()


def mid():
    global midx,midy
    midx = width/2
    midy = height/2

    

def backround(width, height, tile_size):
    WIDTH, HEIGHT, TILE_SIZE = width, height, int(tile_size*scale)
    LIGHT_COLOR = (151, 212, 38)
    DARK_COLOR = (167, 233, 43)
    
    offset_x = (width % TILE_SIZE) // 2
    offset_y = (height % TILE_SIZE) // 2

    for x in range(offset_x-TILE_SIZE,(WIDTH-offset_x)+TILE_SIZE,TILE_SIZE):
        for y in range(offset_y-TILE_SIZE,(HEIGHT-offset_y)+TILE_SIZE,TILE_SIZE):
            row = y // TILE_SIZE
            col = x // TILE_SIZE
            if (row + col) % 2 == 0:
                color = LIGHT_COLOR
            else:
                color = DARK_COLOR
            pygame.draw.rect(screen, color, (x, y, TILE_SIZE, TILE_SIZE))

def backround2():
    pygame.draw.rect(screen, (38, 171, 212), (0, 0, width, height), 0)

def quit():
    global running
    print("Game stopped")
    running = False

def quitscreen():
    global quit_confirm
    print("check")
    while quit_confirm == 1:
        width,height=screen.get_size()
        mid()
        screen.fill("black")
        msg = exitfont.render("Beenden? (J/N)", True, (255, 0, 0))
        msg_rect = msg.get_rect(center=(midx, midy))
        screen.blit(msg, msg_rect)
        for event in pygame.event.get():
                pass
        keys = pygame.key.get_pressed()
        if keys[pygame.K_j]:
            quit()
            quit_confirm = 0 
        if keys[pygame.K_n]:
            quit_confirm = 0
        pygame.display.flip()
        clock.tick(30)

b1 = pygame.image.load('./Blockplay/textures/backround1.png').convert_alpha()
sho = pygame.image.load('./Blockplay/textures/pixel-48x16.png').convert_alpha()
backround1 = pygame.transform.scale(b1, screen.get_size())

while running:
    update()
    mouse.pos = pygame.mouse.get_pos()
    mid()
    sh = pygame.transform.scale(sho, (300, 100))

    keys = pygame.key.get_pressed()
    # x += 5
    # if x > 1500:
    #    x = 100
    for event in pygame.event.get():
        global events
        events = event
        if event.type == pygame.QUIT:
            quit()
        if event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            width, height = event.w, event.h
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse1 = 1
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                mouse1 = 0    
       

    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        x -= 5
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        x += 5
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        y += 5
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        y -= 5
    if keys[pygame.K_b]:
        menu = 1


    if menu == 1:

        backround(width,height,120)
        button1.show(0,-120,1)
        button1.text(0,-120,"Start")
        button2.show(0,-240,1)
        button2.text(0,-240,"Exit")

        if button1.click(0,-120,mouse.pressed(1)):
            menu = 2
        if button2.click(0,-240,mouse.pressed(1)):
            quit_confirm = 1
            quitscreen()
            
            
            

    if menu == 2:
        backround2()

    #button1.show(0,0,1)    
    
    #screen.blit(backround1, (0, 0))
    #pygame.draw.rect(screen, (255,255,255), (x, y, 150, 150), 0)
    #button1.show(0,0,1)
    #screen.blit(sh, (midx-150, 700))
    #text_surface = font.render(str(mouse.pos), True, (255, 255, 255))
    #screen.blit(text_surface, (100, 100))                           
    pygame.display.flip()
    clock.tick(60)
    
#6e4d32