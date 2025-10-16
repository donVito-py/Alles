import arcade
import arcade.gui
from arcade.gui import (
    UIImage,
    UIOnChangeEvent,
    UITextureButton,
    UIGridLayout,
    UIAnchorLayout,
    UIView,
)
from time import sleep
import math


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
        self.mauszeiger_helfer_liste = arcade.SpriteList()
        self.nummer_mauszeiger_helfer = 0

        

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


        #Mauszeiger_helfer
        self.mauszeiger_helfer = arcade.Sprite("Mauszeiger.png", 0.09)
        self.mauszeiger_helfer.center_x = SCREEN_WIDTH // 3
        self.mauszeiger_helfer.center_y = SCREEN_HEIGHT // 3 
        self.nummer_mauszeiger_helfer += 1
        dx = (SCREEN_WIDTH // 2) - self.mauszeiger_helfer.center_x
        dy = (SCREEN_HEIGHT // 2) - self.mauszeiger_helfer.center_y
        winkel_rad = math.atan2(dy, dx)
        winkel_deg = math.degrees(winkel_rad)
        self.mauszeiger_helfer.angle = winkel_deg
        self.mauszeiger_helfer_liste.append(self.mauszeiger_helfer)

        self.mauszeiger_helfer = arcade.Sprite("Mauszeiger.png", 0.09)
        self.mauszeiger_helfer.center_x = SCREEN_WIDTH // 3 + 200
        self.mauszeiger_helfer.center_y = SCREEN_HEIGHT // 3 - 67
        self.nummer_mauszeiger_helfer += 1
        dx = (SCREEN_WIDTH // 2) - self.mauszeiger_helfer.center_x
        dy = (SCREEN_HEIGHT // 2) - self.mauszeiger_helfer.center_y
        winkel_rad = math.atan2(dy, dx)
        winkel_deg = math.degrees(winkel_rad)
        self.mauszeiger_helfer.angle = winkel_deg
        self.mauszeiger_helfer_liste.append(self.mauszeiger_helfer)





        

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
            if self.on_store == True:
                self.zahl += 0
            else:
                self.zahl += 1 
        if key == arcade.key.ESCAPE:
            arcade.close_window()
        if key == arcade.key.Q:
            for i in range(1000):
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
        if self.on_store == True:
            arcade.draw_lbwh_rectangle_filled(75, 75, 675, 675, arcade.color.GRAY)
        self.manager.draw()
        self.mauszeiger_helfer_liste.draw()
        
    def on_mouse_press(self, x, y, button, modifiers):
        self.mauszeiger = arcade.Sprite()
        self.mauszeiger.center_x = x
        self.mauszeiger.center_y = y
        self.mauszeiger.hit_box = arcade.hitbox.HitBox([(5, 5), (-5, 5), (-5, -5), (5, -5)], self.mauszeiger.position)
        if arcade.check_for_collision(self.clicker, self.mauszeiger):
            if self.on_store == True:
                self.zahl = self.zahl + 0
            else:
                self.zahl = self.zahl + 1

    def on_update(self, delta_time):
        pass




if __name__ == "__main__":
    spiel = MeinSpiel()
    spiel.setup()
    arcade.run()