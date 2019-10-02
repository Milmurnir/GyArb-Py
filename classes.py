import pygame
import random
import keyboard
from win32api import * 

def LoadImage(Name,Size):
    Shortcut = "C:\Projects\GyArb-Py\Image"
    Image = pygame.image.load(Shortcut+"\\"+Name)
    Image = pygame.transform.scale(Image,(Size,Size))
    return Image


class Tile:
    def __init__(self,position,size,display):
        self.position = position
        self.size = size
        self.sprite = LoadImage("base.PNG",120)
        self.display = display
    
    def updateTile(self):
        self.display.blit(self.sprite,(self.position[0],self.position[1]))



class Player:
    def __init__(self,position,size,display,movementSpeed):
        self.position = position
        self.size = size
        self.direction = 0
        self.movementSpeed = movementSpeed
        self.display = display
        self.sprite = LoadImage("player.png",self.size)

    def drawPlayer(self):
        self.display.blit(self.sprite,(self.position[0],self.position[1]))
    
    def checkMovement(self):
        if keyboard.is_pressed("d"):
            self.DirectionX = 1
        
        elif keyboard.is_pressed("a"):
            self.DirectionX = -1
        
        else:
            self.DirectionX = 0
        
        if keyboard.is_pressed("w"):
            self.DirectionY = -1
        
        elif keyboard.is_pressed("s"):
            self.DirectionY = 1
        
        else:
            self.DirectionY = 0
        
        self.position[0] += self.DirectionX * self.movementSpeed
        self.position[1] += self.DirectionY * self.movementSpeed

