import arcade
import keyboard
import random
from classes import *




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

        [1,10,10,10,10,10,10,10,10,10,10,10,10,10,10,2],
        [13,0,0,0,0,0,0,0,0,0,0,0,0,0,0,11],
        [13,0,n,0,0,0,0,0,0,0,0,0,0,n,0,11],
        [13,0,m,o,0,0,p,r,r,p,0,0,o,m,0,11],
        [14,0,0,s,0,q,c,0,0,c,q,0,s,0,0,14],
        [13,0,m,o,0,0,p,r,r,p,0,0,o,m,0,11],
        [13,0,n,0,0,0,0,0,0,0,0,0,0,n,0,11],
        [13,0,0,0,0,0,0,0,0,0,0,0,0,0,0,11],
        [4,12,12,12,12,12,12,12,12,12,12,12,12,12,12,3]
    ]
    return baseMap


movementSpeed = 100
Map = generateMap()
roomList = []


class MyGameWindow(arcade.Window):
    def __init__(self, width, height, title, fullscreen=True):
        super().__init__(width,height,title,fullscreen)
        arcade.set_background_color(arcade.color.BLACK)


    def set_vsync(self,vsync):
        super().set_vsync(vsync)
    
    def setup(self):
        self.player = Player([100,100],150,0.5,20)
        self.room = Room(Map)
        roomList.append(self.room)

        
        
        
    def on_draw(self):
        arcade.start_render()
       
    
        self.room.tileSpriteList.draw()
        self.player.spriteList.draw()
        self.player.shotSpriteList.draw()

    def update(self, delta_time):

        self.room = roomList[self.player.roomNumber]
        
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
            shot.updateShot()
            shot.sprite.set_position(shot.X,shot.Y)
        
        for door in self.room.doors:
            door.checkTransision(self.player)
        
       

        
        for tile in self.room.collisionList:
            collision = checkCollision(tile.position,self.player.position,tile.size,self.player.size)
            if collision == True:
                self.player.position[0] = self.player.lastPosition[0]
                self.player.position[1] = self.player.lastPosition[1]

    
        if keyboard.is_pressed("g"):
            Map = generateMap()
            room = Room(Map)
            roomList.append(room)

        
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
    
    def on_key_release(self, key, modifiers):
        
        if not keyboard.is_pressed("d") and not keyboard.is_pressed("a"):
            self.player.directionX = 0
        
        if not keyboard.is_pressed("w") and not keyboard.is_pressed("s"):
            self.player.directionY = 0

        




game = MyGameWindow(1920,1080, "bruh",False)

game.setup()
arcade.run()