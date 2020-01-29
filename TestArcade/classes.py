import time
import pygame
import random
import keyboard
import arcade
import math
import time
from win32api import * 
import os

def LoadImage(Name,size,position,animation = False,animationFolder = ""):
    if animation:
        sprite = arcade.Sprite("C:\Projects\GyArb-Py\TestArcade\Animations"+"\\"+animationFolder+"\\"+Name,size)
    else:
        sprite = arcade.Sprite("C:\Projects\GyArb-Py\TestArcade\Images"+"\\"+Name+".png",size)
    sprite.center_x += position[0]
    sprite.center_y += position[1]
    return sprite

def LoadAnimaitonTree(Directory,size,spriteList,position):
    for pic in os.listdir(Directory):
        sprite = arcade.Sprite(Directory+"\\"+pic,size)
        sprite.center_x += position[0]
        sprite.center_y += position[1]
        spriteList.append(sprite)
    


def collisionPossible(firstPosition, secondPosition):
    diff_vector = [secondPosition[0] - firstPosition[0], secondPosition[1] - firstPosition[1]]
    length_pow2 = pow(diff_vector[0], 2) + pow(diff_vector[1], 2)

    if(length_pow2 < 57600.0): # 57600 is pow 2 of 240, desired check distance
        return True
    return False


def checkCollision(staticPosition,collidingPosition,staticSize,collidingSize):
    col = collisionPossible(staticPosition,collidingPosition)
    if col:
        if collidingPosition[0] + collidingSize/2 > staticPosition[0] - staticSize/2 and collidingPosition[0] < staticPosition[0] + staticSize:
            if collidingPosition[1] + collidingSize/2 > staticPosition[1] - staticSize/2 and collidingPosition[1] < staticPosition[1] + staticSize:
                return True

class Tile:
    def __init__(self,position):
        self.position = position
        self.size = 120
        self.sprite = LoadImage("base",1,self.position)
            
  

        
class Player:
    def __init__(self,position,movementSpeed,shootCooldown,shootingSpeed,shotDamage):
        self.position = position
        self.size = 100
        self.health = 500000000
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
        self.lastHit = 0
        
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
        self.doorExist = [False,False,False,False]
        self.chestList = []
        

        for y in range(9):
            yCord = y* 120 + 60
            for x in range(15):
                xCord = x * 120 + 180

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
                

                elif Map[y][x] == 70:
                    tile.sprite = LoadImage("door",7.5,tile.position)
                    door = Door(tile.position)
                    self.doors.append(door)
                
                elif Map[y][x] == 71:
                    tile.sprite = LoadImage("door",7.5,tile.position)
                    door = Door(tile.position)
                    self.doors.append(door)
                
                elif Map[y][x] == 72:
                    tile.sprite = LoadImage("door",7.5,tile.position)
                    door = Door(tile.position)
                    self.doors.append(door)
                
                elif Map[y][x] == 73:
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
                    enemy = EnemyShoot(tile.position,player,5,5,tile.sprite,len(self.collisionList)-1)
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
                    chest = chest1(tile.position,120)
                    self.chestList.append(chest)
                

                self.tileSpriteList.append(tile.sprite)
                
            
            
                    
    

class Door:
    def __init__(self,position):
        self.position = position
        self.size = 140
        self.xOrYDoor = None

        if self.position[0] < 300:
            self.transitionNumberX = -1
            self.xOrYDoor = 0
        
        elif self.position[0] > 1700:
            self.transitionNumberX = 1
            self.xOrYDoor = 0


        if self.position[1] < 300:
            self.transitionNumberY = 1
            self.xOrYDoor = 1
        
        elif self.position[1] > 700:
            self.transitionNumberY = -1
            self.xOrYDoor = 1
        
    def checkTransision(self,player):
        col = checkCollision(self.position,player.position,self.size,player.size)
        if col:
            if self.xOrYDoor == 0:
                player.worldCord[0] += self.transitionNumberX

                if self.transitionNumberX == -1:
                    player.position[0] = 1920 - 2 * player.size - 5
                
                else:
                    player.position[0] = 360
            
            elif self.xOrYDoor == 1:
                player.worldCord[1] += self.transitionNumberY
            
                if self.transitionNumberY == -1:
                    player.position[1] = 240
                    
                else:
                    player.position[1] = 1080 - 240
                




class EnemyShoot:
    def __init__(self,position,player,shotCooldown,shotDamage,sprite,index):
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
        self.type = "shooting"
        self.animation = False
        self.indexCollision = index

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
            

        
class FlyingEnemy:
    def __init__(self,position,size,cooldown):
        self.position = position
        self.size = size
        self.spriteList = arcade.SpriteList()
        self.type = "flying"
        self.moveVector = [0,0]
        self.targetPos = [0,0]
        self.cooldown = cooldown
        self.lastAttack = 0
        self.enableToMove = True
        self.damage = 1
        self.alive = True
        self.health = 1
        self.animation = True

        for i in os.listdir("C:\Projects\GyArb-Py\TestArcade\Animations\BombFlying"):
            sprite = LoadImage(str(i),3,self.position,True,"BombFlying")
            self.spriteList.append(sprite)
        
        self.animationPlayer = AnimationPlayer(self.spriteList,10)

    def moveEnemyToPlayer(self,player):
        if self.alive:
            self.animationPlayer.runAnimation()

            if time.time() - self.lastAttack >= self.cooldown:
                self.lastAttack = time.time()
                self.enableToMove = True
                self.targetPos[0] = player.position[0]
                self.targetPos[1] = player.position[1]
            
            if self.enableToMove:
            
                self.tempPosition = [0,0]
                self.moveVector[0] = self.targetPos[0] - self.position[0]
                self.moveVector[1] = self.targetPos[1] - self.position[1]
                
                self.length = math.sqrt(self.moveVector[0]**2+self.moveVector[1]**2)

                if self.length == 0:
                    self.length = 1
                self.moveVector[0] /= self.length
                self.moveVector[1] /= self.length
                
                movementSpeed = 10
                if self.length < 10:
                    movementSpeed = self.length

                self.position[0] += self.moveVector[0] * movementSpeed
                self.position[1] += self.moveVector[1] * movementSpeed

                self.vectorPos = [0,0]
                
                i = 0

                while True:
                    i += 1
                    enemyPos = [0]
                    enemyPos[0] = self.position[0]
                    
                    if enemyPos[0] + self.moveVector[0] * 1 + i > player.position[0] and enemyPos[0] + self.moveVector[0] * 1 + i < player.position[0] + player.size:
                        self.vectorPos[0] = enemyPos[0]
                        break
                    else:
                        enemyPos[0] += self.moveVector[0] * 1 

                
                    self.tempPosition[0] = enemyPos[0]

                    if i > 200:
                        break
                
                o = 0

                while True:
                    o += 1
                    enemyPos = [0]
                    enemyPos[0] = self.position[1]
                    
                    if enemyPos[0] + self.moveVector[1] * 1 + i > player.position[1] and enemyPos[0] + self.moveVector[1] * 1 + i < player.position[1] + player.size:
                        self.vectorPos[1] = enemyPos[0]
                        break
                    else:
                        enemyPos[0] += self.moveVector[1] * 1

                    
                    self.tempPosition[1] = enemyPos[0]

                    if o > 200:
                        break
                
                

                col = checkCollision(self.tempPosition,self.targetPos,50,player.size)
                if col:
                    self.enableToMove = False
            
                else:
                    self.enableToMove = True

                


class AnimationPlayer:
    def __init__(self,spriteList,animaitonSpeed):
        self.spriteList = spriteList
        self.currentPicture = 1
        self.animationSpeed = animaitonSpeed
        self.maxAnimationState = self.animationSpeed * len(self.spriteList)
        self.animationState = 0

    def runAnimation(self):
        self.animationState += 1
        if self.animationState == self.animationSpeed * self.currentPicture:
            self.currentPicture += 1
            
            
        if self.animationState >= self.maxAnimationState:
            self.animationState = 0
            
        if self.currentPicture -1 >= len(self.spriteList):
            self.currentPicture = 1
            

        

class chest1:
    def __init__(self,position,tileSize):
        self.item = None
        self.position = position
        self.tileSize = tileSize
        self.sprite = LoadImage("chest1",self.tileSize,self.position)
        self.open = False
        self.powerUpSize = 1

    def checkOpen(self,playerPosition,playerSize):
        if keyboard.is_pressed("e") and self.open == False:
            self.open = checkCollision(self.position,playerPosition,playerSize,self.tileSize)
            rnd = random.randrange(0,1)
            if rnd == 0:
                self.item = HeartPowerUp(self.position,self.powerUpSize)
            
            elif rnd == 1:
                self.item = DamagePowerUp(self.position,self.powerUpSize)

            elif rnd == 2:
                self.item = MovementPowerUp(self.position,self.powerUpSize)

    


class PowerUp:
    def __init__(self,position,size):
        self.position = position
        self.powerItem = None
        self.sprite = None
        rnd = random.randrange(0,1)
        if rnd == 0:
            self.powerItem = HeartPowerUp(self.position,size)
        
        if rnd == 1:
            self.powerItem = DamagePowerUp(self.position,size)

        if rnd == 2:
            self.powerItem = MovementPowerUp(self.position,size)
            

class HeartPowerUp:
    def __init__(self,position,size):
        self.sprite = LoadImage("stone",size,position+[100,100])
        self.HP = 1
        self.damage = 0
        self.movementSpeed = 0
        self.special = None


class DamagePowerUp:
    def __init__(self,position,size):
        self.HP = 0
        self.damage = 0.5
        self.movementSpeed = 0
        self.special = None


class MovementPowerUp:
    def __init__(self,position,size):
        self.HP = 0
        self.damage = 0
        self.movementSpeed = 0.5
        self.special = None
