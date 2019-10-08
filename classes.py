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
    def __init__(self,position,size,display):
        self.position = position
        self.size = size
        self.sprite = LoadImage("base.PNG",120,False)
        self.display = display
    def updateTile(self):
        self.display.blit(self.sprite,(self.position[0],self.position[1]))



class Player:
    def __init__(self,position,size,display,movementSpeed,shootCooldown,shootingSpeed):
        self.position = position
        self.size = size
        self.direction = 0
        self.movementSpeed = movementSpeed
        self.display = display
        self.sprite = LoadImage("enemy0.png",self.size,True)
        self.shootCooldown = shootCooldown
        self.lastShoot = None
        self.facingDirection = 1
        self.shotList = []
        self.shootingSpeed = shootingSpeed

    def drawPlayer(self):
        self.display.blit(self.sprite,(self.position[0],self.position[1]))
        
    
    def checkKeyStrokes(self):
        if keyboard.is_pressed("d"):
            self.DirectionX = 1
            self.facingDirection = 2
        
        elif keyboard.is_pressed("a"):
            self.DirectionX = -1
            self.facingDirection = 4
        
        else:
            self.DirectionX = 0
        
        if keyboard.is_pressed("w"):
            self.DirectionY = -1
            self.facingDirection = 3
        
        elif keyboard.is_pressed("s"):
            self.DirectionY = 1
            self.facingDirection = 1
        
        else:
            self.DirectionY = 0
        
        self.position[0] += self.DirectionX * self.movementSpeed
        self.position[1] += self.DirectionY * self.movementSpeed

        if keyboard.is_pressed("space"):
            if self.lastShoot == None:
                self.lastShoot = time.time()
            elif time.time() - self.lastShoot >= self.shootCooldown:
                self.lastShoot = time.time()
                shot = Shot(self.facingDirection,self.shootingSpeed,self.position,self.display)
                self.shotList.append(shot)
                print(len(self.shotList))
            

class Shot:
    def __init__(self,headingDirection,speed,playerPosition,display):
        self.headingDirection = headingDirection
        self.speed = speed
        self.X = playerPosition[0]
        self.Y = playerPosition[1]
        rnd = random.randrange(2)
        self.sprite = LoadImage("shot"+str(rnd)+".png",32,True)
        self.display = display

    def drawShot(self):
        self.display.blit(self.sprite,(self.X+32,self.Y+32))

    def updateShot(self):
        if self.headingDirection == 1:
            self.Y += self.speed

        if self.headingDirection == 2:
            self.X += self.speed
        
        if self.headingDirection == 3:
            self.Y -= self.speed
        
        if self.headingDirection == 4:
            self.X -= self.speed
        

