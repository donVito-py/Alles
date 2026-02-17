import arcade
import math

class Enemy(arcade.Sprite):
    def __init__(self, bild: str, ):
        super().__init__(bild, scale=0.05)
        self.akktueller_pladpunkt = 0

PFAD= [
    (0,0),
    (0,1),
    (0,2),
    (1,2),
    (1,3),
    (1,4),
    (1,5),
    (2,5),
    (3,5),
    (4,6),
    (4,5),
    (4,5),
    (5,6),
    (6,6),
    (6,7),
    (6,8),
    (7,8),
    (8,8),
    (8,9),
    (9,9)
]

class Game(arcade.Window):
    def __init__(self):
        super().__init__(500, 500, "My TDG",antialiasing=True, update_rate=0.01)
        arcade.set_background_color(arcade.color.BRICK_RED)
        self.pfad = arcade.SpriteList()
        self.enemies = arcade.SpriteList()
        self.towers = arcade.SpriteList()
        for x_idx, y_idx in PFAD:
            pfad_element = arcade.Sprite("Brick Path_Tan.png", 0.05)
            pfad_element.center_x = 25+x_idx*50
            pfad_element.center_y = 25+y_idx*50
            self.pfad.append(pfad_element)

            self.anzahl = 0
            self.vergangendezeit = 0
            self.gegner_time  = 0
            self.countdown = 0.5
            self.stierbt_gleich = True

    def on_mouse_press(self, x, y, button, modifiers):
        for x_idx, y_idx in PFAD:
            if (x_idx, y_idx) == (x//50, y//50):
                return
        if self.anzahl >= 4:
            return
        tower = arcade.Sprite("tower.png", 0.05)
        tower.center_x = x // 50 * 50 + 25
        tower.center_y = y// 50 * 50 + 25
        self.towers.append(tower)
        self.anzahl +=1

    def on_update(self, delta_time):
        self.vergangendezeit += delta_time
        self.gegner_time += delta_time
        if self.vergangendezeit >= 2:
            self.vergangendezeit == 0
            gegner = Enemy("gegner.png")
            gegner.center_x = PFAD [0][0] * 50 +25
            gegner.center_y = PFAD [0][1] * 50 + 25
            self.enemies.append(gegner)

        if self.gegner_time >= 1:
            self.gegner_time  = 0
            for gegner in self.enemies:
                gegner.akktueller_pladpunkt += 1
                gegner.center_x = PFAD[gegner.akktueller_pladpunkt][0] * 50 + 25
                gegner.center_y = PFAD[gegner.akktueller_pladpunkt][1] * 50 + 25
        
        for tower in self.towers:
            for gegner in self.enemies:
                if gegner.countdown <= 0:
                    gegner.kill()
                x_diff= abs(tower.center_x - gegner.center_x)
                y_diff= abs(tower.center_y - gegner.center_y)
                distanz = math.sqrt((x_diff ** 2) + (y_diff ** 2))
                print(distanz)
                if distanz <= 100:
                    gegner.stiert_gleich== True
                    gegner.countdown -= delta_time
                    break
                
        

        

            


    def on_draw(self):
        self.clear()
        self.pfad.draw()
        self.enemies.draw()
        self.towers.draw()

        arcade.draw_text(
            text= str(self.anzahl) + "/4 Türme plaziert",
            x = 10, 
            y = 10,
            color=arcade.color.EARTH_YELLOW,
            font_size= 18
        )
        for tower in self.towers:
            for gegner in self.enemies:
                x_diff= abs(tower.center_x - gegner.center_x)
                y_diff= abs(tower.center_y - gegner.center_y)
                distanz = math.sqrt((x_diff ** 2) + (y_diff ** 2))
                print(distanz)
                if distanz <= 100 and gegner.stierbt_gleich == True:
                    arcade.draw_line(
                        tower.center_x,
                        tower.center_y,
                        gegner.center_x,
                        gegner.center_y,
                        arcade.color.RAJAH,
                        5

                    )

                    gegner.kill()
                    break

          

Game()
arcade.run()

