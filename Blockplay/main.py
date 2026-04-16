import pygame
import random
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
ASSETS = BASE_DIR / "assets"

pygame.init()
screen = pygame.display.set_mode((1920, 1080), pygame.RESIZABLE)
pygame.display.set_caption("Blockplay")
clock = pygame.time.Clock()

import quitscreen as quit
import ingame
import essentials as es
import gui

font = pygame.font.SysFont(None, 32)

running = True
currentmenu = 1

def update():
    es.update()
    gui.update()


button1 = gui.button(str(ASSETS / 'pixel-48x16.png'), 400, 100)
button2 = gui.button(str(ASSETS / 'pixel-48x16.png'), 400, 100)
logo = gui.picture(str(ASSETS / 'logo.png'))
print("Hello World!")
lock = 0

while running:
    update()
    midx,midy,width,height,events,scale = es.basis()
    mouse = es.mouse

    keys = pygame.key.get_pressed()
    
    if events and events.type == pygame.QUIT:
        quit.quit()
    if keys[pygame.K_l]:
        es.scale = 2
    else:
        es.scale = 1
    if keys[pygame.K_b]:
        currentmenu = 1
    if keys[pygame.K_c] and lock==0:
        if es.color_scheme + 1 <= 5:
            es.color_scheme += 1
            lock = 1
        else:
            es.color_scheme = 1
            lock = 1
    if not keys[pygame.K_c]:
        lock = 0


    if currentmenu == 1:

        gui.backround(width,height,120,scale)
        button1.show(0,-120,1)
        button1.text(0,-120,"Start")
        button2.show(0,-240,1)
        button2.text(0,-240,"Exit")
        logo.show(25,320,0.5)
        gui.test(100,100,2,140)
        gui.test2(100,150,2)



        if button1.click(0,-120,mouse.pressed(1)):
            ingame.gen = 1
            currentmenu = 2
        if button2.click(0,-240,mouse.pressed(1)):
            quit.quit_confirm = 1
            quit.quitscreen()
            
            
            

    if currentmenu == 2:
        ingame.backround()
        ingame.game(30)

    text_surface = font.render(str(mouse.pressed(1)), True, (255, 255, 255))
    screen.blit(text_surface, (700, 100))

    running = quit.running_()                           
    pygame.display.flip()
    clock.tick(60)
    
#6e4d32
#text_surface = font.render(str(platformpositions_x[p2.location]-cam.x) + " , " + str(cam.x), True, (255, 255, 255))
#screen.blit(text_surface, (100, 100))