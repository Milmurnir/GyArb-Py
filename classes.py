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

def checkCollision(staticPosition,collidingPosition,staticSize,collidingSize):
    if collidingPosition[0] + collidingSize >= staticPosition[0] and collidingPosition[0] <= staticPosition[0] + staticSize:
        if collidingPosition[1] + collidingSize >= staticPosition[1] and collidingPosition[1] <= staticPosition[1] + staticSize:
            print("collisin")
            return True

class Tile:
    def __init__(self,position,size):
        self.position = position
        self.size = size
        self.sprite = LoadImage("base.png",self.size,False)

"""
        if self.position[0] == 0:
            self.sprite = LoadImage("wallLeft.png",self.size,False)
        
        if self.position[0] == 1920 - self.size:
            self.sprite = LoadImage("wallRight.png",self.size,False)

        if self.position[1] == 0:
            self.sprite = LoadImage("wallUp.png",self.size,False)
        
        if self.position[1] == 1080 - self.size:
            self.sprite = LoadImage("wallDown.png",self.size,False)
        
        if self.position[0] == 0 and self.position[1] == 0:
            self.sprite = LoadImage("wallCornerLeftUp.png",self.size,False)
        
        elif self.position[0] == 1920 - self.size and self.position[1] == 0:
            self.sprite = LoadImage("wallCornerRightUp.png",self.size,False)
        
        elif self.position[0] == 1920 - self.size and self.position[1] == 1080 - self.size:
            self.sprite = LoadImage("wallCornerRightDown.png",self.size,False)
        
        elif self.position[0] == 0 and self.position[1] == 1080 - self.size:
            self.sprite = LoadImage("wallCornerLeftDown.png",self.size,False)
        """
        
        

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

        if self.position[0] > 1920 - 2 *self.size:
            self.position[0] = 1920 - 2 * self.size

        if self.position[0] < 0 + self.size:
            self.position[0] = 0 + self.size

        if self.position[1] < 0 + self.size:
            self.position[1] = 0 + self.size
        
        if self.position[1] > 1080 - 2 * self.size:
            self.position[1] = 1080 - 2 * self.size

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


class Room:
    def __init__(self,map):
        self.background = pygame.Surface((1920,1080))
        self.tileSize = 120
    
        for y in range(9):
            yCord = y * self.tileSize
            for x in range(16):
                xCord = x * self.tileSize

                tile = Tile([xCord,yCord],self.tileSize)
                if map[y][x] == 0:
                    tile.sprite = LoadImage("base.png",tile.size,False)
                
                elif map[y][x] == 1:
                    tile.sprite = LoadImage("wallCornerLeftUp.png",tile.size,False)
                
                elif map[y][x] == 10:
                    tile.sprite = LoadImage("wallUp.png",tile.size,False)
                
                elif map[y][x] == 2:
                    tile.sprite = LoadImage("wallcornerrightup.png",tile.size,False)
                
                elif map[y][x] == 13:
                    tile.sprite = LoadImage("wallright.png",tile.size,False)
                
                elif map[y][x] == 3:
                    tile.sprite = LoadImage("wallcornerrightdown.png",tile.size,False)
                
                elif map[y][x] == 12:
                    tile.sprite = LoadImage("walldown.png",tile.size,False)
                
                elif map[y][x] == 4:
                    tile.sprite = LoadImage("wallcornerleftdown.png",tile.size,False)
                
                elif map[y][x] == 11:
                    tile.sprite = LoadImage("wallleft.png",tile.size,False)
                
                
                
                self.background.blit(tile.sprite,tile.position)
    



"""

class Room:
    def __init__(self,tileSize,roomOffset):
        self.TileXY = (12,8)
        self.roomSize = (1920,1080)
        self.background = pygame.Surface(self.roomSize)
        self.tileSize = tileSize
        self.tiles = []
        self.roomOffset = roomOffset
    
    def makeRoom(self,specials):
        for i in range(self.TileXY[1]):
            yCord = i * self.tileSize + self.roomOffset[1]
            for o in range(self.TileXY[0]):
                xCord = o * self.tileSize + self.roomOffset[0]
                tile = Tile([xCord,yCord],self.tileSize,self.roomSize)
                self.tiles.append(tile)
                self.background.blit(tile.sprite,tile.position)
"""
                


                
"""
        


class Chest:
    def __init__(self,position,tileSize,roomPosition):
        self.item = None
        self.position = position
        self.tileSize = tileSize
        self.sprite = LoadImage("chest.png",self.tileSize,True)
        self.roomPosition = roomPosition
        self.open = False

    def checkOpen(self,playerPosition,playerSize):
        if keyboard.is_pressed("e") and self.open == False:
            self.open = checkCollision(self.position,playerPosition,playerSize,self.tileSize,self.roomPosition)
            self.item = PowerUp(self.position,64)

    def drawChest(self,display):
        display.blit(self.sprite,self.position)
        if self.item.sprite != None:
            display.blit(self.item.sprite,self.item.position)

class PowerUp:
    def __init__(self,position,size):
        self.position = position
        self.powerItem = None
        self.sprite = None
        rnd = random.randrange(0,1)
        if rnd == 0:
            self.powerItem = HeartPowerUp(size)
        
        if rnd == 1:
            self.powerItem = DamagePowerUp(size)

        if rnd == 2:
            self.powerItem = MovementPowerUp(size)
            

class HeartPowerUp:
    def __init__(self,size):
        self.sprite = LoadImage("stone.png",size,True)
        self.HP = 2
        self.damage = 0
        self.movementSpeed = 0
        self.special = None

class DamagePowerUp:
    def __init__(self,size):
        self.HP = 0
        self.damage = 2
        self.movementSpeed = 0
        self.special = None

class MovementPowerUp:
    def __init__(self,size):
        self.HP = 0
        self.damage = 0
        self.movementSpeed = 0.5
        self.special = None
"""