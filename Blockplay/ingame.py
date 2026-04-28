import pygame
import essentials as es
import lang
import time as time_module
import random
import math
from pathlib import Path

#set assets path
BASE_DIR = Path(__file__).resolve().parent
ASSETS = BASE_DIR / "assets"

#basis variables
midx,midy,width,height,events,scale = es.basis()
screen = pygame.display.get_surface()
font = pygame.font.SysFont(None, 32)
timerfont = pygame.font.SysFont(None, 86)
platform_texture = pygame.image.load(str(ASSETS / 'platform.png')).convert_alpha()
pause_button_texture = pygame.image.load(str(ASSETS / 'button.png')).convert_alpha()
highscore = None
new_highscore = False

#load player textures
player_dir = ASSETS / 'player'
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
    for png_file in sorted((player_dir / p).glob("*.png")):
        out.append(pygame.image.load(str(png_file)).convert_alpha())
    player_texture.append(out)

#global variables
gen = 1
jump = 0
can_jump = 0
camy_storage = 0
cp = 0
gravity = 1
last_collision_index = -1
start_time = None
elapsed_time = 0.0
timer_on = False
finishtime = None
mouse_x = 0
mouse_y = 0

#camera class
class camera:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.fov = 1

#player class
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

#platform class
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
        if ((platformpositions_x[self.location]-cam.x)*scale*cam.fov)+200 < -1200:
            if self.location + 7 <= (len(platformpositions_x)-1):
                self.location = self.location + 7
        if ((platformpositions_x[self.location]-cam.x)*scale*cam.fov)-200 > 1200:
            if self.location - 7 >= 0:
                self.location = self.location - 7

        if (platformpositions_x[self.location]-cam.x)*scale*cam.fov > -100 and (platformpositions_x[self.location]-cam.x)*scale*cam.fov < 100:
            global cp 
            cp = self.location

#finish line class
class finish:
    def __init__(self):
        self.columns = 4
        self.base_cell_size = 48
        self.min_cell_size = 12

    def _cell_size(self, lscale):
        return max(int(self.base_cell_size * lscale), self.min_cell_size)

    def hitbox(self, x, player_rect, lscale):
        pixels_per_world = scale * cam.fov
        if pixels_per_world <= 0:
            return False

        cell_size = self._cell_size(lscale)
        total_width_world = (self.columns * cell_size) / pixels_per_world
        left_world = x - (total_width_world / 2)
        right_world = x + (total_width_world / 2)
        return bool(player_rect.right >= left_world and player_rect.left <= right_world)

    def show(self,x,y,lscale):
        if "platformpositions_x" not in globals() or len(platformpositions_x) == 0:
            return

        pixels_per_world = scale * cam.fov
        if pixels_per_world <= 0:
            return

        cell_size = self._cell_size(lscale)
        columns = self.columns
        total_width = columns * cell_size
        screen_x = int(midx + (x - cam.x) * pixels_per_world)
        left_x = screen_x - (total_width // 2)

        if left_x >= width or left_x + total_width <= 0:
            return

        # Anchor rows to world y=0 so camera height changes do not cause color flicker.
        anchor_y = midy + (cam.y * pixels_per_world)
        start_row = math.floor((0 - anchor_y) / cell_size) - 1
        end_row = math.ceil((height - anchor_y) / cell_size) + 1

        for row in range(start_row, end_row + 1):
            row_y = int(anchor_y + row * cell_size)
            if row_y >= height or row_y + cell_size <= 0:
                continue
            for col in range(columns):
                color = (255, 255, 255) if (row + col) % 2 == 0 else (0, 0, 0)
                cell_x = left_x + col * cell_size
                pygame.draw.rect(screen, color, (cell_x, row_y, cell_size, cell_size))

#timer function
def timer(on):
    global start_time, elapsed_time
    if on is False:
        start_time = None
        elapsed_time = 0.0
        return 0.0
    if on == "pause":
        if start_time is not None:
            elapsed_time += time_module.time() - start_time
            start_time = None
        return round(elapsed_time, 2)
    if on is True:
        if start_time is None:
            start_time = time_module.time()
        return round(elapsed_time + (time_module.time() - start_time), 2)
    return round(elapsed_time, 2)

#highscore functions
def load_highscore():
    global highscore
    highscore = None


def save_highscore(value):
    global highscore
    highscore = float(value)


def check_highscore(value):
    global new_highscore
    if value is None:
        return False
    if highscore is None or value < highscore:
        save_highscore(value)
        new_highscore = True
        return True
    new_highscore = False
    return False


time = timer(timer_on)

#pause button
pause_button_rect = None
def draw_pause_button():
    global pause_button_rect
    button_size = 80
    button_x = 100
    button_y = 80
    pause_button_rect = pygame.Rect(button_x, button_y, button_size, button_size)

    button_image = pygame.transform.smoothscale(pause_button_texture, (button_size, button_size))
    screen.blit(button_image, pause_button_rect.topleft)

    icon_width = 16
    icon_height = 40
    icon_x = button_x + (button_size - icon_width*2 - 12) // 2
    icon_y = button_y + (button_size - icon_height) // 2
    pygame.draw.rect(screen, (240, 240, 240), (icon_x, icon_y, icon_width, icon_height), border_radius=4)
    pygame.draw.rect(screen, (240, 240, 240), (icon_x + icon_width + 12, icon_y, icon_width, icon_height), border_radius=4)

    return pause_button_rect

#objects
cam = camera()
player1 = player(1,"green")
p1 = platform()
p2 = platform()
p3 = platform()
p4 = platform()
p5 = platform()
p6 = platform()
p7 = platform()
finish1 = finish()

#draws the ingame backround
def backround():
    pygame.draw.rect(screen, (38, 171, 212), (0, 0, width, height), 0)

#generates the level by creating the platform positions
def generate(number, multiplier):
    platformpositions_x = []
    platformpositions_y = []
    x = 0
    y = 0
    for i in range(number):
        platformpositions_x.insert(i,x)
        x = x + 110*multiplier + random.randint(int(30*multiplier),int(160*multiplier))
        platformpositions_y.insert(i,y)
        y = y + random.randint(int(-60*multiplier),int(60*multiplier))
    return platformpositions_x, platformpositions_y

#runs the game
def game(number):
    #global variables
    global midx,midy,width,height,events,scale,font,platform_texture,gravity,last_collision_index,timer_on,finishtime
    midx,midy,width,height,events,scale = es.basis()
    global gen, p1, p2, p3, p4, p5, menu, jump, can_jump, camy_storage, mouse_x, mouse_y

    #set player skin
    if es.settings["skin"] in folder_names:
        player1.skin = es.settings["skin"]

    #setup for the round
    if gen == 1:
            global platformpositions, platformpositions_x, platformpositions_y, new_highscore
            platformpositions = generate(number,2.3)
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
            timer_on = False
            gen = 0
            jump = 0
            can_jump = 0
            new_highscore = False
    #steering
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        player1.direction = -1
        cam.x -= 8
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        if not timer_on:
            timer_on = True
        player1.direction = 1
        cam.x += 8
    if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and jump == 0:
        cam.y -= 4
    if not keys[pygame.K_LEFT] and not keys[pygame.K_a] and not keys[pygame.K_RIGHT] and not keys[pygame.K_d]:
        player1.direction = 0

    #mouse steering
    if es.mouse.pressed(1):
        mouse_x, mouse_y = es.mouse.pos
        if mouse_x < midx - 100*scale:
            player1.direction = -1
            cam.x -= 8
        elif mouse_x > midx + 100*scale:
            if not timer_on:
                timer_on = True
            player1.direction = 1
            cam.x += 8
        else:
            player1.direction = 0
        if mouse_y > midy + 100*scale and jump == 0:
            cam.y -= 4

    #jump
    if (keys[pygame.K_UP] or keys[pygame.K_w] or keys[pygame.K_SPACE] or (mouse_y < midy - 100*scale and es.mouse.pressed(1))) and can_jump == 1:
        jump = 1
        can_jump = 0
        camy_storage = cam.y
        player1.gravity = 0
    elif jump == 0:
        if player1.gravity + 0.1 > 1:
            player1.gravity = 1
        else:
            player1.gravity += 0.1

    if jump == 1:
        if cam.y - camy_storage >= 200 and cam.y - camy_storage < 300:
            cam.y += 7
        elif cam.y - camy_storage >= 300:
            jump = 0
        else:
            cam.y += 10

    #timer
    time = timer(timer_on)
    
    #finish line position
    finish_world_x = platformpositions_x[-1] + 600

    #hitbox (collision check)
    player_world_x = cam.x + (player1.x / scale / cam.fov)
    player_world_y = (player1.y / scale / cam.fov) - cam.y
    player_rect = pygame.Rect(
        int(player_world_x - player1.sizex / 2),
        int(player_world_y - player1.sizey / 2),
        int(player1.sizex),
        int(player1.sizey),
    )

    if finish1.hitbox(finish_world_x, player_rect, scale):
        finishtime = time
        timer_on = False
        return "won"


    difficulty = es.settings.get("difficulty", "normal")

    for i in range(number):
        platform_rect = pygame.Rect(
            int(platformpositions_x[i] - 200 / 2),
            int(platformpositions_y[i] - 400 / 2),
            200,
            400,
        )
        if player_rect.colliderect(platform_rect):
            if difficulty == "easy":
                cam.y = (player1.sizey / 2 + platform_rect.height / 2) - platformpositions_y[i] - 1
                gravity = 0
                can_jump = 1
                break

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
        cam.y -= 8*(player1.gravity*gravity)
    
    gravity = 1

    # death limit (Adapts to the nearest platform above the player.)
    search_radius = 900
    above_candidates = [
        i for i in range(len(platformpositions_x))
        if abs(platformpositions_x[i] - player_world_x) <= search_radius and platformpositions_y[i] <= player_world_y
    ]
    if above_candidates:
        reference_platform_y = max(platformpositions_y[i] for i in above_candidates)
    else:
        reference_idx = max(0, min(cp, len(platformpositions_y) - 1))
        reference_platform_y = platformpositions_y[reference_idx]

    death_margin = 1200
    stand_cam_y = (player1.sizey / 2 + p1.sizey / 2) - reference_platform_y - 1
    death_limit = stand_cam_y - death_margin
    if cam.y < death_limit:
        timer_on = False
        return "dead"
    
    #debug
    if (es.settings["fly"] and keys[pygame.K_u]):
        cam.y += 20

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
    finish1.show(finish_world_x, 0, scale)
    pause_button_rect = draw_pause_button()
    text_surface = timerfont.render(str(time), True, (255, 255, 255))
    screen.blit(text_surface, (width - 200, 100))

    #return status
    return "playing"