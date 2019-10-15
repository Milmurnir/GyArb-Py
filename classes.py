import time
import pygame
import random
import keyboard
from win32api import * 

def LoadImage(Name,Size,transparency):
    Shortcut = "C:\Projects\GyArb-Py\Image"
    if transparency:
        Image = pygame.image.load(Shortcut+"\\"+Name).convert_alpha()
    else:
        Image = pygame.image.load(Shortcut+"\\"+Name).convert()
    Image = pygame.transform.scale(Image,(Size,Size))
    return Image


class Tile:
    def __init__(self,position,size):
        self.position = position
        self.size = size

        if position[0] == 300:
            self.sprite = LoadImage("wallright.PNG",self.size,False)
        
        elif position[0] == 1620:
            self.sprite = LoadImage("wallleft.png",self.size,False)

        elif position[1] == 75:
            self.sprite = LoadImage("walldown.png",self.size,False)

        elif position[1] == 795:
            self.sprite = LoadImage("wallup.PNG",self.size,False)

        else:
            self.sprite = LoadImage("base.png",self.size,False)
        

class Player:
    def __init__(self,position,display,movementSpeed,shootCooldown,shootingSpeed):
        self.position = position
        self.size = 120
        self.direction = 0
        self.movementSpeed = movementSpeed
        self.display = display
        self.sprite = LoadImage("enemy0.png",self.size,True)
        self.shootCooldown = shootCooldown
        self.lastShoot = 0
        self.facingDirection = 1
        self.shotList = []
        self.shootingSpeed = shootingSpeed
        self.directionX = 0
        self.directionY = 0
        self.aimingDirection = (0,1)


    def drawPlayer(self):
        self.display.blit(self.sprite,(self.position[0],self.position[1]))
        
    def checkKeyStrokes(self):
        if keyboard.is_pressed("d"):
            self.directionX = 1


        elif keyboard.is_pressed("a"):
            self.directionX = -1

        else:
            self.directionX = 0
            

        if keyboard.is_pressed("w"):
            self.directionY = -1
            
        
        elif keyboard.is_pressed("s"):
            self.directionY = 1
        
        else:
            self.directionY = 0
            

        if self.directionX > 0:
            self.aimingDirection = (1,0)
        
        elif self.directionX < 0:
            self.aimingDirection = (-1,0)

        elif self.directionY > 0:
            self.aimingDirection = (0,1)
        
        elif self.directionY < 0:
            self.aimingDirection = (0,-1)


        self.position[0] += self.directionX * self.movementSpeed
        self.position[1] += self.directionY * self.movementSpeed

        if keyboard.is_pressed("space"):
            if time.time() - self.lastShoot >= self.shootCooldown:
                self.lastShoot = time.time()
                shot = Shot(self.aimingDirection,self.shootingSpeed,self.position,self.display)
                self.shotList.append(shot)
                
            

class Shot:
    def __init__(self,aimingDirection,speed,playerPosition,display):
        self.direction = aimingDirection
        self.speed = speed
        self.X = playerPosition[0]
        self.Y = playerPosition[1]
        rnd = random.randrange(2)
        self.sprite = LoadImage("shot"+str(rnd)+".png",32,True)
        self.display = display

    def drawShot(self):
        self.display.blit(self.sprite,(self.X+32,self.Y+32))

    def updateShot(self):
        if self.direction[1] == 1:
            self.Y += self.speed

        elif self.direction[1] == -1:
            self.Y -= self.speed
        
        elif self.direction[0] == 1:
            self.X += self.speed

        elif self.direction[0] == -1:
            self.X -= self.speed




class Chest:
    def __init__(self):
        pass


class Room:
    def __init__(self,resolution,tileSize):
        self.roomSize = (12,7)
        self.resolution = resolution
        self.background = pygame.Surface(self.resolution)
        self.tileSize = tileSize
        
    
    def makeRoom(self):
        for i in range(self.roomSize[1]):
            yCord = i * self.tileSize + 75
            for o in range(self.roomSize[0]):
                xCord = o * self.tileSize + 300
                tile = Tile((xCord,yCord),self.tileSize)

                self.background.blit(tile.sprite,tile.position)
        
        return self.background
