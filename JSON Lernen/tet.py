import json
import os

dateiname = "Unterschriften.json"

# Falls die Datei existiert → laden
if os.path.exists(dateiname):
    with open(dateiname, "r", encoding="utf-8") as f:
        daten = json.load(f)
else:
    daten = {
        "Unterschriften": []
    }

if input("Unterschreiben? (j/n) ") == "j":
    name = input("Geben Sie Ihren Namen ein: ")

    if input("Möchten Sie unterschreiben? (j/n) ") == "j":
        daten["Unterschriften"].append(name)

        with open(dateiname, "w", encoding="utf-8") as f:
            json.dump(daten, f, indent=4)

        print("Unterschrift gespeichert!")
else:
    print("Ok, dann nicht.")
