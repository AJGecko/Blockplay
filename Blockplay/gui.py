import pygame
import essentials as es
import ingame

buttonfont = pygame.font.SysFont(None, 64)

def update():
    global screen,midx,midy,width,height,events,scale,mouse,buttonfont
    screen = pygame.display.get_surface()
    midx,midy,width,height,events,scale = es.basis()
    mouse = es.mouse

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
        self.path = texture_path
        self.sizex = size_x
        self.sizey = size_y
        self.out_original = pygame.image.load(self.path).convert_alpha()
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
#and self.hitbox(mouse.pos)