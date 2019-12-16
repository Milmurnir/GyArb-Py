import arcade
import keyboard
import random
from classes import *
import pyglet


def generateMaze(player):

    maze = [
        [0,0,0],
        [0,0,0],
        [0,0,0],
    ]
    
    xCord = random.randint(0,len(maze)-1)
    yCord = random.randint(0,len(maze)-1)

    player.worldCord[0] = xCord
    player.worldCord[1] = yCord

    maze[yCord].pop(xCord)

    Map = generateMap()

    room = Room(Map,player)

    maze[yCord].insert(xCord, room)

    if  room.doorExist[0] and xCord != 2:
        Map = generateMap()
        room = Room(Map,player)

        maze[yCord].pop(xCord)
        maze[yCord].insert(xCord, room)
    
    


    return maze


def generateMap():
    m = random.randint(28,29)
    n = random.randint(30,31)
    o = random.randint(32,33)
    p = random.randint(34,35)
    q = random.randint(36,37)
    r = random.randint(38,39)
    s = random.randint(40,41)
    c = random.randint(42,43)

    baseMap = [

        [1,10,10,10,10,10,10,14,10,10,10,10,10,10,2],
        [13,0,0,0,0,0,0,0,0,0,0,0,0,0,11],
        [13,0,n,0,0,0,0,0,0,0,0,0,n,0,11],
        [13,0,m,o,0,0,p,r,r,p,0,0,o,m,0,11],
        [14,0,0,s,0,q,c,0,c,q,0,s,0,0,14],
        [13,0,m,o,0,0,p,r,r,p,0,0,o,m,0,11],
        [13,0,n,0,0,0,0,0,0,0,0,0,n,0,11],
        [13,0,0,0,0,0,0,0,0,0,0,0,0,0,11],
        [4,12,12,12,12,12,14,12,12,12,12,12,12,12,3]
    ]
    return baseMap


movementSpeed = 100




class MyGameWindow(arcade.Window):
    def __init__(self, width, height, title, fullscreen=True):
        super().__init__(width,height,title,fullscreen)
        arcade.set_background_color(arcade.color.BLACK)

    
    def setup(self):
        self.player = Player([100,100],150,0.5,20,10)
        
        
        
        self.set_vsync(False)
        

        self.enemiesAlive = False


        self.maze = generateMaze(self.player)

    def on_draw(self):
        arcade.start_render()

        self.room.tileSpriteList.draw()
        if self.player.alive:
            self.player.spriteList.draw()
            self.player.shotSpriteList.draw()

        for enemy in self.room.enemyList:
            enemy.spriteShotList.draw()
       

    def update(self, delta_time):
        self.room = self.maze[self.player.worldCord[1]][self.player.worldCord[0]]
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


game = MyGameWindow(1920,1080, "bruh",True)
game.setup()
arcade.run()
