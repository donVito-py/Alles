import arcade


BREITE = 800
HOEHE = 600
TITEL = "Platformer"


class Spiel(arcade.Window):
    def __init__(self):
        super().__init__(BREITE, HOEHE, TITEL)
        arcade.set_background_color(arcade.color.SKY_BLUE)
        self.player_list = arcade.SpriteList()





        self.player_sprite = arcade.Sprite("tower.png", 0.0625, hit_box_algorithm=arcade.hitbox.algo_detailed)
        self.player_sprite.center_x = 180
        self.player_sprite.center_y = 2650
        self.player_list.append(self.player_sprite)

    def setup(self):
        self.tile_map = arcade.load_tilemap("Platfomer.tmx")
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite, gravity_constant=0.5, walls=self.scene["Wall"])

        self.camera = arcade.camera.Camera2D()
        self.camera_x = self.player_sprite.center_x
        self.camera_y = self.player_sprite.center_y
        self.camera.position = (self.camera_x, self.camera_y)





    def on_draw(self):
        self.clear()
        self.player_list.draw()
        self.camera.use()
        self.scene.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.W or key == arcade.key.UP:
            self.player_sprite.change_y = 5
        elif key == arcade.key.S or key == arcade.key.DOWN:
            self.player_sprite.change_y = -5
        elif key == arcade.key.A or key == arcade.key.LEFT:
            self.player_sprite.change_x = -5
        elif key == arcade.key.D or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 5

    def on_key_release(self, key, modifiers):
        if key == arcade.key.W or key == arcade.key.UP:
            self.player_sprite.change_y = 0
        elif key == arcade.key.S or key == arcade.key.DOWN:
            self.player_sprite.change_y = 0
        elif key == arcade.key.A or key == arcade.key.LEFT:
            self.player_sprite.change_x = 0
        elif key == arcade.key.D or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0


    def on_update(self, delta_time):
        self.player_list.update()
        self.camera_x = self.player_sprite.center_x
        self.camera_y = self.player_sprite.center_y
        self.camera.position = (self.camera_x, self.camera_y)
        self.physics_engine.update()








def main():
    app = Spiel()
    app.setup()
    arcade.run()


if __name__ == "__main__":
	main()
