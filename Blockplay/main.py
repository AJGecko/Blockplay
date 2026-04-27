import pygame
import sys
from pathlib import Path
import asyncio

BASE_DIR = Path(__file__).resolve().parent
ASSETS = BASE_DIR / "assets"
INFO_DIR = BASE_DIR / "info"

pygame.init()
screen = pygame.display.set_mode((1920, 1080), pygame.RESIZABLE)
pygame.display.set_caption("Blockplay")
clock = pygame.time.Clock()

import ingame
import essentials as es
import gui
import lang
lang.updatelang()

font = pygame.font.SysFont(None, 86)
titlefont = pygame.font.SysFont(None, 128)

running = True
currentmenu = 1

def update():
    es.update()
    gui.update()


button1 = gui.button(str(ASSETS / 'button.png'), 400, 100, "start")
button4 = gui.button(str(ASSETS / 'button.png'), 400, 100, "info")
button3 = gui.button(str(ASSETS / 'button.png'), 400, 100, "settings")
button2 = gui.button(str(ASSETS / 'button.png'), 400, 100, "exit")
button_resume = gui.button(str(ASSETS / 'button.png'), 400, 100, "resume")
button_restart = gui.button(str(ASSETS / 'button.png'), 400, 100, "restart")
button_menu = gui.button(str(ASSETS / 'button.png'), 400, 100, "main_menu")
button_yes = gui.button(str(ASSETS / 'button.png'), 180, 80, "yes")
button_no = gui.button(str(ASSETS / 'button.png'), 180, 80, "no")
logo = gui.picture(str(ASSETS / 'logo.png'))
print("Hello World!")
lock = 0
pause_lock = 0
confirm_exit = False


def draw_center_title(key):
    text = lang.currentlang.get(key, key)
    output = titlefont.render(text, True, (255, 255, 255))
    text_rect = output.get_rect(center=(midx, midy - 180 * scale))
    screen.blit(output, text_rect)

while running:
    update()
    midx,midy,width,height,events,scale = es.basis()
    mouse = es.mouse

    keys = pygame.key.get_pressed()
    
    if events and events.type == pygame.QUIT:
        running = False
    if keys[pygame.K_l]:
        es.scale = 2
    else:
        es.scale = 1
    

    pause_pressed = keys[pygame.K_ESCAPE] or keys[pygame.K_p]
    if pause_pressed and pause_lock == 0:
        if currentmenu == 2:
            ingame.timer("pause")
            currentmenu = 4
            ingame.timer_on = "pause"
        elif currentmenu == 4:
            ingame.timer_on = True
            currentmenu = 2
        pause_lock = 1
    if not pause_pressed:
        pause_lock = 0

    if keys[pygame.K_h]:
        currentmenu = 7


    if currentmenu == 1:

        gui.backround(width,height,120,scale)
        button1.show(0,0,1)
        button4.show(0,-120,1)
        button3.show(0,-240,1)
        button2.show(0,-360,1)
        logo.show(25,320,0.5)

        if button1.click(0,0,mouse.pressed(1)):
            ingame.gen = 1
            ingame.timer_on = False
            currentmenu = 2
        if button2.click(0,-360,mouse.pressed(1)):
            confirm_exit = True
            mouse.button_down = False
        if button3.click(0,-240,mouse.pressed(1)):
            mouse.button_down = False
            currentmenu = 3
        if button4.click(0,-120,mouse.pressed(1)):
            mouse.button_down = False
            currentmenu = 7

        if confirm_exit:
            button_yes.show(-310, -360, 1)
            button_no.show(310, -360, 1)

            if button_yes.click(-310, -360, mouse.pressed(1)):
                running = False
            elif button_no.click(310, -360, mouse.pressed(1)):
                confirm_exit = False
                mouse.button_down = False
            elif mouse.pressed(1):
                confirm_exit = False
                mouse.button_down = False
            
            
            

    if currentmenu == 2:
        ingame.backround()
        game_state = ingame.game(es.settings["number_platforms"])
        if game_state == "dead":
            currentmenu = 5
        elif game_state == "won":
            currentmenu = 6

    if currentmenu == 3:
        gui.settingsmenu.show()
        button_menu.show(0,-400,1)
        if button_menu.click(0,-400,mouse.pressed(1)):
            mouse.button_down = False
            currentmenu = 1

    if currentmenu == 4:
        gui.backround(width,height,120,scale)
        draw_center_title("pause")
        button_resume.show(0,-120,1)
        button_restart.show(0,-240,1)
        button_menu.show(0,-360,1)

        if button_resume.click(0,-120,mouse.pressed(1)):
            ingame.timer_on = True
            currentmenu = 2
            mouse.button_down = False
        if button_restart.click(0,-240,mouse.pressed(1)):
            ingame.gen = 1
            ingame.timer_on = False
            mouse.button_down = False
            currentmenu = 2
        if button_menu.click(0,-360,mouse.pressed(1)):
            ingame.gen = 1
            ingame.timer_on = False
            mouse.button_down = False
            currentmenu = 1

    if currentmenu == 5:
        gui.backround(width,height,120,scale)
        draw_center_title("game_over")
        button_restart.show(0,-180,1)
        button_menu.show(0,-300,1)

        if button_restart.click(0,-180,mouse.pressed(1)):
            ingame.gen = 1
            mouse.button_down = False
            currentmenu = 2
        if button_menu.click(0,-300,mouse.pressed(1)):
            mouse.button_down = False
            currentmenu = 1

    if currentmenu == 6:
        gui.backround(width,height,120,scale)
        draw_center_title("you_won")
        your_time_text = lang.currentlang.get("your_time", "Your Time") + ": " + str(ingame.finishtime)
        text_surface = font.render(your_time_text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(midx, midy - 60 * scale))
        screen.blit(text_surface, text_rect)
        button_restart.show(0,-180,1)
        button_menu.show(0,-300,1)

        if button_restart.click(0,-180,mouse.pressed(1)):
            ingame.gen = 1
            mouse.button_down = False
            currentmenu = 2
        if button_menu.click(0,-300,mouse.pressed(1)):
            mouse.button_down = False
            currentmenu = 1

    if currentmenu == 7:
        info_file = INFO_DIR / f"info-{lang.getlang()}.md"
        if not info_file.exists():
            info_file = INFO_DIR / "info-en.md"
        gui.info(str(info_file))
        button_menu.show(0,-400,1)
        if button_menu.click(0,-400,mouse.pressed(1)):
            mouse.button_down = False
            currentmenu = 1

    #text_surface = font.render(str(mouse.pressed(1)), True, (255, 255, 255))
    #screen.blit(text_surface, (700, 100))
    #text_surface = font.render(str(ingame.timer(True)), True, (255, 255, 255))
    #screen.blit(text_surface, (100, 100))



    pygame.display.flip()
    clock.tick(60)
    
#6e4d32
    
sys.exit()



#asyncio def main():
pass