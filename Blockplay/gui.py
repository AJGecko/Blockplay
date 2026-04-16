import pygame
import essentials as es
import ingame
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
buttonfont = pygame.font.SysFont(None, 64)
font = pygame.font.SysFont(None, 32)
pixelfont_path = es.pixelfont_path

def update():
    global screen,midx,midy,width,height,events,scale,mouse,buttonfont
    screen = pygame.display.get_surface()
    midx,midy,width,height,events,scale = es.basis()
    mouse = es.mouse
    text_surface = font.render(str(mouse.pressed(1)), True, (255, 255, 255))
    screen.blit(text_surface, (700, 100))

def backround(width, height, tile_size, scale):
    WIDTH, HEIGHT, TILE_SIZE = width, height, int(tile_size*scale)
    COLOR = es.appearance("color")
    LIGHT_COLOR = COLOR[0]
    DARK_COLOR = COLOR[1]
    
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


class button:
    def __init__(self, texture_path, size_x, size_y):
        self.path = Path(texture_path)
        if not self.path.is_absolute():
            self.path = (BASE_DIR / self.path).resolve()
        self.sizex = size_x
        self.sizey = size_y
        self.out_original = pygame.image.load(str(self.path)).convert_alpha()
        self.lscale = 1
        self.pos = (0, 0)
        self.font = pygame.font.SysFont(None, 64)
    
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
        output = self.font.render(text, True, (255, 255, 255))
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
        
class picture:
    def __init__(self, path):
        self.path = Path(path)
        if not self.path.is_absolute():
            self.path = (BASE_DIR / self.path).resolve()
        self.out_original = pygame.image.load(str(self.path)).convert_alpha()
        self.sizex, self.sizey = self.out_original.get_size()

    def show(self, x, y, lscale):
        width = int(self.sizex * lscale)
        height = int(self.sizey * lscale)
        self.out = pygame.transform.scale(self.out_original, (width, height))
        out_rect = self.out.get_rect(center=(midx + x, midy - y))
        screen.blit(self.out, out_rect)
#and self.hitbox(mouse.pos)

settingsbuild = {
  "music": (-40,300,0),
  "music2": (0,500),
  "test": True,
  "difficulty": ["normal","easy","hard"],
  "language": ["en","de","fr","es"]
}

class menu:

    class slider:
        def __init__(self,min,max,value,color):
            self.x = 0
            self.y = 0
            self.lscale = 1
            self.max = max
            self.min = min
            self.default = value
            if value == "none":
                self.value = min
            else:
                self.value = value
            if color == "none":
                self.color = (0,0,255)
            else:
                self.color = (0,0,255)
        def __call__(self):
            return str((self.min,self.max,self.value,self.color))
        def load(self,x,y,lscale,length):
            upper = self.max
            lower = self.min
            value_range = upper - lower
            min_text_size = 20
            max_text_size = 28
            min_text_px = int(min_text_size * lscale)
            max_text_px = int(max_text_size * lscale)
            if value_range <= 0:
                value_range = 1
            rect = pygame.Rect(int(x), int(y), int(length*lscale), int(10*lscale))
            hitbox = rect.inflate(int(8 * lscale), int(8 * lscale))
            pygame.draw.rect(screen, self.color, rect)
            knob_x = x + (((self.value - lower) / value_range) * length * lscale) - (6 * lscale)
            rect2 = pygame.Rect(int(knob_x), int(y-(1*lscale)), int(12*lscale), int(12*lscale))
            pygame.draw.rect(screen, (150, 150, 150), rect2)
            if (hitbox.collidepoint(mouse.pos) or rect2.collidepoint(mouse.pos)) and mouse.pressed(1):
                tempvalue = (mouse.x - x) / lscale
                if tempvalue < 0:
                    tempvalue = 0
                elif tempvalue > length:
                    tempvalue = length
                self.value = int(lower + ((tempvalue / length) * value_range))
                print(self.value)
            
            if value_range == 0:
                interp = 0.0
                text_size = min_text_px
            else:
                interp = (self.value - lower) / value_range
                text_size = int((min_text_size + (max_text_size - min_text_size) * interp) * lscale)
                text_size = max(min_text_px, min(max_text_px, text_size))
            tempfont = pygame.font.Font(str(pixelfont_path), text_size)
            text_surface = tempfont.render(str(self.value), True, (255, 255, 255))
            text_rect = text_surface.get_rect()
            text_rect.midleft = (x + length*lscale + 12*lscale, y + (4*lscale))
            screen.blit(text_surface, text_rect)

    class toggle:
        def __init__(self, condition):
            self.condition = condition
            self.default = condition
            self.knobx = 0
            self.lock = 0    
        def __call__(self):
            return self.condition
        def load(self,x,y,lscale): #in arbeit
            rect = pygame.Rect(int(x), int(y), int(30*lscale), int(10*lscale))
            hitbox = rect.inflate(int(16 * lscale), int(16 * lscale))

            if hitbox.collidepoint(mouse.pos) and mouse.pressed(1) and self.lock == 0:
                if self.condition == True:
                    self.condition = False
                elif self.condition == False:
                    self.condition = True
                else:
                    self.condition = self.default
                self.lock = 1     
            if not mouse.pressed(1):
                self.lock = 0


            if self.condition == True:
                self.knob_x = 0 
            elif self.condition == False:
                self.knob_x = 40
            else:
                self.condition = self.default
            
            if self.knobx < self.knobx and self.knobx + 2 <= 40:
                self.knob_x += 2
            if self.knob_x > self.knobx and self.knobx - 2 >= 0:
                self.knobx -= 2

            pygame.draw.rect(screen, (0,0,255), rect)
            pygame.draw.rect(screen,(150,150,150),(int((x+self.knobx-1)), int(y-(2*lscale)), int(14*lscale), int(14*lscale)))

    class dropdown:
        pass

    def __init__(self,name):
        self.name = name
        self.built = {}
        self.empty = 0
        print(self.name)
    def build(self, di):
        for key in di:
            optional1 = "none"
            optional2 = "none"

            if isinstance(di[key], tuple):
                given = di[key]
                if len(given) > 2:
                    if isinstance(given[2], int):
                        optional1 = given[2]
                    elif isinstance(given[2], tuple):
                        optional2 = given[2]
                if len(given) > 3:
                    if isinstance(given[3], tuple):
                        optional2 = given[3]
                    elif isinstance(given[3], int):
                        optional1 = given[3]

                out = self.slider(given[0], given[1], optional1, optional2)
                self.built[key] = out.load

            if isinstance(di[key], bool):
                given = di[key]
                out = self.toggle(given)
                self.built[key] = out.load
        
        print(self.built)

        if "music2" in self.built:
            print(self.built["music2"])
        else:
            print("music2 not built yet")

    def show(self):
        for element in self.built:
            pass

settingsmenu = menu("settings")
settingsmenu.build(settingsbuild)
test = settingsmenu.built["music"]
test2 = settingsmenu.built["test"]