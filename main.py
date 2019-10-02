import pygame
import random
import keyboard
from win32api import * 


display = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
resolution = (GetSystemMetrics(0),GetSystemMetrics(1))
playing = True


def makeTerrain()







while playing:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            playing = False

        if keyboard.is_pressed("esc"):
            playing = False