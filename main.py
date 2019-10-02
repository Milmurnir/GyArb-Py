import pygame
import random
import keyboard
from classes import *
from win32api import * 


display = pygame.display.set_mode((1920,1080))
resolution = (GetSystemMetrics(0),GetSystemMetrics(1))
playing = True
tileSize = 120
tileList = []

def makeTerrain():
    for i in range(14):
        yCord = i * tileSize
        for o in range(8):
            xCord = o * tileSize

        tile = Tile((xCord,yCord),tileSize)
        tileList.append(tile)

def start():
    pygame.init()
    makeTerrain()

def update():
    for tile in tileList:
        tile.updateTile()

start()

while playing:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            playing = False

        if keyboard.is_pressed("esc"):
            playing = False
    
    update()
    pygame.display.update()