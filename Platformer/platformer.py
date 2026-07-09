import arcade
from enum import Enum
import random
import time
# ============================================================================
# KONSTANTEN
# ============================================================================

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "Platti"

TILE_SCALING = 1.0
MAP_FILE_PATH = "Platfomer.tmx"
PLAYER_SCALE = 1
PLAYER_START_X = 180
PLAYER_START_Y = 760
CAMERA_LERP = 0.25
DEATH_TIME = 0.1

class PlayerState(Enum):
    """Alle möglichen Player-States."""
    IDLE = "Idle"
    RUN = "Run"
    JUMP = "Jump"
    FALL = "Fall"
    ATTACK = "Attack"
    CROUCH = "Crouch"
    DASH = "Dash"
    ROLL = "Roll"
    HIT = "Hit"
    DEATH = "Death"
    WALL_SLIDE = "WallSlide"
    WALL_CLIMB = "WallClimb"
    SLIDE = "Slide"



# ============================================================================
# GAME CLASS
# ============================================================================

class GameWindow(arcade.Window):

    def __init__(self):
        """Initialisiere das Fenster."""
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        self.player_sprite_list = arcade.SpriteList()

        self.background_color = arcade.color.LIGHT_BLUE

        self.death_time = DEATH_TIME

        self.animations_list = []

        self.wait = 0
       

    
        self.player_sprite = arcade.Sprite(
            hit_box_algorithm=arcade.hitbox.algo_detailed,
            scale=PLAYER_SCALE,
        )
        self.player_sprite.center_x = PLAYER_START_X
        self.player_sprite.center_y = PLAYER_START_Y
        self.player_sprite_list.append(self.player_sprite)
        #============================
        # Music
        #============================

        arcade.load_sound("music.mp3")
        arcade.play_sound(arcade.load_sound("music.mp3"), volume=0.1, loop=True)

        #============================
        # Animationen
        #============================

        self.animation_index = 0
        self.animation_timer = 0.0
        self.animation_frame_duration = 0.08
        self.current_animation_frames = None

        self.animation_frames_attack = [arcade.load_texture(f"FreeKnight_v1_frames/attack/attack_{i}.png") for i in range(0, 4)]
        self.animations_list.append(self.animation_frames_attack)

        self.animation_frames_attack_combo = [arcade.load_texture(f"FreeKnight_v1_frames/attack_combo/attack_combo_{i}.png") for i in range(0, 10)]
        self.animations_list.append(self.animation_frames_attack_combo)

        self.animation_frames_attack2 = [arcade.load_texture(f"FreeKnight_v1_frames/attack2/attack2_{i}.png") for i in range(0, 6)]
        self.animations_list.append(self.animation_frames_attack2)

        self.animation_frames_crouch = [arcade.load_texture(f"FreeKnight_v1_frames/crouch/crouch_{i}.png") for i in range(0, 1)]
        self.animations_list.append(self.animation_frames_crouch)

        self.animation_frames_crouch_attack = [arcade.load_texture(f"FreeKnight_v1_frames/crouch_attack/crouch_attack_{i}.png") for i in range(0, 4)]
        self.animations_list.append(self.animation_frames_crouch_attack)

        self.animation_frames_crouch_walk = [arcade.load_texture(f"FreeKnight_v1_frames/crouch_walk/crouch_walk_{i}.png") for i in range(0, 8)]
        self.animations_list.append(self.animation_frames_crouch_walk)

        self.animation_frames_dash = [arcade.load_texture(f"FreeKnight_v1_frames/dash/dash_{i}.png") for i in range(0, 2)]
        self.animations_list.append(self.animation_frames_dash)

        self.animation_frames_death = [arcade.load_texture(f"FreeKnight_v1_frames/death/death_{i}.png") for i in range(0, 10)]
        self.animations_list.append(self.animation_frames_death)

        self.animation_frames_death_no_movement = [arcade.load_texture(f"FreeKnight_v1_frames/death_no_movement/death_no_movement_{i}.png") for i in range(0, 10)]
        self.animations_list.append(self.animation_frames_death_no_movement)

        self.animation_frames_fall = [arcade.load_texture(f"FreeKnight_v1_frames/fall/fall_{i}.png") for i in range(0, 3)]
        self.animations_list.append(self.animation_frames_fall)

        self.animation_frames_hit = [arcade.load_texture(f"FreeKnight_v1_frames/hit/hit_{i}.png") for i in range(0, 1)]
        self.animations_list.append(self.animation_frames_hit)

        self.animation_frames_idle = [arcade.load_texture(f"FreeKnight_v1_frames/idle/idle_{i}.png") for i in range(0, 10)]
        self.animations_list.append(self.animation_frames_idle)

        self.animation_frames_jump = [arcade.load_texture(f"FreeKnight_v1_frames/jump/jump_{i}.png") for i in range(0, 3)]
        self.animations_list.append(self.animation_frames_jump)

        self.animation_frames_jump_fall_inbetween = [arcade.load_texture(f"FreeKnight_v1_frames/jump_fall_inbetween/jump_fall_inbetween_{i}.png") for i in range(0, 2)]
        self.animations_list.append(self.animation_frames_jump_fall_inbetween)

        self.animation_frames_roll = [arcade.load_texture(f"FreeKnight_v1_frames/roll/roll_{i}.png") for i in range(0, 12)]
        self.animations_list.append(self.animation_frames_roll)

        self.animation_frames_run = [arcade.load_texture(f"FreeKnight_v1_frames/run/run_{i}.png") for i in range(0, 10)]
        self.animations_list.append(self.animation_frames_run)

        self.animation_frames_slide = [arcade.load_texture(f"FreeKnight_v1_frames/slide/slide_{i}.png") for i in range(0, 2)]
        self.animations_list.append(self.animation_frames_slide)

        self.animation_frames_slide_all = [arcade.load_texture(f"FreeKnight_v1_frames/slide_all/slide_all_{i}.png") for i in range(0, 4)]
        self.animations_list.append(self.animation_frames_slide_all)

        self.animation_frames_turn_around = [arcade.load_texture(f"FreeKnight_v1_frames/turn_around/turn_around_{i}.png") for i in range(0, 3)]
        self.animations_list.append(self.animation_frames_turn_around)

        self.animation_frames_wall_climb = [arcade.load_texture(f"FreeKnight_v1_frames/wall_climb/wall_climb_{i}.png") for i in range(0, 7)]
        self.animations_list.append(self.animation_frames_wall_climb)

        self.animation_frames_wall_hang = [arcade.load_texture(f"FreeKnight_v1_frames/wall_hang/wall_hang_{i}.png") for i in range(0, 1)]
        self.animations_list.append(self.animation_frames_wall_hang)

        self.animation_frames_wall_slide = [arcade.load_texture(f"FreeKnight_v1_frames/wall_slide/wall_slide_{i}.png") for i in range(0, 3)]
        self.animations_list.append(self.animation_frames_wall_slide)
        self.current_animation_frames = self.animation_frames_idle


    def setup(self):
        """Setze das Spiel auf."""
        self.tile_map = arcade.load_tilemap(MAP_FILE_PATH, TILE_SCALING)
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        self.simple_physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite, self.scene["Wall"], gravity_constant=0.5)

    
        # Setze die Kamera
        self.camera = arcade.camera.Camera2D()
        # Initialisiere die geglättete Kameraposition zentriert auf den Spieler
        self.camera_x = self.player_sprite.center_x
        self.camera_y = self.player_sprite.center_y 
        self.camera.position = (self.camera_x, self.camera_y)
        self.player_sprite.center_x = PLAYER_START_X
        self.player_sprite.center_y = PLAYER_START_Y
        self.death_time = DEATH_TIME


    def start_random_animation(self):
        if not self.animations_list:
            return

        self.current_animation_frames = random.choice(self.animations_list)
        self.animation_index = 0
        self.animation_timer = 0.0

    def on_key_press(self, key, modifiers):
        """Reagiere auf Tastendruck."""
        if key == arcade.key.ESCAPE:
            self.close()
        if key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 3
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = -3
        if key == arcade.key.UP or key == arcade.key.W or key == arcade.key.SPACE:
            if self.simple_physics_engine.can_jump():
                self.player_sprite.change_y = 12
        if key == arcade.key.DOWN or key == arcade.key.S or key == arcade.key.MOD_SHIFT:
            self.animation_frames_crouch
        if key == arcade.key.G:
            self.start_random_animation()

    def on_key_release(self, key, modifiers):
        """Reagiere auf Loslassen einer Taste."""
        if key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 0
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = 0
        if key == arcade.key.UP or key == arcade.key.W:
            pass
        if key == arcade.key.DOWN or key == arcade.key.S:
            self.player_sprite.change_y = 0
        if key == arcade.key.R:
            self.setup()


    def _update_player_animation(self, delta_time):
        frames = self.current_animation_frames or self.animation_frames_attack
        if not frames:
            return

        self.animation_timer += delta_time
        if self.animation_timer >= self.animation_frame_duration:
            self.animation_timer = 0.0
            self.animation_index = (self.animation_index + 1) % len(frames)

        self.player_sprite.texture = frames[self.animation_index]
        self.player_sprite.scale = PLAYER_SCALE

    def on_update(self, delta_time):
        # Aktualisiere den Spielzustand.
        self._update_player_animation(delta_time)



        # Update physics and player position
        self.simple_physics_engine.update()
        #print(delta_time)

        # Smooth camera follow (linear interpolation)
        target_x = self.player_sprite.center_x
        target_y = self.player_sprite.center_y 
        self.camera_x += (target_x - self.camera_x) * CAMERA_LERP
        self.camera_y += (target_y - self.camera_y) * CAMERA_LERP
        self.camera.position = (self.camera_x, self.camera_y)
        #death check
        self.death = arcade.check_for_collision_with_list(self.player_sprite, self.scene["Death"])
        if self.death:
            self.death_time -= delta_time
        if self.death and self.death_time <= 0:
            self.setup()




    def on_draw(self):
        """Zeichne das Spiel."""
        self.clear()
        self.camera.use()
        self.scene.draw(pixelated=True)
        self.player_sprite_list.draw(pixelated=True)

# ============================================================================
# MAIN
# ============================================================================

def main():
    """Starte das Spiel."""
    app = GameWindow()
    app.setup()
    arcade.run()


if __name__ == "__main__":
    main()