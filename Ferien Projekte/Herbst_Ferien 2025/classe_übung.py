class VideoSpiele:
    def __init__(self, titel, genre, plattform, bewertung: float):
        self.titel = titel
        self.genre = genre
        self.plattform = plattform
        self.bewertung = bewertung  # Bewertung von 0.0 bis 10.0

    def __repr__(self):  # string-repräsentation
        return f"VideoSpiel(Titel: {self.titel}, Genre: {self.genre}, Plattform: {self.plattform}, Bewertung: {self.bewertung})"

    def spiele_info(self):
        print(f"{self.titel} ist ein {self.genre}-Spiel für {self.plattform} mit einer Bewertung von {self.bewertung}/10.")

# Instanziierung von Objekten
spiel1 = VideoSpiele("The Legend of Zelda: Breath of the Wild", "Action-Adventure", "Nintendo Switch", 9.5)
spiel2 = VideoSpiele("Subnautica", "Action, Survivel", "Steam", 10.0)
spiel1.spiele_info()
spiel2.spiele_info()
print(spiel1)
print(spiel2)