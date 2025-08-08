import arcade, random


class Labyrinth(arcade.Window):
    def __init__(self):
        super().__init__(500, 500, "Labyrinth")

        self.tod = 0
        self.exits = ["self.exit1", "self.exit2", "self.exit3", "self.exit4", "self.exit5"]
        self.exit_choice = random.choice(self.exits)  # Randomly select an exit
        print(self.exit_choice)

        arcade.set_background_color(arcade.color.GREEN)

        self.block_liste = arcade.SpriteList()
        self.spieler_liste = arcade.SpriteList()
        self.mauer_liste = arcade.SpriteList()
        self.exit_liste = arcade.SpriteList()

        # Create maze walls and floors
        self.create_maze()

        # Create the player sprite
        self.spieler = arcade.Sprite("Spieler.png", 0.5)
        self.spieler.center_x = 75
        self.spieler.center_y = 25
        self.spieler_liste.append(self.spieler)

        # Create physics engines
        self.physiks = arcade.PhysicsEngineSimple(self.spieler, self.mauer_liste)

    def create_maze(self):
        """ Creates the maze with walls, floors, and exits. """
        # Generate blocks for walls and floors
        for x in range(0, 500, 50):
            for y in range(0, 500, 50):
                if random.random() < 0.2:  # Some blocks are walls
                    block = arcade.Sprite("Mauer.png")
                    block.center_x = x
                    block.center_y = y
                    self.mauer_liste.append(block)
                else:
                    block = arcade.Sprite("Boden.png")
                    block.center_x = x
                    block.center_y = y
                    self.block_liste.append(block)

        # Add exit locations
        for i in range(1, 6):
            exit_sprite = arcade.Sprite("Exit.png")
            exit_sprite.center_x = random.randint(50, 450)
            exit_sprite.center_y = random.randint(50, 450)
            self.exit_liste.append(exit_sprite)

        # Assign random exit as the winning exit
        self.exit_choice = random.choice(self.exit_liste)

    def on_key_press(self, symbol, modifiers):
        """ Handle player movement """
        if symbol == arcade.key.W:
            self.spieler.change_y = 4
        if symbol == arcade.key.A:
            self.spieler.change_x = -4
        if symbol == arcade.key.S:
            self.spieler.change_y = -4
        if symbol == arcade.key.D:
            self.spieler.change_x = 4

    def on_key_release(self, symbol, modifiers):
        """ Stop player movement """
        if symbol == arcade.key.W:
            self.spieler.change_y = 0
        if symbol == arcade.key.A:
            self.spieler.change_x = 0
        if symbol == arcade.key.S:
            self.spieler.change_y = 0
        if symbol == arcade.key.D:
            self.spieler.change_x = 0

    def on_update(self, delta_time):
        """ Update game state, including player movement and collision checks """
        self.spieler_liste.update()
        self.physiks.update()

        # Check if the player has reached the exit
        if arcade.check_for_collision(self.spieler, self.exit_choice):
            print(f"You have reached the exit {self.exit_choice}. Congratulations!")

    def on_draw(self):
        """ Draw everything on the screen """
        self.clear()
        self.block_liste.draw()
        self.mauer_liste.draw()
        self.spieler_liste.draw()
        self.exit_liste.draw()


if __name__ == "__main__":
    Labyrinth()
    arcade.run()
