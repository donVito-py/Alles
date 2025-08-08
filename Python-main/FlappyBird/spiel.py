import arcade


PLAYER_MOVEMENT_SPEED= 10
class Spiel(arcade.Window):
    def __init__(self):
        super().__init__(800, 800, "Flappy Bird")
        arcade.set_background_color(arcade.color.BUD_GREEN)

        self.player = arcade.Sprite("FlappyBIRD.png", 0.05)
        self.player.center_x= 20
        self.player.center_y=400
        
        self.setup()
        


    def setup(self):
#        self.physice_engine = arcade.PhysicsEnginePlatformer(self.player)
        self.tile_map = arcade.load_tilemap(
           "Flappy Bird .tmx",
           scaling=2)
        self.szene = arcade.Scene.from_tilemap(self.tile_map)


    def on_key_press(self, key, modifiers):
        if key == arcade.key.W or arcade.key.SPACE:
            self.player.change_y = 10


    def on_draw(self):
        self.clear()
        self.szene.draw(pixelated = True)
        arcade.draw_sprite(self.player)

    
    def on_update(self, delta_time):
        self.player.update()

def main():
    fenster = Spiel()
    arcade.run()

if __name__ == "__main__":
    main()