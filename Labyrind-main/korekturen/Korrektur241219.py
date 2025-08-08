#Eine for-Schleife , die 100-mal abwechselnd die Zahl 100 und eine Zuhfallszahl, zwischen -100 und 100 ist, ausibt
#Inssgesammt sollen also 100 Zahl ausgegeben werden-
import random

for i in range(50):
    print("100")
    print(random.randint(-100, 100))


#Eine for-Schleife, die alle Quadratzahlen von 9 bis 144

for i in range(3, 13):
    print(i * i)


#Eine for-Schleife, die alle Zweierpotenzen von 16 4096

for i in range(4, 13):
    print(2 ** i)