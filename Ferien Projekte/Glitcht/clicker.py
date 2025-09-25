import arcade
import arcade.gui
from arcade.gui import (
    UIImage,
    UIOnChangeEvent,
    UITextur0000,,,,,,,,,0000
)


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Glitch Klicker"

class MeinSpiel(arcade.Window):

    def UITextureButton_on_click(self, event):
        self.on_store = not self.on_store

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.x = int(input("Hitboxen anzeigen? (1 für Ja, 0 für Nein): "))
        self.mauszeiger = None
        self.zahl = 0

        self.on_store = False

        

        arcade.set_background_color(arcade.color.WHITE)
        self.clicker =arcade.Sprite("Background.png", 0.75)
        self.clicker.center_x = SCREEN_WIDTH // 2
        self.clicker.center_y = SCREEN_HEIGHT // 2
        self.clicker.hit_box = arcade.hitbox.HitBox([(75, 75), (-75, 75), (-75, -75), (75, -75)], self.clicker.position)


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

        self.store_button.on_click = self.UITextureButton_on_click
       
     

        self.store_button.add(
            child=UIImage(
                texture= arcade.load_texture("Store.png"),
                width=25,
                height=25,
            ),
            anchor_x="left",
            align_x=10,


        )
        self.manager.add(self.store_button)
        self.manager.enable()
        
    
    def on_change(self, event: UIOnChangeEvent):
        self.store_button.disabled = event.new_value



        
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
        arcade.draw_sprite(self.clicker)
        arcade.draw_text(f"Abgebaute Glitches: {self.zahl}", 5,5, arcade.color.BLACK, 20 )
        if self.x == 1:
            self.clicker.draw_hit_box(color=arcade.color.RED, line_thickness=2)
            if self.mauszeiger != None:
                self.mauszeiger.draw_hit_box(color=arcade.color.BLUE, line_thickness=2)
        else:
            pass
        # Shop zuerst zeichnen, dann die UI-Elemente (Button)
        if self.on_store == True:
            arcade.draw_lbwh_rectangle_filled(75, 75, 675, 675, arcade.color.GRAY)
        self.manager.draw()
        
    def on_mouse_press(self, x, y, button, modifiers):
        self.mauszeiger = arcade.Sprite()
        self.mauszeiger.center_x = x
        self.mauszeiger.center_y = y
        self.mauszeiger.hit_box = arcade.hitbox.HitBox([(5, 5), (-5, 5), (-5, -5), (5, -5)], self.mauszeiger.position)
        if arcade.check_for_collision(self.clicker, self.mauszeiger):
            self.zahl = self.zahl + 1

    def on_update(self, delta_time):
        pass

if __name__ == "__main__":
    spiel = MeinSpiel()
    spiel.setup()
    arcade.run()