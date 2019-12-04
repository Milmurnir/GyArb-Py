import time
import pygame
import random
import keyboard
from win32api import * 

def LoadImage(Name,Size,transparency):
    Shortcut = "C:/Projects/GyArb-Py/Image"
    if transparency:
        Image = pygame.image.load(Shortcut+"/"+Name).convert_alpha()
    else:
        Image = pygame.image.load(Shortcut+"\\"+Name).convert()
    Image = pygame.transform.scale(Image,(Size,Size))
    return Image



def checkCollision(staticPosition,collidingPosition,staticSize,collidingSize):
    
    if collidingPosition[0] + collidingSize >= staticPosition[0] and collidingPosition[0] <= staticPosition[0] + staticSize:
        if collidingPosition[1] + collidingSize >= staticPosition[1] and collidingPosition[1] <= staticPosition[1] + staticSize:
            return True

class Tile:
    def __init__(self,position,size):
        self.position = position
        self.size = size
        self.sprite = LoadImage("base.png",self.size,False)
        self.quadrant = 0

        if self.position[0] < 1920/2 and self.position[1] < 1080/2:
            self.quadrant = 1
        
        elif self.position[0] > 1920/2 and self.position[1] < 1080/2:
            self.quadrant = 2  
        
        elif self.position[0] < 1920/2 and self.position[1] > 1080/2:
            self.quadrant = 3
        
        elif self.position[0] > 1920/2 and self.position[1] > 1080/2:
            self.quadrant = 4        
  

        
        

class Player:
    def __init__(self,position,display,movementSpeed,shootCooldown,shootingSpeed):
        self.position = position
        self.size = 119
        self.direction = 0
        self.movementSpeed = movementSpeed
        self.display = display
        self.sprite = LoadImage("player.png",self.size,True)
        self.shootCooldown = shootCooldown
        self.lastShoot = 0
        self.facingDirection = 1
        self.shotList = []
        self.shootingSpeed = shootingSpeed
        self.directionX = 0
        self.directionY = 0
        self.aimingDirection = (0,1)
        self.quadrant = None
        self.lastPosition = [0,0]
        self.roomNumber = 0

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

        
        self.lastPosition[0] = self.position[0]
        self.lastPosition[1] = self.position[1]
        self.position[0] += self.directionX * self.movementSpeed
        self.position[1] += self.directionY * self.movementSpeed

        if self.position[0] > 1920 - 2 *self.size + 20:
            self.position[0] = 1920 - 2 * self.size + 20

        elif self.position[0] < 0 + self.size - 20:
            self.position[0] = 0 + self.size - 20

        if self.position[1] < 0 + self.size:
            self.position[1] = 0 + self.size
        
        elif self.position[1] > 1080 - 2 * self.size:
            self.position[1] = 1080 - 2 * self.size
        

        if self.position[0] < 1920/2 and self.position[1] < 1080/2:
            self.quadrant = 1
        
        elif self.position[0] > 1920/2 and self.position[1] < 1080/2:
            self.quadrant = 2  
        
        elif self.position[0] < 1920/2 and self.position[1] > 1080/2:
            self.quadrant = 3
        
        elif self.position[0] > 1920/2 and self.position[1] > 1080/2:
            self.quadrant = 4        


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
        self.sprite = LoadImage("shot"+str(rnd)+".png",48,True)
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
        self.firstQuadrant = []
        self.secondQuadrant = []
        self.thirdQuadrant = []
        self.fourthQuadrant = []
        self.doors = []
    
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
                
                elif map[y][x] == 11:
                    tile.sprite = LoadImage("wallright.png",tile.size,False)
                
                elif map[y][x] == 3:
                    tile.sprite = LoadImage("wallcornerrightdown.png",tile.size,False)
                
                elif map[y][x] == 12:
                    tile.sprite = LoadImage("walldown.png",tile.size,False)
                
                elif map[y][x] == 4:
                    tile.sprite = LoadImage("wallcornerleftdown.png",tile.size,False)
                
                elif map[y][x] == 13:
                    tile.sprite = LoadImage("wallleft.png",tile.size,False)

                elif map[y][x] == 14:
                    tile.sprite = LoadImage("door.png",tile.size,True)
                    door = Door(tile.position)
                    self.doors.append(door)

                else:
                    if (map[y][x] % 2) == 0:
                        if tile.quadrant == 1:
                            self.firstQuadrant.append(tile)
                        
                        elif tile.quadrant == 2:
                            self.secondQuadrant.append(tile)
                        
                        elif tile.quadrant == 3:
                            self.thirdQuadrant.append(tile)
                        
                        elif tile.quadrant == 4:
                            self.fourthQuadrant.append(tile)

                    if map[y][x] == 28:
                        self.background.blit(tile.sprite,tile.position)
                        tile.sprite = LoadImage("stone.png",tile.size,True)
                      
                    
                    elif map[y][x] == 30:
                        self.background.blit(tile.sprite,tile.position)
                        tile.sprite = LoadImage("stone.png",tile.size,True)
                       
                    
                    elif map[y][x] == 32:
                        self.background.blit(tile.sprite,tile.position)
                        tile.sprite = LoadImage("stone.png",tile.size,True)
                        
                    
                    elif map[y][x] == 34:
                        self.background.blit(tile.sprite,tile.position)
                        tile.sprite = LoadImage("stone.png",tile.size,True)
                        
                    
                    elif map[y][x] == 36:
                        self.background.blit(tile.sprite,tile.position)
                        tile.sprite = LoadImage("stone.png",tile.size,True)
                       

                    elif map[y][x] == 38:
                        self.background.blit(tile.sprite,tile.position)
                        tile.sprite = LoadImage("stone.png",tile.size,True)
                        
                    
                    elif map[y][x] == 40:
                        self.background.blit(tile.sprite,tile.position)
                        tile.sprite = LoadImage("stone.png",tile.size,True)
                        

                    elif map[y][x] == 42:
                        self.background.blit(tile.sprite,tile.position)
                        tile.sprite = LoadImage("chest.png",tile.size,True)
                    
                    else:
                        pass
                        
                    

                self.background.blit(tile.sprite,tile.position)
    

class Door:
    def __init__(self,position):
        self.position = position
        self.size = 100
        if self.position[0] < 1920/2:
            self.transitionNumber = -1
        
        else:
            self.transitionNumber = 1
            self.position[0] += 20
        
    def checkTransision(self,player):
        col = checkCollision(self.position,player.position,self.size,player.size)
        if col:
            player.roomNumber += self.transitionNumber
            
            if self.transitionNumber == -1:
                player.position[0] = 1920 - 2 * player.size - 5
            
            elif self.transitionNumber == 1:
                player.position[0] = 0 + player.size

                
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