import pygame
from pathlib import Path

FONT_DIR = Path(__file__).resolve().parent / "assets/fonts"
pixelfont_path = FONT_DIR / "grand9k_pixel.ttf"


scale = 1
width = 0
height = 0
events = None
events_list = []

settings = {
    "number_platforms": 30,
    "difficulty": "normal",
    "language": "en",
    "skin": "green",
    "color_scheme": 1,
    "fly": False,
    "volume": 35
}

current_skin = settings["skin"]
color_scheme = 1
color_schemes = {
    1: ((151, 212, 38), (167, 233, 43)),
    2: ((120, 180, 30), (140, 200, 35)),
    3: ((45, 130, 200), (60, 150, 220)),
    4: ((180, 50, 50), (205, 70, 70)),
    5: ((135, 75, 205), (155, 95, 225)),
}



def appearance(mode):
    global color_scheme, current_skin
    if mode == "color":
        return color_schemes.get(color_scheme, color_schemes[1])
    if mode == "skin":
        return current_skin

class mouse_():
    def __init__(self):
        self.pos = (0,0)
        self.x = self.pos[0]
        self.y = self.pos[1]
        self.button_down = False  # Speichert gedrückten Zustand

    def update(self, event=None):
        if event is None:
            self.pos = pygame.mouse.get_pos()
        else:
            if event.type == pygame.MOUSEMOTION:
                self.pos = event.pos
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.pos = event.pos
                self.button_down = True
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                self.pos = event.pos
                self.button_down = False
            elif event.type == pygame.FINGERDOWN:
                self.pos = (int(event.x * width), int(event.y * height))
                self.button_down = True
            elif event.type == pygame.FINGERUP:
                self.pos = (int(event.x * width), int(event.y * height))
                self.button_down = False
            elif event.type == pygame.FINGERMOTION:
                self.pos = (int(event.x * width), int(event.y * height))
        self.x, self.y = self.pos

    def pressed(self, button):
        return self.button_down
mouse = mouse_()

def update():
    screen = pygame.display.get_surface()
    global width,height,events,scale,current_skin,color_scheme,events_list
    events_list = []
    color_scheme = settings["color_scheme"]
    current_skin = settings["skin"]
    width,height=screen.get_size()
    for event in pygame.event.get():
        events_list.append(event)
        events = event
        mouse.update(event)

midx = 0
midy = 0
def mid():
    global midx, midy
    midx = width / 2
    midy = height / 2

def basis():
    mid()
    return midx,midy,width,height,events,scale

def collision(one, two):
    if isinstance(one, tuple):
        one = pygame.Rect(*one)
    if isinstance(two, tuple):
        two = pygame.Rect(*two)
    return one.colliderect(two) 
    pass

