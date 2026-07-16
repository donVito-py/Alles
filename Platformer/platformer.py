import arcade
import random
from enum import Enum

# ============================================================================
# KONSTANTEN - Screen
# ============================================================================

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "Platti"

# ============================================================================
# KONSTANTEN - Game
# ============================================================================

TILE_SCALING = 1.0
MAP_FILE_PATH = "Platfomer.tmx"

# ============================================================================
# KONSTANTEN - Player
# ============================================================================

PLAYER_SCALE = 1
PLAYER_START_X = 180
PLAYER_START_Y = 2650

# ============================================================================
# KONSTANTEN - Physics
# ============================================================================

GRAVITY_CONSTANT = 0.5
JUMP_SPEED = 12
WALK_SPEED = 4
COYOTE_TIME = 0.15  # Sekunden Verzögerung nach dem Verlassen des Bodens zum Springen
CAMERA_LERP = 0.25  # Kamera-Glättung (0-1)

# ============================================================================
# KONSTANTEN - Animation
# ============================================================================

ANIMATION_FRAME_DURATION = 0.08  # Sekunden pro Frame
DEATH_TIME = 0.1

# ============================================================================
# KONSTANTEN - Audio
# ============================================================================

MUSIC_FILE = "music.mp3"
MUSIC_VOLUME = 0.1


# ============================================================================
# ENUMS
# ============================================================================

class PlayerState(Enum):
    """Alle möglichen Player-States."""

    IDLE = "idle"
    RUN = "run"
    JUMP = "jump"
    FALL = "fall"
    ATTACK = "attack"
    ATTACK_COMBO = "attack_combo"
    ATTACK2 = "attack2"
    CROUCH = "crouch"
    CROUCH_ATTACK = "crouch_attack"
    CROUCH_WALK = "crouch_walk"
    DASH = "dash"
    DEATH = "death"
    DEATH_NO_MOVEMENT = "death_no_movement"
    HIT = "hit"
    ROLL = "roll"
    SLIDE = "slide"
    SLIDE_ALL = "slide_all"
    TURN_AROUND = "turn_around"
    WALL_CLIMB = "wall_climb"
    WALL_HANG = "wall_hang"
    WALL_SLIDE = "wall_slide"


# ============================================================================
# ANIMATION LOADER
# ============================================================================

class AnimationLoader:
    """Lädt und verwaltet alle Animationen für den Spieler."""

    # Mapping von State zu Animationen-Verzeichnis und Frame-Anzahl
    ANIMATION_DATA = {
        PlayerState.ATTACK: ("attack", 4),
        PlayerState.ATTACK_COMBO: ("attack_combo", 10),
        PlayerState.ATTACK2: ("attack2", 6),
        PlayerState.CROUCH: ("crouch", 1),
        PlayerState.CROUCH_ATTACK: ("crouch_attack", 4),
        PlayerState.CROUCH_WALK: ("crouch_walk", 8),
        PlayerState.DASH: ("dash", 2),
        PlayerState.DEATH: ("death", 10),
        PlayerState.DEATH_NO_MOVEMENT: ("death_no_movement", 10),
        PlayerState.FALL: ("fall", 3),
        PlayerState.HIT: ("hit", 1),
        PlayerState.IDLE: ("idle", 10),
        PlayerState.JUMP: ("jump", 3),
        PlayerState.ROLL: ("roll", 12),
        PlayerState.RUN: ("run", 10),
        PlayerState.SLIDE: ("slide", 2),
        PlayerState.SLIDE_ALL: ("slide_all", 4),
        PlayerState.TURN_AROUND: ("turn_around", 3),
        PlayerState.WALL_CLIMB: ("wall_climb", 7),
        PlayerState.WALL_HANG: ("wall_hang", 1),
        PlayerState.WALL_SLIDE: ("wall_slide", 3),
    }

    @classmethod
    def load_animation(cls, state: PlayerState) -> list:
        """Lade alle Frames für einen bestimmten Animation-State.
        
        Args:
            state: Der PlayerState für die Animation
            
        Returns:
            Liste von arcade.Texture Objekten
        """
        if state not in cls.ANIMATION_DATA:
            return cls.load_animation(PlayerState.IDLE)  # Fallback

        directory, frame_count = cls.ANIMATION_DATA[state]
        frames = []
        for i in range(frame_count):
            path = f"FreeKnight_v1_frames/{directory}/{directory}_{i}.png"
            try:
                frames.append(arcade.load_texture(path))
            except:
                print(f"Warnung: Konnte Texture nicht laden: {path}")
        return frames if frames else cls.load_animation(PlayerState.IDLE)

    @classmethod
    def load_all_animations(cls) -> dict:
        """Lade alle verfügbaren Animationen.
        
        Returns:
            Dictionary mit State -> Frame-Liste Mappings
        """
        animations = {}
        for state in PlayerState:
            animations[state] = cls.load_animation(state)
        return animations


# ============================================================================
# GAME WINDOW
# ============================================================================

class GameWindow(arcade.Window):
    """Hauptfenster für das Platformer-Spiel."""

    def __init__(self):
        """Initialisiere das Fenster und alle Spielkomponenten."""
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # Grafik-Setup
        self.background_color = arcade.color.LIGHT_BLUE

        # Player Setup
        self.player_sprite_list = arcade.SpriteList()
        self.player_sprite = self._create_player_sprite()
        self.player_sprite_list.append(self.player_sprite)

        # Animation Setup
        self.animations = AnimationLoader.load_all_animations()
        self.current_animation_frames = self.animations[PlayerState.IDLE]
        self.animation_index = 0
        self.animation_timer = 0.0

        # Player State Setup
        self.current_state = PlayerState.IDLE
        self.jump_key_pressed = False
        self.facing_right = True
        self.coyote_counter = 0.0

        # Camera & Physics (werden in setup() initialisiert)
        self.camera = None
        self.camera_x = 0.0
        self.camera_y = 0.0
        self.simple_physics_engine = None
        self.scene = None

        # Game State
        self.death_time = DEATH_TIME
        self.fps_counter = 0.0

        # Audio
        self._load_music()

    def _create_player_sprite(self) -> arcade.Sprite:
        """Erstelle und initialisiere den Player Sprite."""
        sprite = arcade.Sprite(
            hit_box_algorithm=arcade.hitbox.algo_detailed,
            scale=PLAYER_SCALE,
        )
        sprite.center_x = PLAYER_START_X
        sprite.center_y = PLAYER_START_Y
        return sprite

    def _load_music(self):
        """Lade und spiele die Hintergrundmusik."""
        try:
            arcade.load_sound(MUSIC_FILE)
            arcade.play_sound(arcade.load_sound(MUSIC_FILE), volume=MUSIC_VOLUME, loop=True)
        except:
            print(f"Warnung: Konnte Musik nicht laden: {MUSIC_FILE}")

    def setup(self):
        """Initialisiere das Spiel (wird am Anfang und nach Tod aufgerufen)."""
        # Tilemap laden
        self.tile_map = arcade.load_tilemap(MAP_FILE_PATH, TILE_SCALING)
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        # Player zurücksetzen
        self.player_sprite.center_x = PLAYER_START_X
        self.player_sprite.center_y = PLAYER_START_Y
        self.player_sprite.change_x = 0
        self.player_sprite.change_y = 0

        # Physics Engine
        self.simple_physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite,
            self.scene["Wall"],
            gravity_constant=GRAVITY_CONSTANT
        )

        # Kamera initialisieren
        self.camera = arcade.camera.Camera2D()
        self.camera_x = self.player_sprite.center_x
        self.camera_y = self.player_sprite.center_y
        self.camera.position = (self.camera_x, self.camera_y)

        # Game State zurücksetzen
        self.death_time = DEATH_TIME
        self.current_state = PlayerState.IDLE
        self.jump_key_pressed = False
        self.coyote_counter = 0.0

    # ========================================================================
    # INPUT HANDLING
    # ========================================================================

    def on_key_press(self, key: int, modifiers: int):
        """Reagiere auf Tastendruck."""
        # Spiel beenden
        if key == arcade.key.ESCAPE:
            self.close()

        # Bewegung nach rechts
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = WALK_SPEED
            self.facing_right = True

        # Bewegung nach links
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = -WALK_SPEED
            self.facing_right = False

        # Springen
        elif key == arcade.key.UP or key == arcade.key.W or key == arcade.key.SPACE:
            if not self.jump_key_pressed and (self.simple_physics_engine.can_jump() or self.coyote_counter > 0):
                self.player_sprite.change_y = JUMP_SPEED
                self.jump_key_pressed = True
                self.coyote_counter = 0.0

        # Zufällige Animation (Debug)
        elif key == arcade.key.G:
            self._start_random_animation()

        # FPS Anzeige (Debug)
        elif key == ord('1'):
            print(f"FPS: {self.fps_counter:.1f}")

        # Neustart (Debug)
        elif key == arcade.key.R:
            self.setup()

    def on_key_release(self, key: int, modifiers: int):
        """Reagiere auf Loslassen einer Taste."""
        # Stoppe Bewegung nach rechts
        if key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 0

        # Stoppe Bewegung nach links
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = 0

        # Stoppe Sprung
        elif key == arcade.key.UP or key == arcade.key.W or key == arcade.key.SPACE:
            self.jump_key_pressed = False

    # ========================================================================
    # ANIMATION MANAGEMENT
    # ========================================================================

    def _start_random_animation(self):
        """Starte eine zufällige Animation (für Debug)."""
        random_state = random.choice(list(PlayerState))
        self.current_animation_frames = self.animations[random_state]
        self.animation_index = 0
        self.animation_timer = 0.0

    def _set_animation_for_state(self, state: PlayerState):
        """Setze die Animation für einen bestimmten State.
        
        Args:
            state: Der neue PlayerState
        """
        self.current_animation_frames = self.animations.get(state, self.animations[PlayerState.IDLE])
        self.animation_index = 0
        self.animation_timer = 0.0

    def _update_player_animation(self, delta_time: float):
        """Update die aktuelle Animation.
        
        Args:
            delta_time: Zeit seit letztem Frame in Sekunden
        """
        frames = self.current_animation_frames or self.animations[PlayerState.IDLE]
        if not frames:
            return

        # Erhöhe Timer
        self.animation_timer += delta_time

        # Wechsle zum nächsten Frame wenn Zeit abgelaufen
        if self.animation_timer >= ANIMATION_FRAME_DURATION:
            self.animation_timer = 0.0
            self.animation_index = (self.animation_index + 1) % len(frames)

        # Setze neue Texture
        self.player_sprite.texture = frames[self.animation_index]
        self.player_sprite.scale = PLAYER_SCALE

        # Spiegle basierend auf Blickrichtung
        if self.facing_right:
            self.player_sprite.scale_x = abs(self.player_sprite.scale_x)
        else:
            self.player_sprite.scale_x = -abs(self.player_sprite.scale_x)

    # ========================================================================
    # GAME LOGIC
    # ========================================================================

    def _update_player_state(self):
        """Update den Player State basierend auf Physik und Eingabe."""
        is_on_ground = self.simple_physics_engine.can_jump()
        is_moving = abs(self.player_sprite.change_x) > 0

        # Bestimme neuen State
        if not is_on_ground:
            new_state = PlayerState.JUMP if self.player_sprite.change_y > 0 else PlayerState.FALL
        elif is_moving:
            new_state = PlayerState.RUN
        else:
            new_state = PlayerState.IDLE

        # Wechsle Animation wenn State sich geändert hat
        if new_state != self.current_state:
            self.current_state = new_state
            self._set_animation_for_state(new_state)

    def _update_coyote_time(self, delta_time: float):
        """Update die Coyote Time (Sprung-Verzögerung nach Plattform).
        
        Args:
            delta_time: Zeit seit letztem Frame in Sekunden
        """
        if self.simple_physics_engine.can_jump():
            self.coyote_counter = COYOTE_TIME
        else:
            self.coyote_counter -= delta_time

    def _update_camera(self):
        """Update die Kamera Position (smooth follow)."""
        target_x = self.player_sprite.center_x
        target_y = self.player_sprite.center_y

        # Linear interpolation
        self.camera_x += (target_x - self.camera_x) * CAMERA_LERP
        self.camera_y += (target_y - self.camera_y) * CAMERA_LERP
        self.camera.position = (self.camera_x, self.camera_y)

    def _check_death(self, delta_time: float):
        """Überprüfe ob der Player in der Tod-Zone ist.
        
        Args:
            delta_time: Zeit seit letztem Frame in Sekunden
        """
        death_collisions = arcade.check_for_collision_with_list(
            self.player_sprite,
            self.scene["Death"]
        )

        if death_collisions:
            self.death_time -= delta_time
            if self.death_time <= 0:
                self.setup()

    def on_update(self, delta_time: float):
        """Update die Game Logic.
        
        Args:
            delta_time: Zeit seit letztem Frame in Sekunden
        """
        # Berechne FPS
        if delta_time > 0:
            self.fps_counter = 1.0 / delta_time

        # Update Gameplay
        self._update_player_state()
        self._update_player_animation(delta_time)
        self._update_coyote_time(delta_time)

        # Reset Jump Flag wenn am Boden
        if self.simple_physics_engine.can_jump():
            self.jump_key_pressed = False

        # Physics
        self.simple_physics_engine.update()

        # Camera und World
        self._update_camera()
        self._check_death(delta_time)

    # ========================================================================
    # RENDERING
    # ========================================================================

    def on_draw(self):
        """Zeichne den Frame."""
        self.clear()

        with self.camera.activate():
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
