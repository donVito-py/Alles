import arcade
import arcade.camera
import socket
class game(arcade.Window):
    def __init__(self):
        super().__init__(800, 800, "game")
        self.layer_options = {
            "hindernis": {
                "use_spatial_hash": True
            }
        }
        
        self.tile_map = arcade.load_tilemap("map.tmx",scaling=1, layer_options=self.layer_options)
        self.scene = arcade.Scene().from_tilemap(self.tile_map)
        self.spieler = arcade.Sprite("spieler2.png", 0.9)
        self.spieler.center_x = 16
        self.spieler.center_y = 48
        self.scene.add_sprite("spieler2", self.spieler)
        self.camera = arcade.camera.Camera2D()
        self.server_position = (48, 48)  # Initialisiere die Serverposition von Spieler 2
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.settimeout(0.1)  # Setze einen kurzen Timeout, damit das Spiel nicht einfriert
        self.spieler2 = arcade.Sprite("spieler.png", 0.9)
       # self.spieler2_s_position = (48, 48)  # Initialisiere die Serverposition von Spieler 2
        self.scene.add_sprite("spieler", self.spieler2)
        self.spieler2_position = (200, 200)  # Initialisiere die Position des zweiten Spielers
        self.spieler2.center_x = 200
        self.spieler2.center_y = 200
        server_ip = "192.168.178.131"
        server_port = 8000
        self.client.connect((server_ip, server_port))
        print(self.client.recv(1024).decode('utf-8'))  # Empfang der Begrüßungsnachricht vom Server
        # Sende den Spielernamen an den Server (z.B. "Spieler1")
        self.client.send("Spieler1".encode('utf-8'))
        print("Verbunden mit Server:", server_ip, "Port:", server_port)
        self.physics = arcade.PhysicsEngineSimple(self.spieler, self.scene["hindernis"])

    def on_draw(self):

        self.clear()
        self.camera.use()  # Kamera zuerst setzen
        self.scene.draw()
    def on_update(self, delta_time):
        
        

        self.scene.update(delta_time)
        self.spieler.update()
        self.spieler2.update()
        self.physics.update()
        
        # Spielfeldgröße bestimmen (hier als Beispiel 2000x2000, passe ggf. an)
        map_width = self.tile_map.width * self.tile_map.tile_width
        map_height = self.tile_map.height * self.tile_map.tile_height

        # Kamera folgt dem Spieler, bleibt aber im Fenster
        cam_x = max(self.width // 2, min(self.spieler.center_x, map_width - self.width // 2))
        cam_y = max(self.height // 2, min(self.spieler.center_y, map_height - self.height // 2))
        self.camera.position = (cam_x, cam_y)
        try:
            # Position als "x,y" senden
            pos_str = f"{self.spieler.center_x},{self.spieler.center_y}"
            self.client.send(pos_str.encode("utf-8"))
        except Exception as e:
            print("Fehler beim Senden der Position:", e)

        try:
            data = self.client.recv(1024)
            pos_str = data.decode("utf-8")
            # Position als "x,y" empfangen und setzen
            if "," in pos_str:
                x_str, y_str = pos_str.split(",")
                self.spieler2_position = (float(x_str), float(y_str))
                print("Empfangene Position von Spieler 2:", self.spieler2_position)
            else:
                print("Ungültiges Format empfangen:", pos_str)
        except socket.timeout:
            # Keine Daten empfangen, ignoriere und mache weiter
            pass
        except Exception as e:
            print("Fehler beim Empfangen der Position:", e)
        # Setze die Position des zweiten Spielers
        #print(self.spieler2_s_position)  # Sende die Position des Spielers an den Server

        # print(self.spieler.position)
        # print(self.camera.position)
        






    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.W or symbol == arcade.key.UP:
            self.spieler.change_y = 1
        elif symbol == arcade.key.S or symbol == arcade.key.DOWN:
            self.spieler.change_y = -1
        elif symbol == arcade.key.A or symbol == arcade.key.LEFT:
            self.spieler.change_x = -1
        elif symbol == arcade.key.D or symbol == arcade.key.RIGHT:
            self.spieler.change_x = 1
    def on_key_release(self, symbol, modifiers):
        if symbol == arcade.key.W or symbol == arcade.key.UP:
            self.spieler.change_y = 0
        elif symbol == arcade.key.S or symbol == arcade.key.DOWN:
            self.spieler.change_y = 0
        elif symbol == arcade.key.A or symbol == arcade.key.LEFT:
            self.spieler.change_x = 0
        elif symbol == arcade.key.D or symbol == arcade.key.RIGHT:
            self.spieler.change_x = 0

def main():
    game()
    arcade.run()
if __name__ == "__main__":
    main()


