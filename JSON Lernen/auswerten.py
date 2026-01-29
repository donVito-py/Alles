import json
with open("Ich.json", "r", encoding="utf-8") as f:
    inhalt = json.load(f)
    print(inhalt)