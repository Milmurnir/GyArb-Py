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

roomPosition = [520,195]
player = Player([roomPosition[0]+100,roomPosition[1]+100],display,5,0.5,7.5)
resolution = (GetSystemMetrics(0),GetSystemMetrics(1))
playing = True
tileSize = 120
roomList = []


def makeNewRoom():
    room = Room(tileSize,roomPosition)
    room.makeRoom()
    roomList.append(room)


def start():
    pygame.init()
    makeNewRoom()
    
def update():

    display.blit(roomList[0].background,(roomPosition[0],roomPosition[1]))
    for tile in (roomList[0].tiles):
        if tile.spawnObject != None:
            tile.spawnObject.checkOpen(player.position,player.size)

    player.checkKeyStrokes(roomList[0].roomSize,roomPosition)
    
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
        print("Frames per second "+str(1/elapsed))