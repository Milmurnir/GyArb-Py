import time
import pygame
import random
import keyboard
import arcade
from win32api import * 

def LoadImage(Name,size,position):
    sprite = arcade.Sprite("C:\Projects\GyArb-Py\TestArcade\Images"+"\\"+Name+".png",size)
    sprite.center_x += position[0]
    sprite.center_y += position[1]
    return sprite

def collisionPossible(firstPosition, secondPosition):
    diff_vector = [secondPosition[0] - firstPosition[0], secondPosition[1] - firstPosition[1]]
    length_pow2 = pow(diff_vector[0], 2) + pow(diff_vector[1], 2)

    if(length_pow2 < 57600.0): # 57600 is pow 2 of 240, desired check distance
        return True
    return False


def checkCollision(staticPosition,collidingPosition,staticSize,collidingSize):
    col = collisionPossible(staticPosition,collidingPosition)
    if col:
        if collidingPosition[0] + collidingSize/2 >= staticPosition[0] - staticSize/2 and collidingPosition[0] <= staticPosition[0] + staticSize:
            if collidingPosition[1] + collidingSize/2 >= staticPosition[1] - staticSize/2 and collidingPosition[1] <= staticPosition[1] + staticSize:
                return True

class Tile:
    def __init__(self,position):
        self.position = position
        self.size = 120
        self.sprite = LoadImage("base",1,self.position)
        self.quadrant = 0

        if self.position[0] < 1920/2 and self.position[1] > 1080/2:
            self.quadrant = 1
        
        elif self.position[0] > 1920/2 and self.position[1] > 1080/2:
            self.quadrant = 2  
        
        elif self.position[0] < 1920/2 and self.position[1] < 1080/2:
            self.quadrant = 3
        
        elif self.position[0] > 1920/2 and self.position[1] < 1080/2:
            self.quadrant = 4        
  

        
class Player:
    def __init__(self,position,movementSpeed,shootCooldown,shootingSpeed,shotDamage):
        self.position = position
        self.size = 100
        self.health = 5
        self.movementSpeed = movementSpeed
        self.sprite = LoadImage("boi",1,self.position)
        self.shootCooldown = shootCooldown
        self.shootingSpeed = shootingSpeed
        self.shotDamage = shotDamage
        self.lastShoot = 0
        self.facingDirection = 1
        self.directionX = 0
        self.directionY = 0
        self.aimingDirection = (0,1)
        self.lastPosition = [0,0]
        self.worldCord = [0,0]
        self.shotList = []
        self.shotSpriteList = arcade.SpriteList()
        self.spriteList = arcade.SpriteList()
        self.spriteList.append(self.sprite)
        self.alive = True
        
    def checkKeyStrokes(self):
            
        if self.directionX > 0:
            self.aimingDirection = (1,0)
        
        elif self.directionX < 0:
            self.aimingDirection = (-1,0)

        elif self.directionY > 0:
            self.aimingDirection = (0,1)
        
        elif self.directionY < 0:
            self.aimingDirection = (0,-1)

        

        if self.position[0] < 1920/2 and self.position[1] > 1080/2:
            self.quadrant = 1
        
        elif self.position[0] > 1920/2 and self.position[1] < 1080/2:
            self.quadrant = 2  
        
        elif self.position[0] < 1920/2 and self.position[1] < 1080/2:
            self.quadrant = 3
        
        elif self.position[0] > 1920/2 and self.position[1] < 1080/2:
            self.quadrant = 4        


        if keyboard.is_pressed("space"):
            if time.time() - self.lastShoot >= self.shootCooldown:
                self.lastShoot = time.time()
                shot = Shot(self.aimingDirection,self.shootingSpeed,self.position,"shot",self.shotDamage)
                self.shotList.append(shot)
                self.shotSpriteList.append(shot.sprite)

                
            

class Shot:
    def __init__(self,aimingDirection,speed,position,name,damage):
        self.direction = aimingDirection
        self.speed = speed * 15
        self.X = position[0]
        self.Y = position[1]
        self.position = [self.X,self.Y]
        rnd = random.randrange(2)
        self.sprite = LoadImage(name+str(rnd),1,self.position)
        self.size = 40
        self.col = False
        self.damage = damage

    def updateShot(self,delta_time):
        if self.direction[1] == 1:
            self.Y += self.speed * delta_time

        elif self.direction[1] == -1:
            self.Y -= self.speed * delta_time
        
        elif self.direction[0] == 1:
            self.X += self.speed * delta_time

        elif self.direction[0] == -1:
            self.X -= self.speed * delta_time

    def checkIfHit(self,hitObject):
        col = checkCollision(hitObject.position,[self.X,self.Y],hitObject.size,self.size)
        if col:
            self.col = True
            
class Room:
    def __init__(self,Map,player):
        self.tileSize = 120
        self.doors = []
        self.tileSpriteList = arcade.SpriteList()
        self.collisionList = []
        self.enemyList = []

        for y in range(9):
            yCord = y* 120 + 60
            for x in range(16):
                xCord = x * 120 + 60

                self.tilePosition = [xCord,yCord]
                tile = Tile(self.tilePosition)
               

                if Map[y][x] == 0:
                    tile.sprite = LoadImage("base",1,tile.position)
        
                elif Map[y][x] == 4:
                    tile.sprite = LoadImage("wallCornerLeftUp",1,tile.position)
                
                elif Map[y][x] == 12:
                    tile.sprite = LoadImage("wallUp",1,tile.position)
                
                elif Map[y][x] == 3:
                    tile.sprite = LoadImage("wallcornerrightup",1,tile.position)
                
                elif Map[y][x] == 11:
                    tile.sprite = LoadImage("wallright",1,tile.position)
                
                elif Map[y][x] == 2:
                    tile.sprite = LoadImage("wallcornerrightdown",1,tile.position)
                
                elif Map[y][x] == 10:
                    tile.sprite = LoadImage("walldown",1,tile.position)
                
                elif Map[y][x] == 1:
                    tile.sprite = LoadImage("wallcornerleftdown",1,tile.position)
                
                elif Map[y][x] == 13:
                    tile.sprite = LoadImage("wallleft",1,tile.position)
                
                elif Map[y][x] == 14:
                    tile.sprite = LoadImage("door",7.5,tile.position)
                    door = Door(tile.position)
                    self.doors.append(door)
        

                if Map[y][x] == 28:
                    self.collisionList.append(tile)
                    tile.sprite = LoadImage("stone",1,tile.position)
                    
                
                elif Map[y][x] == 30:
                    self.collisionList.append(tile)
                    tile.sprite = LoadImage("stone",1,tile.position)
                    
                
                elif Map[y][x] == 32:
                    self.collisionList.append(tile)
                    tile.sprite = LoadImage("stone",1,tile.position)
                    
                
                elif Map[y][x] == 34:
                    self.collisionList.append(tile)
                    tile.sprite = LoadImage("stone",1,tile.position)
                    
                
                elif Map[y][x] == 36:
                    self.collisionList.append(tile)
                    tile.sprite = LoadImage("mushroom",1,tile.position)
                    enemy = EnemyShoot(tile.position,player,5,5,tile.sprite)
                    self.enemyList.append(enemy)
                    

                elif Map[y][x] == 38:
                    self.collisionList.append(tile)
                    tile.sprite = LoadImage("stone",1,tile.position)
                    
                
                elif Map[y][x] == 40:
                    self.collisionList.append(tile)
                    tile.sprite = LoadImage("stone",1,tile.position)
                    

                elif Map[y][x] == 42:
                    self.collisionList.append(tile)
                    tile.sprite = LoadImage("chest1",1,tile.position)
                

                
                self.tileSpriteList.append(tile.sprite)
            
            
                    
    

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
            player.worldCord[0] += self.transitionNumber
            
            if self.transitionNumber == -1:
                player.position[0] = 1920 - 2 * player.size - 5
            
            elif self.transitionNumber == 1:
                player.position[0] = 0 + player.size




class EnemyShoot:
    def __init__(self,position,player,shotCooldown,shotDamage,sprite):
        self.position = position
        self.health = 1
        self.size = 120
        self.player = player
        self.shotCooldown = shotCooldown
        self.damage = shotDamage
        self.stillhit = 0
        self.aimDirection = [0,0]
        self.spriteShotList = arcade.SpriteList()
        self.shotList = []
        self.lastShot = 0
        self.sprite = sprite
        self.alive = True

    def hitPossible(self):
        if self.health > 0:
            self.aimDirection = [0,0]

            if self.player.position[0] - 60 < self.position[0] + 60 and self.player.position[0] + 60 > self.position[0] - 60:
    
                if self.player.position[1] < self.position[1]:
                    self.aimDirection[1] = -1
                
                else:
                    self.aimDirection[1] = 1
                if time.time() - self.lastShot >= self.shotCooldown:
                    self.lastShot = time.time()
                    shot = Shot(self.aimDirection,20,self.position,"enemyShot",self.damage)
                    self.spriteShotList.append(shot.sprite)
                    self.shotList.append(shot)
            
            
            
            if self.player.position[1] - 60 < self.position[1] + 60 and self.player.position[1] + 60 > self.position[1] - 60:
                self.stillhit += 1
                if self.player.position[0] < self.position[0]:
                    self.aimDirection[0] = -1
                
                else:
                    self.aimDirection[0] = 1
                
                if time.time() - self.lastShot >= self.shotCooldown:
                    self.lastShot = time.time()

                    shot = Shot(self.aimDirection,10,self.position,"enemyShot",self.damage)
                    self.spriteShotList.append(shot.sprite)
                    self.shotList.append(shot)
            

        
            


"""
        


class chest11:
    def __init__(self,position,tileSize,roomPosition):
        self.item = None
        self.position = position
        self.tileSize = tileSize
        self.sprite = LoadImage("chest1",self.tileSize,tile.position)
        self.roomPosition = roomPosition
        self.open = False

    def checkOpen(self,playerPosition,playerSize):
        if keyboard.is_pressed("e") and self.open == False:
            self.open = checkCollision(self.position,playerPosition,playerSize,self.tileSize,self.roomPosition)
            self.item = PowerUp(self.position,64)

    def drawchest1(self,display):
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
        self.sprite = LoadImage("stone",size,tile.position)
        self.HP = 2
        self.damage = 0
        self.movementSpeed = 0
        self.special = None


class DamagePowerUp:
    def __init__(self,size):
        self.HP = 0
        self.damage = 0.5
        self.movementSpeed = 0
        self.special = None


class MovementPowerUp:
    def __init__(self,size):
        self.HP = 0
        self.damage = 0
        self.movementSpeed = 0.5
        self.special = None
"""