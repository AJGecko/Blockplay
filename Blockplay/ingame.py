import pygame
import essentials as es
import random
from pathlib import Path

midx,midy,width,height,events,scale = es.basis()
screen = pygame.display.get_surface()
font = pygame.font.SysFont(None, 32)
platform_texture = pygame.image.load('./Blockplay/textures/pixel-64x128.png').convert_alpha()

player_dir = Path("./Blockplay/textures/player")
player_entries = player_dir.iterdir()
folders = []
for p in player_entries:
    if p.is_dir():
        folders.append(p)
folder_names = []
for p in folders:
    folder_names.append(p.name)
folder_names.sort()
print(folder_names)

player_texture = []
for p in folder_names:
    out = []
    for png_file in sorted(Path("./Blockplay/textures/player/" + p).glob("*.png")):
        out.append(pygame.image.load(str(png_file)).convert_alpha())
    player_texture.append(out)

print(player_texture)

gen = 1
jump = 0
can_jump = 0
camy_storage = 0
cp = 0
gravity = 1
last_collision_index = -1

class camera:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.fov = 1

class player:
    def __init__(self, id, skin):
        self.x = 0 
        self.y = 0
        self.sizex = 100
        self.sizey = 100
        self.pos = (self.x,self.y)
        self.speed = 1
        self.jump_strength = 1
        self.id = id
        self.lscale = 1
        self.vis = 1
        self.skin = skin
        self.direction = 0
        self.gravity = 1
    def visible(self, v):
        self.vis = v
    def show(self):
        #lt stands for local texture
        lt = player_texture[folder_names.index(self.skin)]
        lt1 = lt[0]
        lt2 = lt[1]
        lt3 = lt[2]
        if self.direction == 0:
            self.out = lt1
        if self.direction == 1:
            self.out = lt2
        if self.direction == -1:
            self.out = lt3
        self.out2 = pygame.transform.scale(self.out, (self.sizex*self.lscale,self.sizey*self.lscale))
        self.out_rect = self.out2.get_rect(center=(midx+self.x, midy+self.y))
        if self.vis == 1:
            screen.blit(self.out2, self.out_rect)
    def update(self,x,y,lscale):
        self.x = x
        self.y = y
        self.pos = (self.x,self.y)
        self.lscale = lscale 

class platform:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.pos = (self.x,self.y)
        self.lscale = 1
        self.sizex = 200
        self.sizey = 400
        self.location = 1
        self.vis = 1
    def show(self):
        global platform_texture
        self.out1 = platform_texture
        self.out2 = pygame.transform.scale(self.out1, (self.sizex*self.lscale,self.sizey*self.lscale))
        self.out_rect = self.out2.get_rect(center=(midx+self.x, midy+self.y))
        if self.vis == 1:
            screen.blit(self.out2, self.out_rect)
    def update(self,x,y,lscale):
        self.x = x
        self.y = y
        self.pos = (self.x,self.y)
        self.lscale = lscale 
    def updateauto(self):
        self.x = (platformpositions_x[self.location]-cam.x)*scale*cam.fov
        self.y = (platformpositions_y[self.location]+cam.y)*scale*cam.fov
        self.lscale = scale
        if (platformpositions_x[self.location]-cam.x)*scale*cam.fov < -1200:
            if self.location + 7 <= (len(platformpositions_x)-1):
                self.location = self.location + 7
        if (platformpositions_x[self.location]-cam.x)*scale*cam.fov > -100 and (platformpositions_x[self.location]-cam.x)*scale*cam.fov < 100:
            global cp 
            cp = self.location


cam = camera()
player1 = player(1,"green")
p1 = platform()
p2 = platform()
p3 = platform()
p4 = platform()
p5 = platform()
p6 = platform()
p7 = platform()

def backround():
    pygame.draw.rect(screen, (38, 171, 212), (0, 0, width, height), 0)

def generate(number, multiplier):
    platformpositions_x = []
    platformpositions_y = []
    x = 0
    y = 0
    for i in range(number):
        platformpositions_x.insert(i,x)
        x = x + 110*multiplier + random.randint(30*multiplier,200*multiplier)
        platformpositions_y.insert(i,y)
        y = y + random.randint(-60*multiplier,60*multiplier)
    return platformpositions_x, platformpositions_y

def game(number):
    global midx,midy,width,height,events,scale,font,platform_texture,gravity,last_collision_index
    midx,midy,width,height,events,scale = es.basis()
    global gen, p1, p2, p3, p4, p5, menu, jump, can_jump, camy_storage
    if gen == 1:
        global platformpositions, platformpositions_x, platformpositions_y
        platformpositions = generate(number,2)
        print(platformpositions)
        platformpositions_x = platformpositions[0]
        platformpositions_y = platformpositions[1]
        cam.x = 0
        cam.y = 400
        p1.location = 0
        p2.location = 1
        p3.location = 2
        p4.location = 3
        p5.location = 4
        p6.location = 5
        p7.location = 6
        gen = 0
        jump = 0
        can_jump = 0
    
    #steering
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        player1.direction = -1
        cam.x -= 5
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        player1.direction = 1
        cam.x += 5
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        cam.y -= 2
    if not keys[pygame.K_LEFT] and not keys[pygame.K_a] and not keys[pygame.K_RIGHT] and not keys[pygame.K_d]:
        player1.direction = 0

    #jump
    if (keys[pygame.K_UP] or keys[pygame.K_w] or keys[pygame.K_SPACE]) and can_jump == 1:
        jump = 1
        can_jump = 0
        camy_storage = cam.y
        player1.gravity = 0
    elif jump == 0:
        if player1.gravity + 0.10 > 1:
            player1.gravity = 1
        else:
            player1.gravity += 0.10

    if jump == 1:
        cam.y += 5
        if cam.y - camy_storage >= 300:
            jump = 0

    #hitbox (collision check)
    player_world_x = cam.x + (player1.x / scale / cam.fov)
    player_world_y = (player1.y / scale / cam.fov) - cam.y
    player_rect = pygame.Rect(
        int(player_world_x - player1.sizex / 2),
        int(player_world_y - player1.sizey / 2),
        int(player1.sizex),
        int(player1.sizey),
    )
    for i in range(number):
        platform_rect = pygame.Rect(
            int(platformpositions_x[i] - 200 / 2),
            int(platformpositions_y[i] - 400 / 2),
            200,
            400,
        )
        if player_rect.colliderect(platform_rect):
            landing_overlap = player_rect.bottom - platform_rect.top
            if -30 <= landing_overlap <= 40:
                min_overlap = min(player_rect.right, platform_rect.right) - max(player_rect.left, platform_rect.left)
                if min_overlap > 5:
                    cam.y = (player1.sizey / 2 + platform_rect.height / 2) - platformpositions_y[i] - 1
                    gravity = 0
                    can_jump = 1
                    break
            can_jump = 0

    #gravity
    if jump == 0:
        cam.y -= 5*(player1.gravity*gravity)
    
    gravity = 1
    
    #debug
    if keys[pygame.K_r]:
        gen = 1
    if keys[pygame.K_o]:
        cam.y += 10

    #game display and update
    player1.update(0+(10*player1.direction),0,scale)
    player1.show()
    p1.updateauto()
    p1.show()
    p2.updateauto()
    p2.show()
    p3.updateauto()
    p3.show()
    p4.updateauto()
    p4.show()
    p5.updateauto()
    p5.show()
    p6.updateauto()
    p6.show()
    p7.updateauto()
    p7.show()
    
    #debug
    text_surface = font.render(str(jump), True, (255, 255, 255))
    #screen.blit(text_surface, (700, 100))
    text_surface = font.render(str(platformpositions_x[p2.location]-cam.x) + " , " + str(cam.x), True, (255, 255, 255))
    #screen.blit(text_surface, (100, 100))