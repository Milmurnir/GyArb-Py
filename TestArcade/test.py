import arcade
import keyboard


movementSpeed = 100

class Tile:
    def __init__(self,position):
        self.position = position
        self.sprite = arcade.Sprite("Images\\base.png")


class MyGameWindow(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width,height,title)
        arcade.set_background_color(arcade.color.BLACK)


        
    
    def setup(self):
        self.playerPosition = [100,100]
        self.playerSprite = arcade.Sprite("Images\character.png",5,center_x=100,center_y=100)
        self.playerSpriteList = arcade.SpriteList()
        self.playerSpriteList.append(self.playerSprite)
        self.playerDirectionX = 0
        self.playerDirectionY = 0
        self.tileSpriteList = arcade.SpriteList()


        for y in range(9):
            yCord = y* 120
            for x in range(16):
                xCord = x * 120

                self.tilePosition = [xCord,yCord]
                tile = Tile(self.tilePosition)
                self.tileSpriteList.append(tile)



    def on_draw(self):
        arcade.start_render()
        arcade.draw_circle_filled(self.playerPosition[0],self.playerPosition[1],20,arcade.color.GREEN)
        self.playerSpriteList.draw()

        self.tileSpriteList.draw()
    

    def update(self, delta_time):
        self.playerPosition[0] += self.playerDirectionX * movementSpeed * delta_time
        self.playerPosition[1] += self.playerDirectionY * movementSpeed * delta_time



        self.playerSprite.set_position(self.playerPosition[0],self.playerPosition[1])

        self.playerSpriteList.update()


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

        




game = MyGameWindow(1280,720, "bruh")
game.setup()
arcade.run()