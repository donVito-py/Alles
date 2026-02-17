from flask import Flask, request, jsonify, send_from_directory
import json
import os

app = Flask(__name__)
dateiname = "Ich.json"

# JSON-Datei laden oder neu anlegen
if os.path.exists(dateiname):
    with open(dateiname, "r", encoding="utf-8") as f:
        daten = json.load(f)
else:
    daten = {"Unterschriften": []}

# Route zum Auslesen der Unterschriften
@app.route("/get")
def get_unterschriften():
    return jsonify(daten)

# Route zum Hinzufügen einer Unterschrift
@app.route("/add", methods=["POST"])
def add_unterschrift():
    global daten
    name = request.json.get("name")
    if name and name not in daten["Unterschriften"]:
        daten["Unterschriften"].append(name)
        with open(dateiname, "w", encoding="utf-8") as f:
            json.dump(daten, f, indent=4)
        return jsonify({"success": True, "name": name})
    return jsonify({"success": False})

# Route zum Ausliefern der HTML-Datei
@app.route("/")
def index():
    return send_from_directory('.', 'index.html')

if __name__ == "__main__":
    app.run(debug=True)
