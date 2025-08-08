import arcade
import arcade.gui
from arcade.gui import (
    UIAnchorLayout,
    UIFlatButton,
    UIGridLayout,
    UIImage,
    UIOnChangeEvent,
    UITextureButton,
    UITextureToggle,
    UIView,
)



SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Glitch Klicker"

class MeinSpiel(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.x = int(input("Hitboxen anzeigen? (1 für Ja, 0 für Nein): "))
        self.mauszeiger = None
        self.manager = arcade.gui.UIManager()

        self.store_button = UITextureButton(
            text="Store",
            width=200,
            texture=arcade.load_texture(":resources:gui_basic_assets/button/red_normal.png"),
            texture_hovered=arcade.load_texture(":resources:gui_basic_assets/button/red_hover.png"),
            texture_pressed=arcade.load_texture(":resources:gui_basic_assets/button/red_press.png")
        )
        
        self.store_button.center_x = SCREEN_WIDTH // 2
        self.store_button.center_y = 100
        self.store_button.add(
            child=UIImage(
                texture= arcade.load_texture("Store.png"),
                width=25,
                height=25,
            ),
            anchor_x="left",
            align_x=10,
        )
        def on_change(event: UIOnChangeEvent):
            self.store_button.disabled = event.new_value

        self.manager.add(self.store_button)
        self.manager.enable()

        arcade.set_background_color(arcade.color.WHITE)
        self.affe =arcade.Sprite("Background.png", 0.75)
        self.affe.center_x = SCREEN_WIDTH // 2
        self.affe.center_y = SCREEN_HEIGHT // 2
        self.zahl = 0
        self.affe.hit_box = arcade.hitbox.HitBox([(75, 75), (-75, 75), (-75, -75), (75, -75)], self.affe.position)

    def setup(self):
        pass

    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE:
            self.zahl = self.zahl + 1   
        if key == arcade.key.ESCAPE:
            arcade.close_window()
        if key == arcade.key.Q:
            self.zahl = self.zahl + self.zahl 
   
    def on_draw(self):
        self.clear()
        arcade.draw_sprite(self.affe)
        arcade.draw_text(f"Abgebaute Glitches: {self.zahl}", 5,5, arcade.color.BLACK, 20 )
        if self.x == 1:
            self.affe.draw_hit_box(color=arcade.color.RED, line_thickness=2)
            if self.mauszeiger != None:
                self.mauszeiger.draw_hit_box(color=arcade.color.BLUE, line_thickness=2)
        else:
            pass
        self.manager.draw()
        arcade.draw_lbwh_rectangle_filled(75, 75, 675, 675, arcade.color.GRAY)
        
    def on_mouse_press(self, x, y, button, modifiers):
        self.mauszeiger = arcade.Sprite()
        self.mauszeiger.center_x = x
        self.mauszeiger.center_y = y
        self.mauszeiger.hit_box = arcade.hitbox.HitBox([(5, 5), (-5, 5), (-5, -5), (5, -5)], self.mauszeiger.position)
        if arcade.check_for_collision(self.affe, self.mauszeiger):
            self.zahl = self.zahl + 1

    def on_update(self, delta_time):
        print(f"Anzahl Klicks: {self.zahl}")
                        

if __name__ == "__main__":
    spiel = MeinSpiel()
    spiel.setup()
    arcade.run()