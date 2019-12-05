import arcade
import keyboard
import time





resolution = [1920,1080]

SCREEN_TITLE = ""


class MyGame(arcade.Window):
    """
    Main application class.

    NOTE: Go ahead and delete the methods you don't need.
    If you do need a method, delete the 'pass' and replace it
    with your own code. Don't leave 'pass' in this program.
    """

    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        
        arcade.set_background_color(arcade.color.BLACK)

        # If you have sprite lists, you should create them here,
        # and set them to None

    def setup(self):
        self.playerPosition = [100,100]
        self.playerSprite = arcade.Sprite("Images\Enemy0.png",center_x=self.playerPosition[0],center_y=self.playerPosition[1])
        self.spriteList = arcade.SpriteList()

        self.spriteList.append(self.playerSprite)


        
        # Create your sprites and sprite lists here
        pass

    def on_draw(self):
        """
        Render the screen.
        """
        
        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        #lt = time.time()
        arcade.start_render()
        
        self.spriteList.draw()

        #elapsed = time.time() - lt
        #print(elapsed)
        # Call draw() on all your sprite lists below

    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """
        print(delta_time)



        pass

    

    def on_key_press(self, key, key_modifiers):
        """
        Called whenever the user lets off a previously pressed key.
        """
        print("hh")

        if keyboard.is_pressed("d"):
            self.playerSprite.change_x = 5

        pass

 

def main():
    """ Main method """
    game = MyGame(resolution[0], resolution[1], SCREEN_TITLE)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()


