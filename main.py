import time
import pygame
import random
import keyboard
from classes import *
from win32api import *



display = pygame.display.set_mode((0,0), pygame.FULLSCREEN)

#display = pygame.display.set_mode((1920,1080))



clock = pygame.time.Clock()
player = Player([0,0],display,5,0.5,6)
resolution = (GetSystemMetrics(0),GetSystemMetrics(1))
playing = True
tileSize = 120
Map = []
roomList = []


class dumbRoom:
    def __init__(self,position,doors):
        self.position = position
        self.doors = doors


def start():
    pygame.init()
    
def generateMaze():

    maze = [
# generera maze utått och dra då en random på hur många dörrar den ska ha för att fatta hur resten ska generera det borde vara scalable också :)
        [0,1,0],
        [1,1,0],
        [0,0,0]

    ]
#ta in rummens position för dörr beräkning?
    for y in maze:
        for x in y:
            maze[y].remove[x]
            test = dumbRoom([x,y],2)
            maze[y].append()

    return maze


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
        [14,0,0,s,0,q,c,0,0,c,q,0,s,0,0,14],
        [13,0,m,o,0,0,p,r,r,p,0,0,o,m,0,11],
        [13,0,n,0,0,0,0,0,0,0,0,0,0,n,0,11],
        [13,0,0,0,0,0,0,0,0,0,0,0,0,0,0,11],
        [4,12,12,12,12,12,12,12,12,12,12,12,12,12,12,3]
    ]
    return baseMap



def blitRoom(playerRoomNumber,roomList):
    display.blit(roomList[playerRoomNumber].background,(0,0))

    
def update():
   
# kan optimeras
    blitRoom(player.roomNumber,roomList)

    
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

    for door in room.doors:
        door.checkTransision(player)
        
  

    if player.quadrant == 1:
        for tile in room.firstQuadrant:
            collision = checkCollision(tile.position,player.position,tile.size,player.size)
            if collision == True:
                player.position[0] = player.lastPosition[0]
                player.position[1] = player.lastPosition[1]

    elif player.quadrant == 2:
        for tile in room.secondQuadrant:
            collision = checkCollision(tile.position,player.position,tile.size,player.size)
            if collision == True:
                player.position[0] = player.lastPosition[0]
                player.position[1] = player.lastPosition[1]

    elif player.quadrant == 3:
        for tile in room.thirdQuadrant:
            collision = checkCollision(tile.position,player.position,tile.size,player.size)
            if collision == True:
                player.position[0] = player.lastPosition[0]
                player.position[1] = player.lastPosition[1]

    elif player.quadrant == 4:
        for tile in room.fourthQuadrant:
            collision = checkCollision(tile.position,player.position,tile.size,player.size)
            if collision == True:
                player.position[0] = player.lastPosition[0]
                player.position[1] = player.lastPosition[1]


Map = generateRoom()
room = Room(Map)
roomList.append(room)


lt = 0
start()
#generateMaze()

while playing:
    t = time.time()
    display.fill((0,0,0))

    update()
    room = roomList[player.roomNumber]
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            playing = False
            break 

        if keyboard.is_pressed("esc"):
            playing = False
    
    if keyboard.is_pressed("g"):
        Map = generateRoom()
        room = Room(Map)
        roomList.append(room)

    elapsed = t - lt
    lt = t
    
    
    if keyboard.is_pressed("f"):
        print("Frames per second "+str(1/elapsed))
