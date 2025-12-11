import random
import datetime
#objektorientiertese Programmierung in Python
class Adresse:
    def __init__(self, straße,hausnummer, stadt, postleitzahl: int, land, bundelesland):
        if type(hausnummer) != int:
            raise ValueError("Hausnummer und Postleitzahl müssen positive ganze Zahlen sein.")
        self.hausnummer = hausnummer
        self.straße = straße
        self.stadt = stadt
        self.postleitzahl = postleitzahl
        self.land = land
        self.bundelesland = bundelesland

    def __repr__(self):
        return f"Adresse(Straße: {self.straße}, hausnummer:{self.hausnummer}, Stadt: {self.stadt}, PLZ: {self.postleitzahl}, Land: {self.land}, Bundesland: {self.bundelesland})"
    
class Person:
    def __init__(self, name, alter, adresse):  # kontruktor (initialisien)
        self.name = name
        self.alter = alter
        self.adresse = adresse


    def __repr__(self):  # string-repräsentation
        return f"Person(Name: {self.name}, Alter: {self.alter})"
    
    def vorstellung(self):
        print( f"Hallo, ich heiße {self.name} und bin {self.alter} Jahre alt.")

    def feieren_geburtstag(self):
        self.alter += 1
        print(f"Herzlichen Glückwunsch zum {self.alter}. Geburtstag, {self.name}!")

    def todestag(self):
        self.alter == self.alter 
        print(f"{self.name} ist im Alter von {self.alter} gestorben.")

    
    



# Instanziierung von Objekten  
a = Adresse("Wendl-Dietrich-Platz", 11 , "München", 80992, "Deutschland", "Bayern") 
Franz = Person("Franz", 28, a)
Josef = Person("Josef", 12, a)
random_zahl_Franz = random.randint(1, 5)
if random_zahl_Franz == 5:
    Franz.todestag()
random_zahl_Josef = random.randint(1, 5)
if random_zahl_Josef == 5:
    Josef.todestag()

Franz.vorstellung()
Josef.vorstellung()