# Eine Funktion namens "eins", die die Zahl 1 ausgibt
def eins():
    return 1

# Eine Funktion namens "produckt", die das Produkt der beiden Zahlen 413 und 78 ausgibt
def produckt():
    return(413 * 78)

# Eine Funktion namens "zufallige_zahl", die eine zufällige Zahl zwischen -24 und 24 ausgibt
import random

def zufallige_zahl():
    return(random.randint(-24, 24))


# Eine Funktion namens "zufalsszahl_positiv", die eine zufällige  Zahl zwischen -24 und 48 ausgibt und True zurückgibt, wenn die Zahl positiv ist, und False, wenn die Zahl negativ ist.

def zufalsszahl_positiv():
    zahl = random.randint(-24, 48)
    if zahl > 0:
        return True
    else:
        return False
    
# Eine Funktion namens "größte", die 100 Zufallszahlen zwischen -240 und 240 generiert und die größte Zahl zurückgibt.

def größte():
    zahlen = [random.randint(-240, 240) for _ in range(100)]
    biggest = max(zahlen)
    return biggest