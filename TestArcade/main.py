
import arcade
import keyboard
import random
from classes import *
import pyglet


def generateMaze(player):
    

    maze = [
        [0,0,0],
        [0,0,0],
        [0,0,0]
    ]
    
    xCord = random.randint(0,2)
    yCord = random.randint(0,2)

    player.worldCord[0] = xCord
    player.worldCord[1] = yCord

    generateRoom(maze,player,[xCord,yCord],[False,False,False,False])



    return maze


def generateRoom(maze,player,cords,forcedDoors=[False,False,False,False]):

    m = random.randint(28,29)
    n = random.randint(30,31)
    o = random.randint(32,33)
    p = random.randint(34,35)
    q = random.randint(36,37)
    r = random.randint(38,39)
    s = random.randint(40,41)
    c = random.randint(42,43)

    d1 = 14
    d2 = 14
    d3 = 14
    d4 = 14

    forcedD1 = False
    forcedD2 = False
    forcedD3 = False
    forcedD4 = False


    if forcedDoors[0]:
        d1 = 70
        forcedD1 = True
    
    else:
        rnd = random.randint(1,2)
        if rnd == 1 and cords[0] + 1 != 3:
            d1 = 70
    
    if forcedDoors[1]:
        d2 = 71
        forcedD2 = True

    else:
        rnd = random.randint(1,2)
        if rnd == 1 and cords[1] - 1 != -1:
            d2 = 71
    
    if forcedDoors[2]:
        d3 = 72
        forcedD3 = True
    
    else:
        rnd = random.randint(1,2)
        if rnd == 1 and cords[0] - 1 != -1:
            d3 = 72
    
    if forcedDoors[3]:
        d4 = 73
        forcedD4 = True
    
    else:
        rnd = random.randint(1,2)
        if rnd == 1 and cords[1] + 1 != 3:
            d4 = 73
    


    baseMap = [
        [1,10,10,10,10,10,10,d4,10,10,10,10,10,10,2],
        [13,0,0,0,0,0,0,0,0,0,0,0,0,0,11],
        [13,0,0,0,0,0,0,0,0,0,0,0,0,0,11],
        [13,0,0,0,0,0,0,o,0,0,0,0,0,0,11],
        [d3,0,0,0,0,0,n,m,n,0,0,0,0,0,d1],
        [13,0,0,0,0,0,0,o,0,0,0,0,0,0,11],
        [13,0,0,0,0,0,0,0,0,0,0,0,0,0,11],
        [13,0,0,0,0,0,0,0,0,0,0,0,0,0,11],
        [4,12,12,12,12,12,12,d2,12,12,12,12,12,12,3]
    ]

    
    
    room = Room(baseMap,player)

    maze[cords[1]].pop(cords[0])

    maze[cords[1]].insert(cords[0],room)

    

    
    if d1 == 70 and not forcedD1:
        if (cords[0] + 1) != 3:
            generateRoom(maze,player,[cords[0]+1,cords[1]],[False,False,True,False])

    if d2 == 71 and not forcedD2:
        if (cords[1] - 1) != -1:
            generateRoom(maze,player,[cords[0],cords[1]-1],[False,False,False,True])

    if d3 == 72 and not forcedD3:
        if (cords[0] - 1) != -1:
            generateRoom(maze,player,[cords[0]-1,cords[1]],[True,False,False,False])

    if d4 == 73 and not forcedD4:
        if (cords[1] + 1) != 3:
            generateRoom(maze,player,[cords[0],cords[1]+1],[False,True,False,False])




class MyGameWindow(arcade.Window):
    def __init__(self, width, height, title, fullscreen=True):
        super().__init__(width,height,title,fullscreen)
        arcade.set_background_color(arcade.color.BLACK)

    
    def setup(self):
        self.animaitonState = 0
        self.player = Player([100,100],500,0.5,20,100)
        
        self.flyingEnemy = FlyingEnemy([0,0],120,2)
        
        self.set_vsync(False)
        
        self.enemiesAlive = False

        self.maze = generateMaze(self.player)

    
    def on_draw(self):
        if self.animaitonState == 2:
            self.animaitonState = 0
        self.animaitonState += 1
        
        arcade.start_render()
        self.room.tileSpriteList.draw()
        if self.player.alive:
            self.player.spriteList.draw()
            self.player.shotSpriteList.draw()

        for enemy in self.room.enemyList:
            enemy.spriteShotList.draw()
       
       
        self.flyingEnemy.spriteList[self.flyingEnemy.animationPlayer.currentPicture-1].draw()
        

    def update(self, delta_time):

        self.flyingEnemy.spriteList.update()

        self.room = self.maze[self.player.worldCord[1]][self.player.worldCord[0]]
        
        self.flyingEnemy.moveEnemyToPlayer(self.player)
        for i in range(len(self.flyingEnemy.spriteList)):
            self.flyingEnemy.spriteList[i].set_position(self.flyingEnemy.position[0],self.flyingEnemy.position[1])

        if len(self.room.enemyList) > 0:
            self.enemiesAlive = True
        
        else:
            self.enemiesAlive = False
            

        self.player.lastPosition[0] = self.player.position[0]
        self.player.lastPosition[1] = self.player.position[1]
        self.player.position[0] += self.player.directionX * self.player.movementSpeed * delta_time
        self.player.position[1] += self.player.directionY * self.player.movementSpeed * delta_time
        self.player.checkKeyStrokes()
        self.player.sprite.set_position(self.player.position[0],self.player.position[1])
        self.player.spriteList.update()
        self.room.tileSpriteList.update()
        self.flyingEnemy.spriteList.update()

        if self.player.position[0] > 1920 - 155:
            self.player.position[0] = 1920 - 155

        elif self.player.position[0] < 0 + 155:
            self.player.position[0] = 0 + 155

        if self.player.position[1] < 0 + 155:
            self.player.position[1] = 0 + 155
        
        elif self.player.position[1] > 1080 - 155:
            self.player.position[1] = 1080 - 155


        for shot in self.player.shotList:
            shot.updateShot(delta_time)
            shot.sprite.set_position(shot.X,shot.Y)

            if shot.X > 2000 or shot.X < -100 :
                self.player.shotList.remove(shot)
                self.player.shotSpriteList.remove(shot.sprite)
                
            if shot.Y > 1100 or shot.Y < -100:
                self.player.shotList.remove(shot)
                self.player.shotSpriteList.remove(shot.sprite)

        for shot in self.player.shotList:
            hit = False
            
            for enemy in self.room.enemyList:
                shot.checkIfHit(enemy)
                if shot.col:
                    enemy.health -= self.player.shotDamage
                    hit = True

                    if enemy.health < 0:
                        enemy.alive = False
                
                if not enemy.alive:
                    self.room.enemyList.remove(enemy)
                    self.room.tileSpriteList.remove(enemy.sprite)
                    tile = Tile(enemy.position)
                    self.room.tileSpriteList.append(tile.sprite)
            
            if hit:
                self.player.shotList.remove(shot)
                self.player.shotSpriteList.remove(shot.sprite)
            

        for enemy in self.room.enemyList:
            enemy.hitPossible()


        for enemy in self.room.enemyList:

            col = checkCollision(enemy.position,self.player.position,enemy.size +10,self.player.size)
            if col:
                self.player.health -= enemy.damage

            for shot in enemy.shotList:

                shot.updateShot(delta_time)
                shot.sprite.set_position(shot.X,shot.Y)
                shot.checkIfHit(self.player)
                
                if shot.col:
                    enemy.shotList.remove(shot)
                    enemy.spriteShotList.remove(shot.sprite)

                    self.player.health -= shot.damage

        
                if shot.X > 2000 or shot.X < -100 :
                    enemy.shotList.remove(shot)
                    enemy.spriteShotList.remove(shot.sprite)
                
                if shot.Y > 1100 or shot.Y < -100:
                    enemy.shotList.remove(shot)
                    enemy.spriteShotList.remove(shot.sprite)
            
            
        if self.enemiesAlive == False:
            for door in self.room.doors:
                door.checkTransision(self.player)
        
        if self.player.health < 0:
            self.player.alive = False
            arcade.close_window()
        
        
        for tile in self.room.collisionList:
            collision = checkCollision(tile.position,self.player.position,tile.size,self.player.size)
            if collision == True:
                self.player.position[0] = self.player.lastPosition[0]
                self.player.position[1] = self.player.lastPosition[1]


        if keyboard.is_pressed("f"):
            print(1/delta_time)
        

    def on_key_press(self, key, modifiers):
        
        if keyboard.is_pressed("d"):
            self.player.directionX = 1
        
        if keyboard.is_pressed("a"):
            self.player.directionX = -1
        
        if keyboard.is_pressed("s"):
            self.player.directionY = -1
        
        if keyboard.is_pressed("w"):
            self.player.directionY = 1
        
        if keyboard.is_pressed("esc"):
            arcade.close_window()
    
    def on_key_release(self, key, modifiers):
        
        if not keyboard.is_pressed("d") and not keyboard.is_pressed("a"):
            self.player.directionX = 0
        
        if not keyboard.is_pressed("w") and not keyboard.is_pressed("s"):
            self.player.directionY = 0


game = MyGameWindow(1920,1080, "bruh",False)
game.setup()
arcade.run()
