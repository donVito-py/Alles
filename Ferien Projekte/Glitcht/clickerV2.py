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
# UPGRADES
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
        self.count += 1
        self.price = int(self.price * 1.15)


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
        self.rotation_time = 0

        self.upgrades = [
            Upgrade("Mauszeiger Helfer", 10, 1),
            Upgrade("Super Helfer", 100, 5, scale=0.12),
            Upgrade("Mega Helfer", 500, 20, scale=0.15),
        ]

        self.clicker = arcade.Sprite("Background.png", 0.75)
        self.clicker.center_x = SCREEN_WIDTH // 2
        self.clicker.center_y = SCREEN_HEIGHT // 2

        self.ui = arcade.gui.UIManager()
        self.ui.enable()

        self.store_button = arcade.gui.UIFlatButton(text="Store", width=150)
        self.store_button.on_click = self.open_store

        self.options_button = arcade.gui.UIFlatButton(text="Optionen", width=150)
        self.options_button.on_click = self.open_options

        anchor = arcade.gui.UIAnchorLayout()
        anchor.add(self.store_button, anchor_x="center", anchor_y="bottom", align_y=20)
        anchor.add(self.options_button, anchor_x="right", anchor_y="bottom", align_x=-20, align_y=20)
        self.ui.add(anchor)

        self.click_effects = []
        self.load_game()

    # -----------------
    # RESET
    # -----------------
    def reset_game(self):
        self.glitches = 0
        self.timer = 0
        self.rotation_time = 0

        for u in self.upgrades:
            u.count = 0
            u.price = u.base_price
            u.sprites.clear()

        if os.path.exists(SAVE_FILE):
            os.remove(SAVE_FILE)

    # -----------------
    def create_helper_sprite(self, upgrade):
        sprite = arcade.Sprite(upgrade.sprite, upgrade.scale)
        sprite.center_x = self.clicker.center_x
        sprite.center_y = self.clicker.center_y
        upgrade.sprites.append(sprite)

    # -----------------
    def open_store(self, event):
        self.paused = True
        self.ui.disable()
        self.window.show_view(StoreView(self))

    def open_options(self, event):
        self.paused = True
        self.ui.disable()
        self.window.show_view(OptionsView(self))

    # -----------------
    def on_draw(self):
        self.clear()
        arcade.draw_sprite(self.clicker)

        for u in self.upgrades:
            u.sprites.draw()

        for e in self.click_effects:
            arcade.draw_text(e["text"], e["x"], e["y"], arcade.color.RED, 14)

        if not self.paused:
            self.ui.draw()

        arcade.draw_text(f"Glitches: {self.glitches}", 10, 10, arcade.color.BLACK, 20)
        gps = sum(u.count * u.increment for u in self.upgrades)
        arcade.draw_text(f"/ Sekunde: {gps}", 10, 35, arcade.color.DARK_GREEN, 16)

        y = 60
        for u in self.upgrades:
            arcade.draw_text(f"{u.name}: {u.count}", 10, y, arcade.color.BLACK, 16)
            y += 25

        if self.paused:
            arcade.draw_text("PAUSIERT", SCREEN_WIDTH // 2, SCREEN_HEIGHT - 40,
                             arcade.color.RED, 20, anchor_x="center")

    # -----------------
    def on_mouse_press(self, x, y, button, modifiers):
        if self.paused:
            return

        if self.clicker.collides_with_point((x, y)):
            self.glitches += 1
            self.click_effects.append({
                "x": x + random.randint(-10, 10),
                "y": y,
                "text": "+1",
                "timer": 0
            })

    # -----------------
    def on_update(self, delta_time):
        for e in self.click_effects:
            e["y"] += 30 * delta_time
            e["timer"] += delta_time
        self.click_effects = [e for e in self.click_effects if e["timer"] < 0.5]

        if self.paused:
            return

        self.timer += delta_time
        self.rotation_time += delta_time

        if self.timer >= 1:
            self.timer = 0
            for u in self.upgrades:
                self.glitches += u.count * u.increment

        for u in self.upgrades:
            count = len(u.sprites)
            if count == 0:
                continue
            for i, h in enumerate(u.sprites):
                angle = (360 / count) * i + self.rotation_time * 60
                rad = math.radians(angle)
                h.center_x = self.clicker.center_x + math.cos(rad) * 140
                h.center_y = self.clicker.center_y + math.sin(rad) * 140
                h.angle = -angle

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
        if not os.path.exists(SAVE_FILE):
            return

        with open(SAVE_FILE, "r") as f:
            data = json.load(f)

        self.glitches = data.get("glitches", 0)

        for u in self.upgrades:
            u.sprites.clear()

        for u, d in zip(self.upgrades, data.get("upgrades", [])):
            u.count = d["count"]
            u.price = d["price"]
            for _ in range(u.count):
                self.create_helper_sprite(u)


# ===============================
# STORE VIEW
# ===============================
class StoreView(arcade.View):
    def __init__(self, game):
        super().__init__()
        arcade.set_background_color(arcade.color.DARK_GRAY)
        self.game = game

        self.ui = arcade.gui.UIManager()
        self.ui.enable()

        layout = arcade.gui.UIBoxLayout(vertical=True, space_between=15)
        layout.add(arcade.gui.UILabel(text="STORE", font_size=32))

        self.buttons = []
        for u in self.game.upgrades:
            btn = arcade.gui.UIFlatButton(width=450)
            btn.on_click = lambda e, up=u: self.buy(up)
            layout.add(btn)
            self.buttons.append(btn)

        back = arcade.gui.UIFlatButton(text="Zurück", width=200)
        back.on_click = self.back
        layout.add(back)

        anchor = arcade.gui.UIAnchorLayout()
        anchor.add(layout, anchor_x="center", anchor_y="center")
        self.ui.add(anchor)

        self.update_buttons()

    def update_buttons(self):
        for u, btn in zip(self.game.upgrades, self.buttons):
            btn.text = f"{u.name} (+{u.increment}/s) – {u.price}"
            btn.disabled = self.game.glitches < u.price

    def buy(self, upgrade):
        if self.game.glitches >= upgrade.price:
            self.game.glitches -= upgrade.price
            upgrade.buy()
            self.game.create_helper_sprite(upgrade)
            self.update_buttons()

    def back(self, event):
        self.game.paused = False
        self.game.ui.enable()
        self.game.save_game()
        self.game.ui.disable()
        self.window.show_view(self.game)

    def on_draw(self):
        self.clear()
        self.ui.draw()


# ===============================
# OPTIONS VIEW
# ===============================
class OptionsView(arcade.View):
    def __init__(self, game):
        super().__init__()
        arcade.set_background_color(arcade.color.LIGHT_GRAY)
        self.game = game

        self.ui = arcade.gui.UIManager()
        self.ui.enable()

        layout = arcade.gui.UIBoxLayout(vertical=True, space_between=15)
        layout.add(arcade.gui.UILabel(text="OPTIONEN", font_size=32))

        save_btn = arcade.gui.UIFlatButton(text="Speichern", width=200)
        save_btn.on_click = lambda e: self.game.save_game()
        layout.add(save_btn)

        load_btn = arcade.gui.UIFlatButton(text="Laden", width=200)
        load_btn.on_click = lambda e: self.game.load_game()
        layout.add(load_btn)

        reset_btn = arcade.gui.UIFlatButton(text="SPIEL ZURÜCKSETZEN", width=300)
        reset_btn.on_click = self.reset
        layout.add(reset_btn)

        back_btn = arcade.gui.UIFlatButton(text="Zurück", width=200)
        back_btn.on_click = self.back
        layout.add(back_btn)

        anchor = arcade.gui.UIAnchorLayout()
        anchor.add(layout, anchor_x="center", anchor_y="center")
        self.ui.add(anchor)

    def reset(self, event):
        self.game.reset_game()
        self.game.paused = False
        self.game.ui.enable()
        self.window.show_view(self.game)

    def back(self, event):
        self.game.paused = False
        self.game.ui.enable()
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
