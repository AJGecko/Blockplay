import pygame
from pathlib import Path

FONT_DIR = Path(__file__).resolve().parent / "assets/fonts"
pixelfont_path = FONT_DIR / "grand9k_pixel.ttf"


scale = 1
width = 0
height = 0
events = None

curret_skin = "green"
color_scheme = 1
color_schemes = [
    ((151, 212, 38), (167, 233, 43)),
    ((120, 180, 30), (140, 200, 35)),
    ((45, 130, 200), (60, 150, 220)),
    ((180, 50, 50), (205, 70, 70)),
    ((135, 75, 205), (155, 95, 225)),
]

def appearance(mode):
    global color_scheme, curret_skin
    if mode == "color":
        return color_schemes[color_scheme-1] 
    if mode == "skin":
        return curret_skin

class mouse_():
    def __init__(self):
        self.pos = (0,0)
        self.x = self.pos[0]
        self.y = self.pos[1]
        self.button_down = False  # Speichert gedrückten Zustand

    def update(self):
        self.pos = pygame.mouse.get_pos()
        self.x = self.pos[0]
        self.y = self.pos[1]
        global events
        if events:
            if events.type == pygame.MOUSEBUTTONDOWN and events.button == 1:
                self.button_down = True
            if events.type == pygame.MOUSEBUTTONUP and events.button == 1:
                self.button_down = False

    def pressed(self, button):
        return self.button_down
mouse = mouse_()

def update():
    screen = pygame.display.get_surface()
    global width,height,events,scale
    width,height=screen.get_size()
    mouse.update()
    for event in pygame.event.get():
        events = event

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

"""
def aabb_collision(rect1, rect2):
    AABB (Axis-Aligned Bounding Box) collision detection.
    rect1, rect2: pygame.Rect objects or (x, y, width, height) tuples
    Returns: True if rectangles overlap, False otherwise
    if isinstance(rect1, tuple):
        rect1 = pygame.Rect(*rect1)
    if isinstance(rect2, tuple):
        rect2 = pygame.Rect(*rect2)
    return rect1.colliderect(rect2)
"""