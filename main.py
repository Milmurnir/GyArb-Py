import time
import pygame
import random
import keyboard
from classes import *
from win32api import * 
"""
display = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
"""
display = pygame.display.set_mode((1920,1080))

player = Player([0,0],display,5,0.5,7.5)
resolution = (GetSystemMetrics(0),GetSystemMetrics(1))
playing = True
tileSize = 120
background = pygame.Surface(resolution)


def makeTerrain():
    for i in range(7):
        yCord = i * tileSize + 75
        for o in range(12):
            xCord = o * tileSize + 300
            
            tile = Tile((xCord,yCord),tileSize,display)
            background.blit(tile.sprite,tile.position)

def start():
    pygame.init()
    makeTerrain()

def update():
   
    display.blit(background,(0,0))
    player.checkKeyStrokes()
    if player.position[0] + player.size > resolution[0]:
        player.position[0] = resolution[0] - player.size
    elif player.position[0] < 0:
        player.position[0] = 0
    
    if player.position[1] < 0:
        player.position[1] = 0
    elif player.position[1] + player.size > resolution[1]:
        player.position[1] = resolution[1] - player.size
    player.drawPlayer()

    for shot in player.shotList:
        shot.drawShot()
        shot.updateShot()
        if shot.X > resolution[0] + 500 or shot.X < 0 - 500:
            player.shotList.remove(shot)
        
        elif shot.Y > resolution[1] + 500 or shot.Y < 0 - 500:
            player.shotList.remove(shot)


lt = 0
start()
while playing:
    t = time.time()
    
    display.fill((0,0,0))
    update()
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            playing = False
            break 
        if keyboard.is_pressed("esc"):
            playing = False

    elapsed = t - lt
    lt = t
     
    if keyboard.is_pressed("f"):
        print("Frames per second "+str(elapsed))