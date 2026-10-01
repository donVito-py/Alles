import arcade

BREITE = 800
HOEHE = 600
PLAYER_SCALE = 0.0625
TITEL = "Platformer"


class Spiel(arcade.Window):
    def __init__(self):
        super().__init__(BREITE, HOEHE, TITEL)
        arcade.set_background_color(arcade.color.SKY_BLUE)
        self.player_list = arcade.SpriteList()


        Textur = arcade.load_texture("tower.png", hit_box_algorithm=arcade.hitbox.algo_detailed)
        
        self.player_sprite = arcade.Sprite(Textur, scale=PLAYER_SCALE, )
        self.player_list.append(self.player_sprite)
        
        self.up = arcade.key.W
        self.down = arcade.key.S
        self.left = arcade.key.A
        self.right = arcade.key.D
        
        
        
                

    def setup(self):
        self.tile_map = arcade.load_tilemap("Platfomer.tmx")
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite, walls=[self.scene["Wall"], self.scene["Barrier"]], gravity_constant=0.25)

        self.camera = arcade.camera.Camera2D()
        self.camera_x = self.player_sprite.center_x
        self.camera_y = self.player_sprite.center_y
        self.camera.position = (self.camera_x, self.camera_y)
        
    


        
        self.player_sprite.center_x = 180
        self.player_sprite.center_y = 2650
        
    # def change_keybines(self, key, modifiers):
    #     self.up = input("Enter key for up: ")
    #     self.down = input("Enter key for down: ")
    #     self.left = input("Enter key for left: ")
    #     self.right = input("Enter key for right: ")
    #     if hasattr(arcade, self.up):
    #         self.up = getattr(arcade.key, self.up)
    #     if hasattr(arcade, self.down):
    #         self.down = getattr(arcade.key, self.down)
    #     if hasattr(arcade, self.left):
    #         self.left = getattr(arcade.key, self.left)
    #     if hasattr(arcade, self.right):
    #         self.right = getattr(arcade.key, self.right)
            
    #     return self.up, self.down, self.left, self.right

        
        


    def on_draw(self):
        self.clear()
        self.camera.use()
        self.scene.draw(pixelated=True)
        self.player_list.draw(pixelated=True)

        #self.scene["Wall"].draw_hit_boxes()
        #self.scene["Barrier"].draw_hit_boxes()
        #self.player_list.draw_hit_boxes()

    def on_key_press(self, key, modifiers):
        if key == self.up or key == arcade.key.UP or key == arcade.key.SPACE or self.physics_engine.can_jump():
            self.player_sprite.change_y = 12
        elif key == self.down or key == arcade.key.DOWN:
            self.player_sprite.change_y = -4
        elif key == self.left or key == arcade.key.LEFT:
            self.player_sprite.change_x = -4
        elif key == self.right or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 4

        elif key == arcade.key.R:
            self.setup()
            
        elif key == arcade.key.ESCAPE:
            arcade.close_window()
            
        # elif key == arcade.key.K:
        #     self.change_keybines(key, modifiers)

    def on_key_release(self, key, modifiers):
        if key == self.up or key == arcade.key.UP :
            self.player_sprite.change_y = 0
        elif key == self.down or key == arcade.key.DOWN:
            self.player_sprite.change_y = 0
        elif key == self.left or key == arcade.key.LEFT:
            self.player_sprite.change_x = 0
        elif key == self.right or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0
            
            


    def on_update(self, delta_time):
        self.player_list.update()
        self.camera_x = self.player_sprite.center_x
        self.camera_y = self.player_sprite.center_y
        self.camera.position = (self.camera_x, self.camera_y)
        self.physics_engine.update()
        
        if arcade.check_for_collision_with_list(self.player_sprite, self.scene["Death"]):
            self.setup()








def main():
    app = Spiel()
    app.setup()
    arcade.run()


if __name__ == "__main__":
	main()
