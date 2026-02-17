from flask import Flask, request, render_template, jsonify
import json
import os
from datetime import datetime

app = Flask(__name__)
dateiname = "clients.json"

# JSON-Datei laden oder neu anlegen
if os.path.exists(dateiname):
    with open(dateiname, "r", encoding="utf-8") as f:
        try:
            clients = json.load(f)
            if "visits" not in clients:
                clients["visits"] = []
        except json.JSONDecodeError:
            clients = {"visits": []}
else:
    clients = {"visits": []}


@app.route("/")
def home():
    ip = request.remote_addr
    zeit = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Prüfen, ob IP schon existiert
    if ip not in [v["ip"] for v in clients["visits"]]:
        clients["visits"].append({"ip": ip, "zeit": zeit})
    else:
        # Optional: Zeit aktualisieren, falls IP schon da ist
        for v in clients["visits"]:
            if v["ip"] == ip:
                v["zeit"] = zeit

    # JSON speichern
    with open(dateiname, "w", encoding="utf-8") as f:
        json.dump(clients, f, indent=4)

    return render_template("indexx.html", visits=clients["visits"])

@app.route("/clients")
def show_clients():
    return jsonify(clients)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
