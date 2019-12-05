import arcade
import keyboard
import random

def LoadImage(Name,size,position):
    sprite = arcade.Sprite("C:\Projects\GyArb-Py\TestArcade\Images"+"\\"+Name+".png")
    sprite.center_x += position[0]
    sprite.center_y += position[1]
    return sprite

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
        [13,0,0,0,0,0,0,0,0,0,0,0,0,0,0,11],
        [13,0,0,0,0,0,0,0,0,0,0,0,0,0,0,11],
        [14,0,0,0,0,0,0,0,0,0,0,0,0,0,0,14],
        [13,0,0,0,0,0,0,0,0,0,0,0,0,0,0,11],
        [13,0,0,0,0,0,0,0,0,0,0,0,0,0,0,11],
        [13,0,0,0,0,0,0,0,0,0,0,0,0,0,0,11],
        [4,12,12,12,12,12,12,12,12,12,12,12,12,12,12,3]
    ]
    return baseMap


movementSpeed = 100
Map = generateMap()


class Tile:
    def __init__(self,position):
        self.position = position
        self.sprite = None


class MyGameWindow(arcade.Window):
    def __init__(self, width, height, title, fullscreen=True):
        super().__init__(width,height,title,fullscreen)
        arcade.set_background_color(arcade.color.BLACK)


    def set_vsync(self,vsync):
        super().set_vsync(vsync)
    
    def setup(self):
        self.playerPosition = [100,100]
        self.playerSprite = arcade.Sprite("C:\Projects\GyArb-Py\TestArcade\Images\player.png",6,center_x=100,center_y=100)
        self.playerSpriteList = arcade.SpriteList()
        self.playerSpriteList.append(self.playerSprite)
        self.playerDirectionX = 0
        self.playerDirectionY = 0
        self.tileSpriteList = arcade.SpriteList()
        


        for y in range(9):
            yCord = y* 120 + 60
            for x in range(16):
                xCord = x * 120 + 60

                self.tilePosition = [xCord,yCord]
                tile = Tile(self.tilePosition)

                if Map[y][x] == 0:
                    tile.sprite = LoadImage("base",0,tile.position)
        
                elif Map[y][x] == 4:
                    tile.sprite = LoadImage("wallCornerLeftUp",0,tile.position)
                
                elif Map[y][x] == 12:
                    tile.sprite = LoadImage("wallUp",0,tile.position)
                
                elif Map[y][x] == 3:
                    tile.sprite = LoadImage("wallcornerrightup",0,tile.position)
                
                elif Map[y][x] == 11:
                    tile.sprite = LoadImage("wallright",0,tile.position)
                
                elif Map[y][x] == 2:
                    tile.sprite = LoadImage("wallcornerrightdown",0,tile.position)
                
                elif Map[y][x] == 10:
                    tile.sprite = LoadImage("walldown",0,tile.position)
                
                elif Map[y][x] == 1:
                    tile.sprite = LoadImage("wallcornerleftdown",0,tile.position)
                
                elif Map[y][x] == 13:
                    tile.sprite = LoadImage("wallleft",0,tile.position)
                
                else:
                    tile.sprite = LoadImage("base",0,tile.position)

                print(tile.position)
                self.tileSpriteList.append(tile.sprite)



    def on_draw(self):
        arcade.start_render()
        

        self.tileSpriteList.draw()
        self.playerSpriteList.draw()
    

    def update(self, delta_time):
        self.playerPosition[0] += self.playerDirectionX * movementSpeed * delta_time
        self.playerPosition[1] += self.playerDirectionY * movementSpeed * delta_time



        self.playerSprite.set_position(self.playerPosition[0],self.playerPosition[1])

        self.playerSpriteList.update()

        print(1/delta_time)

    def on_key_press(self, key, modifiers):
        
        if keyboard.is_pressed("d"):
            self.playerDirectionX = 1
        
        if keyboard.is_pressed("a"):
            self.playerDirectionX = -1
        
        if keyboard.is_pressed("s"):
            self.playerDirectionY = -1
        
        if keyboard.is_pressed("w"):
            self.playerDirectionY = 1
    
    def on_key_release(self, key, modifiers):
        
        if not keyboard.is_pressed("d") and not keyboard.is_pressed("a"):
            self.playerDirectionX = 0
        
        if not keyboard.is_pressed("w") and not keyboard.is_pressed("s"):
            self.playerDirectionY = 0

        




game = MyGameWindow(1920,1080, "bruh",)

game.setup()
arcade.run()