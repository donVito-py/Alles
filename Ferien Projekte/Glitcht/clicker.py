import arcade
import arcade.gui
import math
import json
import os
import random

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Glitch Klicker"

SAVE_FILE = "savegame.json"


# ===============================
# HELFER / UPGRADES
# ===============================
class Upgrade:
    def __init__(self, name, base_price, increment=1, sprite="Mauszeiger.png", scale=0.08):
        self.name = name
        self.base_price = base_price
        self.price = base_price
        self.increment = increment
        self.count = 0
        self.sprite = sprite
        self.scale = scale
        self.sprites = arcade.SpriteList()

    def buy(self):
       # while self.paused:
            self.count += 1
            self.price = int(self.price * 1.5)
            return self.increment


# ===============================
# GAME VIEW
# ===============================
class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.WHITE)
        self.paused = False
        self.glitches = 0
        self.timer = 0

        # Upgrades / Helfer
        self.upgrades = [
            Upgrade("Mauszeiger Helfer", 10, increment=1),
            Upgrade("Super Helfer", 100, increment=5, scale=0.12),
            Upgrade("Mega Helfer", 500, increment=20, scale=0.15),
        ]

        # Clicker
        self.clicker = arcade.Sprite("Background.png", 0.75)
        self.clicker.center_x = SCREEN_WIDTH // 2
        self.clicker.center_y = SCREEN_HEIGHT // 2

        # UI
        self.ui = arcade.gui.UIManager()
        self.ui.enable()

        # Store Button
        self.store_button = arcade.gui.UIFlatButton(text="Store", width=200)
        self.store_button.on_click = self.open_store

        # Options Button
        self.options_button = arcade.gui.UIFlatButton(text="Optionen", width=200)
        self.options_button.on_click = self.open_options

        # UI Layout
        anchor = arcade.gui.UIAnchorLayout()
        anchor.add(self.store_button, anchor_x="left", anchor_y="bottom", align_x=20, align_y=20)
        anchor.add(self.options_button, anchor_x="right", anchor_y="bottom", align_x=-20, align_y=20)
        self.ui.add(anchor)

        # Klick-Effekte
        self.click_effects = []

        # Lade Spielstand
        self.load_game()

        self.store = 0
        self.options = 0

    # -----------------
    # HELFER ERZEUGEN
    # -----------------
    def create_helper_sprite(self, upgrade: Upgrade):
        helper = arcade.Sprite(upgrade.sprite, upgrade.scale)
        helper.center_x = self.clicker.center_x
        helper.center_y = self.clicker.center_y
        upgrade.sprites.append(helper)

    # -----------------
    # STORE ÖFFNEN
    # -----------------
    def open_store(self, event):
        self.paused = True
        self.ui.disable()  # Haupt-UI deaktivieren
        self.window.show_view(StoreView(self))
        self.store += 1
        if self.store == 2:
            self.paused = False
            self.ui.enable()

    # -----------------
    # OPTIONS ÖFFNEN
    # -----------------
    def open_options(self, event):
        self.paused = True
        self.ui.disable()  # Haupt-UI deaktivieren
        self.window.show_view(OptionsView(self))
        if self.options == 2:
            self.paused = False
            self.ui.enable()

    #----------------
    # On_Key_Press
    #----------------
    def on_key_press(self, key, modifiers):
        if key == arcade.key.P:
            print(self.paused)


    # -----------------
    # ZEICHNEN
    # -----------------
    def on_draw(self):
        self.clear()
        arcade.draw_sprite(self.clicker)


        # Helfer
        for upgrade in self.upgrades:
            upgrade.sprites.draw()

        # Klick-Effekte
        for effect in self.click_effects:
            arcade.draw_text(effect["text"], effect["x"], effect["y"], arcade.color.RED, 14)

        # UI nur zeichnen, wenn nicht pausiert
        if not self.paused:
            self.ui.draw()

        # Glitches
        arcade.draw_text(f"Glitches: {self.glitches}", 10, 10, arcade.color.BLACK, 20)
        total_per_sec = sum(u.count * u.increment for u in self.upgrades)
        arcade.draw_text(f"Glitches / Sek: {total_per_sec}", 10, 35, arcade.color.DARK_GREEN, 16)

        # Anzeige der Helfer
        y_offset = 60
        for upgrade in self.upgrades:
            arcade.draw_text(f"{upgrade.name}: {upgrade.count}", 10, y_offset, arcade.color.BLACK, 16)
            y_offset += 25

        if self.paused:
            self.click = False
            print("PAUSIERT")
        
    # -----------------
    # MAUSKLICK
    # -----------------
    def on_mouse_press(self, x, y, button, modifiers):
        if self.paused:
            return

        if self.clicker.collides_with_point((x, y)):
            self.glitches += 1
            # Klick-Effekt erzeugen
            self.click_effects.append({"x": x + random.randint(-10, 10),
                                       "y": y + random.randint(-10, 10),
                                       "text": "+1",
                                       "timer": 0})

    # -----------------
    # UPDATE
    # -----------------
    def on_update(self, delta_time):
        # Update Klick-Effekte
        for effect in self.click_effects:
            effect["y"] += 20 * delta_time
            effect["timer"] += delta_time
        self.click_effects = [e for e in self.click_effects if e["timer"] < 0.5]

        if self.paused:
            return

        # Helfer jede Sekunde Glitches generieren
        self.timer += delta_time
        if self.timer >= 1:
            self.timer = 0
            for upgrade in self.upgrades:
                self.glitches += upgrade.count * upgrade.increment

        # Helfer rotieren
        for upgrade in self.upgrades:
            if len(upgrade.sprites) == 0:
                continue
            angle_offset = self.timer * 360
            radius = 140
            for i, helper in enumerate(upgrade.sprites):
                angle = angle_offset + (360 / max(len(upgrade.sprites), 1)) * i
                rad = math.radians(angle)
                helper.center_x = self.clicker.center_x + math.cos(rad) * radius
                helper.center_y = self.clicker.center_y + math.sin(rad) * radius
                helper.angle = -angle

    # -----------------
    # SAVE / LOAD
    # -----------------
    def save_game(self):
        data = {
            "glitches": self.glitches,
            "upgrades": [{"count": u.count, "price": u.price} for u in self.upgrades]
        }
        with open(SAVE_FILE, "w") as f:
            json.dump(data, f)

    def load_game(self):
        if os.path.exists(SAVE_FILE):
            with open(SAVE_FILE, "r") as f:
                data = json.load(f)
                self.glitches = data.get("glitches", 0)
                upgrade_data = data.get("upgrades", [])
                for u, d in zip(self.upgrades, upgrade_data):
                    u.count = d.get("count", 0)
                    u.price = d.get("price", u.base_price)
                    for _ in range(u.count):
                        self.create_helper_sprite(u)


# ===============================
# STORE VIEW
# ===============================
class StoreView(arcade.View):
    def __init__(self, game: GameView):
        super().__init__()
        arcade.set_background_color(arcade.color.DARK_GRAY)
        self.game = game
        self.ui = arcade.gui.UIManager()
        self.ui.enable()

        layout = arcade.gui.UIBoxLayout(vertical=True, space_between=15)

        title = arcade.gui.UILabel(text="STORE", font_size=32)
        layout.add(title)

        # Buttons für alle Upgrades
        self.buy_buttons = []
        for upgrade in self.game.upgrades:
            btn = arcade.gui.UIFlatButton(width=450)
            btn.on_click = lambda event, u=upgrade, b=btn: self.buy_upgrade(u, b)
            layout.add(btn)
            self.buy_buttons.append((upgrade, btn))

        # Back Button
        back_button = arcade.gui.UIFlatButton(text="Zurück", width=200)
        back_button.on_click = self.go_back
        layout.add(back_button)

        anchor = arcade.gui.UIAnchorLayout()
        anchor.add(layout, anchor_x="center", anchor_y="center")
        self.ui.add(anchor)

        self.update_buttons()

    # -----------------
    # BUTTON TEXT + ENABLE
    # -----------------
    def update_buttons(self):
        for upgrade, btn in self.buy_buttons:
            btn.text = f"{upgrade.name} (+{upgrade.increment}/Sek) - Preis: {upgrade.price}"
            btn.disabled = self.game.glitches < upgrade.price

    # -----------------
    # KAUFEN
    # -----------------
    def buy_upgrade(self, upgrade: Upgrade, button: arcade.gui.UIFlatButton):
        if self.game.glitches >= upgrade.price:
            self.game.glitches -= upgrade.price
            upgrade.buy()
            self.game.create_helper_sprite(upgrade)
            self.update_buttons()

    # -----------------
    # ZURÜCK
    # -----------------
    def go_back(self, event):
        self.game.paused = False
        self.game.ui.enable()  # Haupt-UI wieder aktivieren
        self.game.save_game()
        self.window.show_view(self.game)

    def on_draw(self):
        self.clear()
        self.ui.draw()


# ===============================
# OPTIONS VIEW
# ===============================
class OptionsView(arcade.View):
    def __init__(self, game: GameView):
        super().__init__()
        arcade.set_background_color(arcade.color.LIGHT_GRAY)
        self.game = game
        self.ui = arcade.gui.UIManager()
        self.ui.enable()

        layout = arcade.gui.UIBoxLayout(vertical=True, space_between=15)

        title = arcade.gui.UILabel(text="OPTIONEN", font_size=32)
        layout.add(title)

        # Save Button
        save_btn = arcade.gui.UIFlatButton(text="Speichern", width=200)
        save_btn.on_click = self.save_game
        layout.add(save_btn)

        # Load Button
        load_btn = arcade.gui.UIFlatButton(text="Laden", width=200)
        load_btn.on_click = self.load_game
        layout.add(load_btn)

        # Back Button
        back_btn = arcade.gui.UIFlatButton(text="Zurück", width=200)
        back_btn.on_click = self.go_back
        layout.add(back_btn)

        anchor = arcade.gui.UIAnchorLayout()
        anchor.add(layout, anchor_x="center", anchor_y="center")
        self.ui.add(anchor)

    def save_game(self, event):
        self.game.save_game()

    def load_game(self, event):
        self.game.load_game()

    def go_back(self, event):
        self.game.paused = False
        self.game.ui.enable()  # Haupt-UI wieder aktivieren
        self.window.show_view(self.game)

    def on_draw(self):
        self.clear()
        self.ui.draw()


# ===============================
# MAIN
# ===============================
def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.show_view(GameView())
    arcade.run()


if __name__ == "__main__":
    main()