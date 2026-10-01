import arcade

class MeinSpiel(arcade.Window):
    def __init__(self):
        super().__init__(800, 600, "String zu Methode")
        
        # Der Name der Methode als String
        befehl_als_string = "aktioniere_powerup"
        
        # Ruft die Methode dynamisch auf
        self.fuehre_befehl_aus(befehl_als_string)

    def aktioniere_powerup(self):
        print("Power-Up wurde aktiviert!")

    def fuehre_befehl_aus(self, methoden_name):
        # getattr(objekt, name_als_string) holt die Methode
        if hasattr(self, methoden_name):
            methode = getattr(self, methoden_name)
            methode()  # Führt die Methode aus
        else:
            print(f"Methode {methoden_name} existiert nicht.")

# Spiel starten
window = MeinSpiel()
arcade.run()
