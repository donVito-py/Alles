import arcade

# ============================================================================
# KONSTANTEN
# ============================================================================

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "Platti"

TILE_SCALING = 1.0
MAP_FILE_PATH = "Platfomer.tmx"


# ============================================================================
# GAME CLASS
# ============================================================================

class GameWindow(arcade.Window):

    def __init__(self):
        """Initialisiere das Fenster."""
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        self.player_sprite_list = arcade.SpriteList()

        self.background_color = arcade.color.LIGHT_BLUE

        





        self.player_sprite = arcade.load_animated_gif("FreeKnight_v1/11/__Idle.gif")

        #self.player_sprite = arcade.Sprite("tower.png")
        self.player_sprite.center_x = 180
        self.player_sprite.center_y = 770
        self.player_sprite.scale = 1.5
        self.player_sprite_list.append(self.player_sprite)



    def setup(self):
        """Setze das Spiel auf."""
        self.tile_map = arcade.load_tilemap(MAP_FILE_PATH, TILE_SCALING)
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        self.simple_physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite, self.scene["Wall"], gravity_constant=0.5)
    
        # Setze die Kamera
        self.camera = arcade.camera.Camera2D()

    def on_key_press(self, key, modifiers):
        """Reagiere auf Tastendruck."""
        if key == arcade.key.ESCAPE:
            self.close()
        if key == arcade.key.RIGHT or key ==arcade.key.D:
            self.player_sprite.change_x = 5
        if key == arcade.key.LEFT or key==arcade.key.A:
            self.player_sprite.change_x = -5
        if key == arcade.key.UP or key == arcade.key.W:
            self.player_sprite.change_y = 5
        if key == arcade.key.DOWN or key == arcade.key.S:
            self.player_sprite.change_y = -5

    def on_key_release(self, key, modifiers):
        """Reagiere auf Loslassen einer Taste."""
        if key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 0
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = 0
        if key == arcade.key.UP or key == arcade.key.W:
            self.player_sprite.change_y = 0
        if key == arcade.key.DOWN or key == arcade.key.S:
            self.player_sprite.change_y = 0


    def on_update(self, delta_time):
        self.camera.position = self.player_sprite.position
        self.player_sprite_list.update()
        self.simple_physics_engine.update()
    def on_draw(self):
        """Zeichne das Spiel."""
        self.clear()
        self.camera.use()
        self.scene.draw(pixelated=True)
        self.player_sprite_list.draw(pixelated=True)

# ============================================================================
# MAIN
# ============================================================================

def main():
    """Starte das Spiel."""
    app = GameWindow()
    app.setup()
    arcade.run()


if __name__ == "__main__":
    main()