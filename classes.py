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
    def __init__(self,position,size):
        self.position = position
        self.size = size
        self.sprite = LoadImage("base.PNG",120)
    
    def updateTile(self):
        pygame.blit(self.sprite,(self.size,self.size))