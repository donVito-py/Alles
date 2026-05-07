"""
Arcade 3.3.3 TileMap Scaffold
Minimalistische Struktur für TileMap-Projekte.
"""

import arcade

# ============================================================================
# KONSTANTEN
# ============================================================================

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "TileMap Scaffold"
FPS = 60

TILE_SCALING = 1.0
MAP_FILE_PATH = "Platfomer.tmx"  # Deine Tiled-JSON-Datei


# ============================================================================
# GAME CLASS
# ============================================================================

class GameWindow(arcade.Window):
    """Haupt-Game-Fenster mit TileMap-Support."""

    def __init__(self):
        """Initialisiere das Fenster."""
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # === TILEMAP ===
        self.tile_map: arcade.TileMap | None = None
        self.scene: arcade.Scene | None = None

        # === PHYSIK ===
        self.physics_engine: arcade.PhysicsEnginePlatformer | None = None

        # === PLAYER ===
        self.player_sprite: arcade.Sprite | None = None

        # === KAMERA ===
        self.camera = arcade.camera.Camera2D()

        # Hintergrundfarbe
        self.bg_color = arcade.color.BLACK

    def setup(self) -> None:
        """Initialisiere das Spiel."""
        # === MAP LADEN ===
        layer_options = {
            # Layer-Namen hier anpassen an deine .json-Datei
            # "Platforms": {"use_spatial_hash": True}
        }

        try:
            self.tile_map = arcade.load_tilemap(
                "Platfomer.tmx",
                scaling=TILE_SCALING,
                layer_options=layer_options,
                use_spatial_hash=False,
            )
        except FileNotFoundError:
            print(f"⚠️  Map nicht gefunden: {MAP_FILE_PATH}")
            print("   Erstelle minimal-test-scene...")
            self.scene = arcade.Scene()
            return

        # Scene aus der Map erstellen
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        # === PLAYER SPRITE (placeholder) ===
        # Ersetze das durch dein Asset
        self.player_sprite = arcade.load_animated_gif("FreeKnight_v1/11/__Idle.gif")
        

        # Player zur Scene hinzufügen (oder neue Layer erstellen)
        if "Player" not in self.scene:
            self.scene.add_sprite_list("Player")
        self.scene.add_sprite("Player", self.player_sprite)

        # === PHYSICS ENGINE ===
        # Anpassen an deine Layer-Namen!
        walls_layer = None
        if self.scene and "Platforms" in self.scene:
            walls_layer = self.scene["Platforms"]

        if walls_layer:
            self.physics_engine = arcade.PhysicsEnginePlatformer(
                self.player_sprite,
                walls=walls_layer,
                gravity_constant=0.5,
            )
        else:
            # Fallback wenn keine Walls-Layer
            self.physics_engine = arcade.PhysicsEnginePlatformer(
                self.player_sprite,
                gravity_constant=0.5,
            )

    def on_draw(self) -> None:
        """Render-Loop."""
        self.camera.use()
        self.clear()

        if self.scene:
            self.scene.draw()



    def on_update(self, delta_time: float) -> None:
        """Update-Loop."""
        if not self.physics_engine or not self.player_sprite:
            return

        # Physics updaten
        self.physics_engine.update()

        # Kamera folgt dem Player
        self.camera.center_x = self.player_sprite.center_x
        self.camera.center_y = self.player_sprite.center_y

    def on_key_press(self, key: int, modifiers: int) -> None:
        """Tastatureingaben."""
        if key == arcade.key.LEFT:
            self.player_sprite.velocity_x = -200
        elif key == arcade.key.RIGHT:
            self.player_sprite.velocity_x = 200
        elif key == arcade.key.SPACE:
            self.player_sprite.velocity_y = 600

    def on_key_release(self, key: int, modifiers: int) -> None:
        """Taste losgelassen."""
        if key in (arcade.key.LEFT, arcade.key.RIGHT):
            self.player_sprite.velocity_x = 0


# ============================================================================
# MAIN
# ============================================================================

def main() -> None:
    """Starte das Spiel."""
    app = GameWindow()
    app.setup()
    app.run()


if __name__ == "__main__":
    main()