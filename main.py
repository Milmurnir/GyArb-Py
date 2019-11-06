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



clock = pygame.time.Clock()
player = Player([0,0],display,5,0.5,6)
resolution = (GetSystemMetrics(0),GetSystemMetrics(1))
playing = True
tileSize = 120
Map = []

firstQuadrant = [0]


def start():
    pygame.init()
    



def generateRoom():
    m = random.randint(28,29)
    n = random.randint(30,31)
    o = random.randint(32,33)
    p = random.randint(34,35)
    q = random.randint(36,37)
    r = random.randint(38,39)
    s = random.randint(40,41)
    c = random.randint(42,43)

    baseMap = [

        [1,10,10,10,10,10,10,10,10,10,10,10,10,10,10,2],
        [13,0,0,0,0,0,0,0,0,0,0,0,0,0,0,11],
        [13,0,n,0,0,0,0,0,0,0,0,0,0,n,0,11],
        [13,0,m,o,0,0,p,r,r,p,0,0,o,m,0,11],
        [13,0,s,0,0,q,c,0,0,c,q,0,0,s,0,11],
        [13,0,m,o,0,0,p,r,r,p,0,0,o,m,0,11],
        [13,0,n,0,0,0,0,0,0,0,0,0,0,n,0,11],
        [13,0,0,0,0,0,0,0,0,0,0,0,0,0,0,11],
        [4,12,12,12,12,12,12,12,12,12,12,12,12,12,12,3]
    ]
    return baseMap


    
def update():

# kan optimeras
    display.blit(room.background,(0,0))


# kan optimeras
    player.checkKeyStrokes()
    
    player.drawPlayer()

    for shot in player.shotList:
        shot.drawShot()
        shot.updateShot()
        if shot.X > resolution[0] + 500 or shot.X < 0 - 500:
            player.shotList.remove(shot)
        
        elif shot.Y > resolution[1] + 500 or shot.Y < 0 - 500:
            player.shotList.remove(shot)
        
    if player.quadrant == 1:
        for tile in room.firstQuadrant:
            checkCollision(tile.position,player.position,tile.size,player.size)
    
    elif player.quadrant == 2:
        for tile in room.secondQuadrant:
            checkCollision(tile.position,player.position,tile.size,player.size)

    elif player.quadrant == 3:
        for tile in room.thirdQuadrant:
            checkCollision(tile.position,player.position,tile.size,player.size)

    elif player.quadrant == 4:
        for tile in room.fourthQuadrant:
            checkCollision(tile.position,player.position,tile.size,player.size)

Map = generateRoom()
room = Room(Map,firstQuadrant)
lt = 0
start()




while playing:
    t = time.time()
    clock.tick(200)

    display.fill((0,0,0))
#    for tile in specialObjects:
#        checkCollision(tile.position,player.position,tile.size,player.size)

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
