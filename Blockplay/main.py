# /// script
# dependencies = [
#  "pygame-ce",
#  "pygame_markdown",
# ]
# ///
#for the web version

import pygame
import sys
from pathlib import Path
import asyncio

#set assets path
BASE_DIR = Path(__file__).resolve().parent
LIB_DIR = BASE_DIR / "lib"
if str(LIB_DIR) not in sys.path:
    sys.path.insert(0, str(LIB_DIR))

ASSETS = BASE_DIR / "assets"
INFO_DIR = BASE_DIR / "info"

#init pygame and create window
pygame.init()
try:
    pygame.mixer.init()
except Exception as e:
    print("Mixer init failed:", e)
screen = pygame.display.set_mode((1920, 1080), pygame.RESIZABLE)
pygame.display.set_caption("Blockplay")
clock = pygame.time.Clock()

#import other files
import ingame
import essentials as es
import gui
import lang
lang.updatelang()

#set font
font = pygame.font.SysFont(None, 86)
titlefont = pygame.font.SysFont(None, 128)

#main loop variables
running = True
currentmenu = 1
midx = midy = width = height = scale = 0

#update function to update essentials and gui
def update():
    es.update()
    gui.update()

#create buttons and logo
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
pause_button_lock = 0
confirm_exit = False

#load music
MENU_MUSIC_FILE = ASSETS / 'music' / 'viacheslavstarostin-game-gaming-video-game-music-471936.ogg'
OTHER_MENU_MUSIC_FILE = ASSETS / 'music' / 'viacheslavstarostin-gaming-game-video-game-music-474517.ogg'
menu_music_playing = False
active_music_file = None

#music functions
def get_menu_volume():
    return max(0.0, min(1.0, es.settings.get("volume", 35) / 100.0))

def update_menu_music():
    global menu_music_playing, active_music_file
    desired_music = None

    if currentmenu in (1, 3, 7):
        desired_music = MENU_MUSIC_FILE
    elif currentmenu in (2, 4, 6):
        desired_music = OTHER_MENU_MUSIC_FILE

    if desired_music is not None:
        if not menu_music_playing or active_music_file != desired_music:
            try:
                pygame.mixer.music.load(str(desired_music))
                pygame.mixer.music.play(-1)
                active_music_file = desired_music
                menu_music_playing = True
            except Exception as e:
                print("Menu music load failed:", e)
                menu_music_playing = False
                active_music_file = None
        if menu_music_playing:
            pygame.mixer.music.set_volume(get_menu_volume())
    else:
        if menu_music_playing:
            pygame.mixer.music.stop()
            menu_music_playing = False
            active_music_file = None

#draw center title function for pause, win and lose screens
def draw_center_title(key):
    text = lang.currentlang.get(key, key)
    output = titlefont.render(text, True, (255, 255, 255))
    text_rect = output.get_rect(center=(midx, midy - 180 * scale))
    screen.blit(output, text_rect)


async def main():
    global running, currentmenu, midx, midy, width, height, scale, pause_lock, pause_button_lock, confirm_exit, screen
    while running:
        #update essentials and gui
        update()

        #get basic variables
        midx,midy,width,height,events,scale = es.basis()
        mouse = es.mouse
        keys = pygame.key.get_pressed()
        
        #handle events
        if events and events.type == pygame.QUIT:
            running = False

        
        #pause menu toggle
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

        #main menu
        if currentmenu == 1:

            #background display
            gui.backround(width,height,120,scale)

            #button display
            button1.show(0,0,1)
            button4.show(0,-120,1)
            button3.show(0,-240,1)
            button2.show(0,-360,1)

            #logo display
            logo.show(25,320,0.5)

            #highscore display
            highscore_label = lang.currentlang.get("highscore", "Highscore")
            highscore_value = "--" if ingame.highscore is None else f"{ingame.highscore:.2f}"
            highscore_surface = font.render(f"{highscore_label}: {highscore_value}", True, (255, 255, 255))
            highscore_rect = highscore_surface.get_rect(center=(midx, midy - 120 * scale))
            screen.blit(highscore_surface, highscore_rect)

            #button interactions
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
              
        #ingame
        if currentmenu == 2:
            #draw background
            ingame.backround()

            #run game and get state
            game_state = ingame.game(es.settings["number_platforms"])

            #pause functionality
            if ingame.pause_button_rect is not None and mouse.pressed(1) and pause_button_lock == 0:
                if ingame.pause_button_rect.collidepoint(mouse.pos):
                    ingame.timer("pause")
                    ingame.timer_on = "pause"
                    currentmenu = 4
                    pause_button_lock = 1
            if not mouse.pressed(1):
                pause_button_lock = 0
            
            #check game state for win/lose
            if game_state == "dead":
                currentmenu = 5
            elif game_state == "won":
                ingame.check_highscore(ingame.finishtime)
                currentmenu = 6

        #settings menu
        if currentmenu == 3:
            #show settings menu
            gui.settingsmenu.show()

            #main menu button in settings menu
            button_menu.show(0,-400,1)
            if button_menu.click(0,-400,mouse.pressed(1)):
                mouse.button_down = False
                currentmenu = 1

        #pause menu
        if currentmenu == 4:
            #draw pause menu (background, title and buttons)
            gui.backround(width,height,120,scale)
            draw_center_title("pause")
            button_resume.show(0,-120,1)
            button_restart.show(0,-240,1)
            button_menu.show(0,-360,1)
            
            #button interactions
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

        #game over screen
        if currentmenu == 5:
            #draw game over screen (background, title and buttons)
            gui.backround(width,height,120,scale)
            draw_center_title("game_over")
            button_restart.show(0,-180,1)
            button_menu.show(0,-300,1)

            #button interactions
            if button_restart.click(0,-180,mouse.pressed(1)):
                ingame.gen = 1
                mouse.button_down = False
                currentmenu = 2
            if button_menu.click(0,-300,mouse.pressed(1)):
                mouse.button_down = False
                currentmenu = 1

        #win screen
        if currentmenu == 6:
            #draw win screen (background, title, time, highscore and buttons)
            gui.backround(width,height,120,scale)
            draw_center_title("you_won")
            your_time_text = lang.currentlang.get("your_time", "Your Time") + ": " + str(ingame.finishtime)
            text_surface = font.render(your_time_text, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(midx, midy - 60 * scale))
            screen.blit(text_surface, text_rect)

            button_restart.show(0,-180,1)
            button_menu.show(0,-300,1)

            #new highscore display
            if ingame.new_highscore:
                if (pygame.time.get_ticks() // 500) % 2 == 0:
                    new_text = lang.currentlang.get("new_highscore", "New Highscore!")
                    new_surface = font.render(new_text, True, (255, 255, 0))
                    new_rect = new_surface.get_rect(center=(midx, midy + 20 * scale))
                    screen.blit(new_surface, new_rect)

            #button interactions
            if button_restart.click(0,-180,mouse.pressed(1)):
                ingame.gen = 1
                mouse.button_down = False
                currentmenu = 2
            if button_menu.click(0,-300,mouse.pressed(1)):
                mouse.button_down = False
                currentmenu = 1

        #info screen (loads markdown file)
        if currentmenu == 7:
            #load info file based on current language, default to english if not found
            info_file = INFO_DIR / f"info-{lang.getlang()}.md"
            if not info_file.exists():
                info_file = INFO_DIR / "info-en.md"
            gui.info(str(info_file))
            button_y = -midy + 70

            #main menu button in info menu
            button_menu.show(0, button_y, 1)
            if button_menu.click(0, button_y, mouse.pressed(1)):
                mouse.button_down = False
                currentmenu = 1

        update_menu_music()

        pygame.display.flip()
        clock.tick(60)
        await asyncio.sleep(0)

    sys.exit()


if __name__ == '__main__':
    asyncio.run(main())
