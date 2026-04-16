import arcade
from pathlib import Path

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "Arcade + Tiled Map"
TILE_SCALE = 1.0

LAYER_NAME_GROUND = "ground"
LAYER_NAME_OBSTACLES = "obstacles"
LAYER_NAME_DECORATIONS = "decorations"


class Game(arcade.Window):

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        self.tile_map = None
        self.scene = None

        self.player_sprite = None
        self.physics_engine = None

        self.camera = arcade.Camera2D()
        self.debug_mode = False

        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)

    def setup(self):

        self._load_tilemap()
        self._setup_player()
        self._setup_physics()

    def _load_tilemap(self):

        map_path = Path("assets/maps/map.tmx")

        self.tile_map = arcade.load_tilemap(
            "Platfomer.tmx",
            scaling=TILE_SCALE
        )

        self.scene = arcade.Scene.from_tilemap(self.tile_map)

    def _setup_player(self):

        self.player_sprite = arcade.load_animated_gif(
            "FreeKnight_v1/11/__Idle.gif"
        )
        self.player_sprite.center_x = 100
        self.player_sprite.center_y = 100

        self.scene.add_sprite("player", self.player_sprite)

    def _setup_physics(self):

        walls = None

      #  if LAYER_NAME_OBSTACLES in self.scene.name_mapping:
      #     walls = self.scene[LAYER_NAME_OBSTACLES]

        self.physics_engine = arcade.PhysicsEnginePlatformer(
            player_sprite=self.player_sprite,
            walls=walls,
            gravity_constant=0.5
        )

    def on_draw(self):

        self.clear()


        self.scene.draw()


    def on_update(self, delta_time):

        self.physics_engine.update()
        self._update_camera()

    def _update_camera(self):

        self.camera.position = arcade.Vec2(
            self.player_sprite.center_x - SCREEN_WIDTH / 2,
            self.player_sprite.center_y - SCREEN_HEIGHT / 2
        )

    def on_key_press(self, key, modifiers):

        if key in (arcade.key.A, arcade.key.LEFT):
            self.player_sprite.change_x = -10

        elif key in (arcade.key.D, arcade.key.RIGHT):
            self.player_sprite.change_x = 10

        elif key in (arcade.key.W, arcade.key.UP, arcade.key.SPACE):
            self.player_sprite.change_y = 5

    def on_key_release(self, key, modifiers):

        if key in (arcade.key.A, arcade.key.LEFT):
            if self.player_sprite.change_x < 0:
                self.player_sprite.change_x = 0

        elif key in (arcade.key.D, arcade.key.RIGHT):
            if self.player_sprite.change_x > 0:
                self.player_sprite.change_x = 0


def main():

    game = Game()
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()