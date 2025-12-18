import arcade

# Deine erste Sprite-Klasse
class Spieler(arcade.Sprite):
    def __init__(self, filename, scale):
        super().__init__(filename, scale)
        self.change_x = 0
        self.change_y = 0
        self.speed = 5

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y
        # Kollisionsprüfung etc. hier
        
# Deine zweite Sprite-Klasse (z.B. Gegner)
class Gegner(arcade.Sprite):
    def __init__(self, filename, scale):
        super().__init__(filename, scale)
        self.change_x = 0
        self.change_y = 0
        self.speed = 2

    def update(self):
        self.center_x += self.change_x
        # Einfache Gegner-Logik
        if self.center_x < 0:
            self.change_x *= -1 # Richtung wechseln
        elif self.center_x > 800: # Beispiel Fensterbreite
            self.change_x *= -1

class HauptAnsicht(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.AMAZON)
        
        # Listen für die verschiedenen Sprite-Typen
        self.spieler_liste = arcade.SpriteList()
        self.gegner_liste = arcade.SpriteList()

        # Sprites erstellen und hinzufügen
        self.spieler = Spieler("spieler.png", 0.5) # Pfad anpassen!
        self.spieler.center_x = 100
        self.spieler.center_y = 250
        self.spieler_liste.append(self.spieler)

        self.gegner1 = Gegner("gegner.png", 0.5) # Pfad anpassen!
        self.gegner1.center_x = 400
        self.gegner1.center_y = 250
        self.gegner_liste.append(self.gegner1)
        
        self.gegner2 = Gegner("gegner.png", 0.5)
        self.gegner2.center_x = 600
        self.gegner2.center_y = 150
        self.gegner_liste.append(self.gegner2)

    def on_draw(self):
        self.clear()
        self.spieler_liste.draw() # Zeichnet alle Spieler-Sprites
        self.gegner_liste.draw()  # Zeichnet alle Gegner-Sprites

    def on_update(self, delta_time):
        self.spieler_liste.update() # Aktualisiert Spieler-Logik
        self.gegner_liste.update()  # Aktualisiert Gegner-Logik
        # Kollisionen zwischen den Listen hier prüfen, z.B.:
        # player_hits = arcade.check_for_collision_with_list(self.spieler, self.
