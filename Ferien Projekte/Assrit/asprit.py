import arcade

# Fenster- und Raster-Konfiguration
WINDOW_WIDTH = 512
WINDOW_HEIGHT = 512
PIXEL_SIZE = 32
GRID_WIDTH = WINDOW_WIDTH // PIXEL_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // PIXEL_SIZE

# Seitenleiste + Farben
COLORS = [arcade.color.BLACK, arcade.color.RED, arcade.color.GREEN, arcade.color.BLUE]
current_color_index = 0


class PixelEditor(arcade.Window):
    def __init__(self):
        super().__init__(WINDOW_WIDTH + 200, WINDOW_HEIGHT, "Pixel Editor mit Seitenleiste")
        arcade.set_background_color(arcade.color.WHITE)
        self.grid = [[arcade.color.WHITE for _ in range(GRID_HEIGHT)] for _ in range(GRID_WIDTH)]

    def on_draw(self):
        self.clear()

        # Pixel-Zeichenbereich
        for x in range(GRID_WIDTH):
            for y in range(GRID_HEIGHT):
                color = self.grid[x][y]
                px = x * PIXEL_SIZE + PIXEL_SIZE // 2
                py = y * PIXEL_SIZE + PIXEL_SIZE // 2
                arcade.draw_rectangle_filled(px, py, PIXEL_SIZE, PIXEL_SIZE, color)

        # Rasterlinien
        for x in range(GRID_WIDTH + 1):
            arcade.draw_line(x * PIXEL_SIZE, 0, x * PIXEL_SIZE, WINDOW_HEIGHT, arcade.color.LIGHT_GRAY)
        for y in range(GRID_HEIGHT + 1):
            arcade.draw_line(0, y * PIXEL_SIZE, WINDOW_WIDTH, y * PIXEL_SIZE, arcade.color.LIGHT_GRAY)

        # Seitenleiste
        sidebar_x = WINDOW_WIDTH
        arcade.draw_line(sidebar_x, 0, sidebar_x, WINDOW_HEIGHT, arcade.color.DARK_GRAY)

        # Farbauswahl-Knöpfe
        for i, color in enumerate(COLORS):
            bx = sidebar_x + 40
            by = 60 + i * 60
            arcade.draw_rectangle_filled(bx + 20, by + 20, 40, 40, color)
            if i == current_color_index:
                arcade.draw_text("✓", bx + 10, by + 10, arcade.color.BLACK, 24)

        # "Löschen"-Button
        bx = sidebar_x + 40
        by = WINDOW_HEIGHT - 80
        arcade.draw_rectangle_filled(bx + 40, by + 20, 80, 40, arcade.color.LIGHT_GRAY)
        arcade.draw_text("Löschen", bx + 10, by + 10, arcade.color.BLACK, 20)

    def on_mouse_press(self, x, y, button, modifiers):
        sidebar_x = WINDOW_WIDTH

        # Farbauswahl
        for i in range(len(COLORS)):
            bx = sidebar_x + 40
            by = 60 + i * 60
            if bx <= x <= bx + 40 and by <= y <= by + 40:
                global current_color_index
                current_color_index = i
                return

        # "Löschen"-Button
        bx = sidebar_x + 40
        by = WINDOW_HEIGHT - 80
        if bx <= x <= bx + 80 and by <= y <= by + 40:
            for xg in range(GRID_WIDTH):
                for yg in range(GRID_HEIGHT):
                    self.grid[xg][yg] = arcade.color.WHITE
            return

        # Zeichenbereich
        if x < WINDOW_WIDTH:
            self.paint_pixel(x, y)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if x < WINDOW_WIDTH:
            self.paint_pixel(x, y)

    def paint_pixel(self, x, y):
        grid_x = int(x // PIXEL_SIZE)
        grid_y = int(y // PIXEL_SIZE)
        if 0 <= grid_x < GRID_WIDTH and 0 <= grid_y < GRID_HEIGHT:
            self.grid[grid_x][grid_y] = COLORS[current_color_index]

    def on_key_press(self, key, modifiers):
        pass  # Aktuell keine Tastenkürzel


if __name__ == "__main__":
    app = PixelEditor()
    arcade.run()
