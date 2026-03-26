import arcade, random
import arcade.color
import arcade.color
import arcade.key 


class Labyrinth(arcade.Window):
    def __init__(self):
        super().__init__(500, 500, "Labyrinth")

        self.tod = 0
        self.exits = ["exit1", "exit2", "exit3", "exit4", "exit5"]
        self.exit_choice = random.choice(self.exits)
        print(self.exit_choice)
        self.zeit = 0 
        

        self.hacker = input()
        if self.hacker == "⠀":
            print(self.exit_choice)
    
        
        self.check_Atom_Spieler = False
        self.schaltkasten = arcade.Sprite("Schaltkasten.png")
        self.schaltkasten.center_x =250
        self.schaltkasten.center_y =250


        

        arcade.set_background_color(arcade.color.DARK_GREEN)

        self.block_liste = arcade.SpriteList()
        self.spieler_liste = arcade.SpriteList()
        self.mauer_liste = arcade.SpriteList()
        self.exit_liste = arcade.SpriteList()
        self.atom_liste = arcade.SpriteList()
        self.item_liste = arcade.SpriteList()


        #1

        block=arcade.Sprite("Mauer.png")
        block.center_x = 25
        block.center_y = 25
        self.mauer_liste.append(block)

        block=arcade.Sprite("Mauer.png")
        block.center_x = 25
        block.center_y = 75
        self.mauer_liste.append(block)

        block=arcade.Sprite("Mauer6.png")
        block.center_x = 25
        block.center_y = 125
        self.mauer_liste.append(block)

        block=arcade.Sprite("Mauer.png")
        block.center_x = 25
        block.center_y = 175
        self.mauer_liste.append(block)

        block=arcade.Sprite("Mauer.png")
        block.center_x = 25
        block.center_y = 225
        self.mauer_liste.append(block)

        block=arcade.Sprite("Mauer6.png")
        block.center_x = 25
        block.center_y = 275
        self.mauer_liste.append(block)

        block=arcade.Sprite("Mauer.png")
        block.center_x = 25
        block.center_y = 325
        self.mauer_liste.append(block)

        block=arcade.Sprite("Mauer.png")
        block.center_x = 25
        block.center_y = 375
        self.mauer_liste.append(block)

        block=arcade.Sprite("Mauer.png")
        block.center_x = 25
        block.center_y = 425
        self.mauer_liste.append(block)

        block=arcade.Sprite("Mauer.png")
        block.center_x = 25
        block.center_y = 475
        self.mauer_liste.append(block)

        block=arcade.Sprite("Mauer.png")
        block.center_x = 25
        block.center_y = 525
        self.mauer_liste.append(block)


        #2
        block=arcade.Sprite("Mauer.png")
        block.center_x = 75
        block.center_y = -25
        self.mauer_liste.append(block)

        block=arcade.Sprite("Boden.png")
        block.center_x = 75
        block.center_y = 25
        self.block_liste.append(block)

        block=arcade.Sprite("Boden.png")
        block.center_x = 75
        block.center_y = 75
        self.block_liste.append(block)

        block=arcade.Sprite("Mauer2.png")
        block.center_x = 75
        block.center_y = 125
        self.mauer_liste.append(block)

        block=arcade.Sprite("Boden.png")
        block.center_x = 75
        block.center_y = 175
        self.block_liste.append(block)

        block=arcade.Sprite("Boden.png")
        block.center_x = 75
        block.center_y = 225
        self.block_liste.append(block)

        block=arcade.Sprite("Mauer2.png")
        block.center_x = 75
        block.center_y = 275
        self.mauer_liste.append(block)

        block=arcade.Sprite("Boden.png")
        block.center_x = 75
        block.center_y = 325
        self.block_liste.append(block)

        block=arcade.Sprite("Boden.png")
        block.center_x = 75
        block.center_y = 375
        self.block_liste.append(block)

        self.exit1=arcade.Sprite("Exit.png")
        self.exit1.center_x = 75
        self.exit1.center_y = 425
        self.exit_liste.append(self.exit1)

        block=arcade.Sprite("Boden.png")
        block.center_x = 75
        block.center_y = 475
        self.block_liste.append(block)

        block=arcade.Sprite("Mauer.png")
        block.center_x = 75
        block.center_y = 525
        self.mauer_liste.append(block)

        #3
        block=arcade.Sprite("Mauer.png")
        block.center_x = 125
        block.center_y = 25
        self.mauer_liste.append(block)

        block=arcade.Sprite("Boden.png")
        block.center_x = 125
        block.center_y = 75
        self.block_liste.append(block)

        block=arcade.Sprite("Boden.png")
        block.center_x = 125
        block.center_y = 125
        self.block_liste.append(block)

        block=arcade.Sprite("Boden.png")
        block.center_x = 125
        block.center_y = 175
        self.block_liste.append(block)

        block=arcade.Sprite("Boden.png")
        block.center_x = 125
        block.center_y = 225
        self.block_liste.append(block)

        block=arcade.Sprite("Boden.png")
        block.center_x = 125
        block.center_y = 275
        self.block_liste.append(block)

        block=arcade.Sprite("Boden.png")
        block.center_x = 125
        block.center_y = 325
        self.block_liste.append(block)

        block=arcade.Sprite("Mauer.png")
        block.center_x = 125
        block.center_y = 375
        self.mauer_liste.append(block)

        block=arcade.Sprite("Mauer.png")
        block.center_x = 125
        block.center_y = 425
        self.mauer_liste.append(block)

        block=arcade.Sprite("Boden.png")
        block.center_x = 125
        block.center_y = 475
        self.block_liste.append(block)

        block=arcade.Sprite("Mauer.png")
        block.center_x = 125
        block.center_y = 525
        self.mauer_liste.append(block)




        #4
        block=arcade.Sprite("Mauer.png")
        block.center_x = 175
        block.center_y = 25
        self.mauer_liste.append(block)

        block=arcade.Sprite("Boden.png")
        block.center_x = 175
        block.center_y = 75
        self.block_liste.append(block)

        block=arcade.Sprite("Mauer.png")
        block.center_x = 175
        block.center_y = 125
        self.mauer_liste.append(block)

        block=arcade.Sprite("Mauer.png")
        block.center_x = 175
        block.center_y = 175
        self.mauer_liste.append(block)

        block=arcade.Sprite("Boden.png")
        block.center_x = 175
        block.center_y = 225
        self.block_liste.append(block)

        block=arcade.Sprite("Mauer.png")
        block.center_x = 175
        block.center_y = 275
        self.mauer_liste.append(block)

        block=arcade.Sprite("Boden.png")
        block.center_x = 175
        block.center_y = 325
        self.block_liste.append(block)

        block=arcade.Sprite("Boden.png")
        block.center_x = 175
        block.center_y = 375
        self.block_liste.append(block)

        self.exit2=arcade.Sprite("Exit.png")
        self.exit2.center_x = 175
        self.exit2.center_y = 425
        self.exit_liste.append(self.exit2)

        block=arcade.Sprite("Boden.png")
        block.center_x = 175
        block.center_y = 475
        self.block_liste.append(block)

        block=arcade.Sprite("Mauer.png")
        block.center_x = 175
        block.center_y = 525
        self.mauer_liste.append(block)

        #4
        block=arcade.Sprite("Mauer.png")
        block.center_x = 225
        block.center_y = 25
        self.mauer_liste.append(block)

        block=arcade.Sprite("Mauer.png")
        block.center_x = 225
        block.center_y = 75
        self.mauer_liste.append(block)

        block=arcade.Sprite("Boden.png")
        block.center_x = 225
        block.center_y = 125
        self.block_liste.append(block)

        block=arcade.Sprite("Boden.png")
        block.center_x = 225
        block.center_y = 175
        self.block_liste.append(block)

        block=arcade.Sprite("Boden.png")
        block.center_x = 225
        block.center_y = 225
        self.block_liste.append(block)

        block=arcade.Sprite("Mauer.png")
        block.center_x = 225
        block.center_y = 275
        self.mauer_liste.append(block)

        block=arcade.Sprite("Boden.png")
        block.center_x = 225
        block.center_y = 325
        self.block_liste.append(block)

        block=arcade.Sprite("Mauer.png")
        block.center_x = 225
        block.center_y = 375
        self.mauer_liste.append(block)

        block=arcade.Sprite("Mauer.png")
        block.center_x = 225
        block.center_y = 425
        self.mauer_liste.append(block)

        block=arcade.Sprite("Boden.png")
        block.center_x = 225
        block.center_y = 475
        self.block_liste.append(block)

        block=arcade.Sprite("Mauer.png")
        block.center_x = 225
        block.center_y = 525
        self.mauer_liste.append(block)

        #5
        block=arcade.Sprite("Boden.png")
        block.center_x = 275
        block.center_y = 25
        self.block_liste.append(block)

        block=arcade.Sprite("Boden.png")
        block.center_x = 275
        block.center_y = 75
        self.block_liste.append(block)

        block=arcade.Sprite("Mauer.png")
        block.center_x = 275
        block.center_y = 125
        self.mauer_liste.append(block)

        block=arcade.Sprite("Boden.png")
        block.center_x = 275
        block.center_y = 175
        self.block_liste.append(block)

        block=arcade.Sprite("Mauer.png")
        block.center_x = 275
        block.center_y = 225
        self.mauer_liste.append(block)

        block=arcade.Sprite("Boden.png")
        block.center_x = 275
        block.center_y = 275
        self.block_liste.append(block)

        block=arcade.Sprite("Boden.png")
        block.center_x = 275
        block.center_y = 325
        self.block_liste.append(block)

        block=arcade.Sprite("Boden.png")
        block.center_x = 275
        block.center_y = 375
        self.block_liste.append(block)

        self.exit3=arcade.Sprite("Exit.png")
        self.exit3.center_x = 275
        self.exit3.center_y = 425
        self.exit_liste.append(self.exit3)

        block=arcade.Sprite("Boden.png")
        block.center_x = 275
        block.center_y = 475
        self.block_liste.append(block)

        block=arcade.Sprite("Mauer.png")
        block.center_x = 275
        block.center_y = 525
        self.mauer_liste.append(block)

        #6
        block=arcade.Sprite("Mauer.png")
        block.center_x = 325
        block.center_y = 25
        self.mauer_liste.append(block)

        block=arcade.Sprite("Mauer.png")
        block.center_x = 325
        block.center_y = 75
        self.mauer_liste.append(block)

        block=arcade.Sprite("Mauer.png")
        block.center_x = 325
        block.center_y = 125
        self.mauer_liste.append(block)

        block=arcade.Sprite("Boden.png")
        block.center_x = 325
        block.center_y = 175
        self.block_liste.append(block)

        block=arcade.Sprite("Mauer.png")
        block.center_x = 325
        block.center_y = 225
        self.mauer_liste.append(block)

        block=arcade.Sprite("Boden.png")
        block.center_x = 325
        block.center_y = 275
        self.block_liste.append(block)

        block=arcade.Sprite("Boden.png")
        block.center_x = 325
        block.center_y = 325
        self.block_liste.append(block)

        block=arcade.Sprite("Mauer.png")
        block.center_x = 325
        block.center_y = 375
        self.mauer_liste.append(block)

        block=arcade.Sprite("Mauer.png")
        block.center_x = 325
        block.center_y = 425
        self.mauer_liste.append(block)

        block=arcade.Sprite("Boden.png")
        block.center_x = 325
        block.center_y = 475
        self.block_liste.append(block)

        block=arcade.Sprite("Mauer.png")
        block.center_x = 325
        block.center_y = 525
        self.mauer_liste.append(block)

        #7
        block=arcade.Sprite("Mauer.png")
        block.center_x = 375
        block.center_y = 25
        self.mauer_liste.append(block)

        block=arcade.Sprite("Boden.png")
        block.center_x = 375
        block.center_y = 75
        self.block_liste.append(block)

        block=arcade.Sprite("Boden.png")
        block.center_x = 375
        block.center_y = 125
        self.block_liste.append(block)

        block=arcade.Sprite("Boden.png")
        block.center_x = 375
        block.center_y = 175
        self.block_liste.append(block)

        block=arcade.Sprite("Mauer.png")
        block.center_x = 375
        block.center_y = 225
        self.mauer_liste.append(block)

        block=arcade.Sprite("Boden.png")
        block.center_x = 375
        block.center_y = 275
        self.block_liste.append(block)

        block=arcade.Sprite("Boden.png")
        block.center_x = 375
        block.center_y = 325
        self.block_liste.append(block)

        block=arcade.Sprite("Boden.png")
        block.center_x = 375
        block.center_y = 375
        self.block_liste.append(block)

        self.exit4=arcade.Sprite("Exit.png")
        self.exit4.center_x = 375
        self.exit4.center_y = 425
        self.exit_liste.append(self.exit4)

        block=arcade.Sprite("Boden.png")
        block.center_x = 375
        block.center_y = 475
        self.block_liste.append(block)

        block=arcade.Sprite("Mauer.png")
        block.center_x = 375
        block.center_y = 525
        self.mauer_liste.append(block)

        #8
        block=arcade.Sprite("Mauer.png")
        block.center_x = 425
        block.center_y = 25
        self.mauer_liste.append(block)

        block=arcade.Sprite("Mauer.png")
        block.center_x = 425
        block.center_y = 75
        self.mauer_liste.append(block)

        block=arcade.Sprite("Mauer.png")
        block.center_x = 425
        block.center_y = 125
        self.mauer_liste.append(block)

        block=arcade.Sprite("Mauer.png")
        block.center_x = 425
        block.center_y = 175
        self.mauer_liste.append(block)

        block=arcade.Sprite("Mauer.png")
        block.center_x = 425
        block.center_y = 225
        self.mauer_liste.append(block)

        block=arcade.Sprite("Boden.png")
        block.center_x = 425
        block.center_y = 275
        self.block_liste.append(block)

        block=arcade.Sprite("Boden.png")
        block.center_x = 425
        block.center_y = 325
        self.block_liste.append(block)

        block=arcade.Sprite("Mauer.png")
        block.center_x = 425
        block.center_y = 375
        self.mauer_liste.append(block)

        block=arcade.Sprite("Mauer.png")
        block.center_x = 425
        block.center_y = 425
        self.mauer_liste.append(block)

        block=arcade.Sprite("Boden.png")
        block.center_x = 425
        block.center_y = 475
        self.block_liste.append(block)

        block=arcade.Sprite("Mauer.png")
        block.center_x = 425
        block.center_y = 525
        self.mauer_liste.append(block)

        #9
        block=arcade.Sprite("Mauer.png")
        block.center_x = 475
        block.center_y = 25
        self.mauer_liste.append(block)

        block=arcade.Sprite("Mauer.png")
        block.center_x = 475
        block.center_y = 75
        self.mauer_liste.append(block)

        block=arcade.Sprite("Mauer.png")
        block.center_x = 475
        block.center_y = 125
        self.mauer_liste.append(block)

        block=arcade.Sprite("Mauer.png")
        block.center_x = 475
        block.center_y = 175
        self.mauer_liste.append(block)

        block=arcade.Sprite("Boden.png")
        block.center_x = 475
        block.center_y = 225
        self.block_liste.append(block)

        block=arcade.Sprite("Boden.png")
        block.center_x = 475
        block.center_y = 275
        self.block_liste.append(block)

        block=arcade.Sprite("Boden.png")
        block.center_x = 475
        block.center_y = 325
        self.block_liste.append(block)

        block=arcade.Sprite("Boden.png")
        block.center_x = 475
        block.center_y = 375
        self.block_liste.append(block)

        self.exit5=arcade.Sprite("Exit.png")
        self.exit5.center_x = 475
        self.exit5.center_y = 425
        self.exit_liste.append(self.exit5)

        block=arcade.Sprite("Boden.png")
        block.center_x = 475
        block.center_y = 475
        self.block_liste.append(block)

        block=arcade.Sprite("Mauer.png")
        block.center_x = 475
        block.center_y = 525
        self.mauer_liste.append(block)

        #10

        block=arcade.Sprite("Mauer.png")
        block.center_x = 525
        block.center_y = 475
        self.mauer_liste.append(block)

        block=arcade.Sprite("Mauer.png")
        block.center_x = 525
        block.center_y = 225
        self.mauer_liste.append(block)

        block=arcade.Sprite("Mauer.png")
        block.center_x = 525
        block.center_y = 275
        self.mauer_liste.append(block)

        block=arcade.Sprite("Mauer.png")
        block.center_x = 525
        block.center_y = 325
        self.mauer_liste.append(block)

        block=arcade.Sprite("Mauer.png")
        block.center_x = 525
        block.center_y = 375
        self.mauer_liste.append(block)

        block=arcade.Sprite("Mauer.png")
        block.center_x = 525
        block.center_y = 425
        self.mauer_liste.append(block)
    

        self.Atom=arcade.Sprite("Atomreaktor_kaputt.png")
        self.Atom.center_x = 475
        self.Atom.center_y = 275
        self.atom_liste.append(self.Atom)

        self.spieler = arcade.Sprite("Spieler.png", 0.5)
        self.spieler.center_x = 75
        self.spieler.center_y = 25
        self.spieler_liste.append(self.spieler)
        
        #Item
        self.Schere = arcade.Sprite("Schere.png", 0.5)
        self.Schere.center_x = 375
        self.Schere.center_y = 75
        self.item_liste.append(self.Schere)

        
        self.sieg = arcade.Sprite("Sieg.png")
        self.sieg.center_x=250
        self.sieg.center_y=250


        self.hotbar = arcade.Sprite("Horbar.png")
        self.hotbar.center_x = 570
        self.hotbar.center_y = 510
        



        self.physiks = arcade.PhysicsEngineSimple(self.spieler, self.mauer_liste)



    def on_mouse_press(self, x, y, button, modifiers):
        if 427 == self.Schere.center_x:
            if x in range(125, 375):
                self.schaltkasten.texture = arcade.load_texture("Schaltkasten222.png")

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.W :
            self.spieler.change_y = 4
        if symbol == arcade.key.A :
            self.spieler.change_x = -4
        if symbol == arcade.key.S :        
            self.spieler.change_y = -4
        if symbol == arcade.key.D :
            self.spieler.change_x = 4

    
    def on_key_release(self, symbol, modifiers):
        if symbol == arcade.key.W :
            self.spieler.change_y = 0
        if symbol == arcade.key.A :
            self.spieler.change_x = 0
        if symbol == arcade.key.S :
            self.spieler.change_y = 0
        if symbol == arcade.key.D :
            self.spieler.change_x = 0
    
    def on_update(self, delta_time):
        self.spieler_liste.update()
        if self.hacker != "⠀":
            self.physiks.update()
        self.zeit = self.zeit + delta_time
        if self.zeit <= 10:
            arcade.draw_text("Entschärfe die Bombe",)
       

        
        if self.exit_choice == "exit1":
            if arcade.check_for_collision(self.spieler, self.exit1):
                self.spieler.center_y = 475
                self.spieler.center_x = 75 
        if self.exit_choice == "exit2":
            if arcade.check_for_collision(self.spieler, self.exit2):
                self.spieler.center_y = 475
                self.spieler.center_x = 175
        if self.exit_choice == "exit3":
            if arcade.check_for_collision(self.spieler, self.exit3):
                self.spieler.center_y = 475
                self.spieler.center_x = 275
        if self.exit_choice == "exit4":
            if arcade.check_for_collision(self.spieler, self.exit4):
                self.spieler.center_y = 475
                self.spieler.center_x = 375
        if self.exit_choice == "exit5":                
            if arcade.check_for_collision(self.spieler, self.exit5):
                self.spieler.center_y = 475
                self.spieler.center_x = 475
        if arcade.check_for_collision_with_list(self.spieler, self.exit_liste):
            self.spieler.center_y = 25
            self.spieler.center_x = 75

        if arcade.check_for_collision(self.spieler, self.Schere):
           self.Schere.center_x= 427
           self.Schere.center_y= 475

            







    
        if arcade.check_for_collision(self.spieler, self.Atom):
            self.check_Atom_Spieler = True
        else:
            self.check_Atom_Spieler = False

        




    def on_draw(self,):
        self.clear()
        self.block_liste.draw()
        self.mauer_liste.draw()
        self.hotbar.draw()
        self.spieler_liste.draw()
        self.atom_liste.draw()
        self.exit1.draw()
        self.exit2.draw()
        self.exit3.draw()
        self.exit4.draw()
        self.exit5.draw()
        self.item_liste.draw()
       
        if self.check_Atom_Spieler == True: 
            self.schaltkasten.draw()
        if self.schaltkasten.texture == arcade.load_texture("Schaltkasten222.png"):
            self.sieg.draw()
            
Labyrinth()
arcade.run()