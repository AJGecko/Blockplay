import pygame
from essentials import *

running = True
quit_confirm = 1
exitfont = pygame.font.SysFont(None, 128)

def quit():
    global running
    print("Game stopped")
    running = False

def quitscreen():
    global quit_confirm, running, exitfont
    print("check")
    screen = pygame.display.get_surface()
    clock = pygame.time.Clock()
    while quit_confirm == 1:
        screen = pygame.display.get_surface()
        midx,midy,width,height,events,scale = basis()
        screen.fill("black")
        msg = exitfont.render("Beenden? (J/N)", True, (255, 0, 0))
        msg_rect = msg.get_rect(center=(midx, midy))
        screen.blit(msg, msg_rect)
        for event in pygame.event.get():
                pass
        keys = pygame.key.get_pressed()
        if keys[pygame.K_j]:
            quit_confirm = 0
            quit() 
        if keys[pygame.K_n]:
            quit_confirm = 0
            running = True
        pygame.display.flip()
        clock.tick(30)

def running_():
    global running
    return running