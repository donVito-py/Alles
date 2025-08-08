import arcade

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Flappy Bird"
GRAVITY = 0.5
JUMP_STRENGTH = 10
PLAYER_SCALE = 0.05

class Spiel(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.BUD_GREEN)

        self.player = arcade.Sprite("FlappyBIRD.png", PLAYER_SCALE)
        self.player.center_x = 100
        self.player.center_y = SCREEN_HEIGHT // 2
        self.player.change_y = 0

        self.setup()

    def setup(self):
        try:
            self.tile_map = arcade.load_tilemap("Flappy Bird .tmx", scaling=2)
            self.szene = arcade.Scene.from_tilemap(self.tile_map)
        except FileNotFoundError:
            print("⚠️ Tilemap nicht gefunden. Szene wird übersprungen.")
            self.szene = arcade.Scene()
        
        self.szene.add_sprite("Player", self.player)

    def on_key_press(self, key, modifiers):
        if key in (arcade.key.W, arcade.key.SPACE):
            self.player.change_y = JUMP_STRENGTH

    def on_draw(self):
        self.clear()
        self.szene.draw(pixelated=True)
        self.player.draw()

    def on_update(self, delta_time):
        # Gravitation anwenden
        self.player.change_y -= GRAVITY
        self.player.center_y += self.player.change_y

        # Optional: Begrenzung nach unten
        if self.player.center_y < 30:
            self.player.center_y = 30
            self.player.change_y = 0

def main():
    fenster = Spiel()
    arcade.run()

if __name__ == "__main__":
    main()
