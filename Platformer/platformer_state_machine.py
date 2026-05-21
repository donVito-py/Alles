import arcade
from enum import Enum
from pathlib import Path

# ============================================================================
# KONSTANTEN
# ============================================================================
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "Platti - State Machine"
TILE_SCALING = 1.0
MAP_FILE_PATH = "Platfomer.tmx"

# Pfad zu den GIFs
ANIMATIONS_PATH = Path("FreeKnight_v1/11")  # oder wo deine GIFs sind

# Movement
MOVE_SPEED = 300
JUMP_FORCE = 400
GRAVITY = 0.5

# ============================================================================
# ENUMS
# ============================================================================

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
# ANIMATION MANAGER
# ============================================================================

class AnimationManager:
    """Verwaltet alle Animationen des Players."""
    
    def __init__(self, anim_path: Path):
        """Initialisiere alle Animationen."""
        self.animations = {}
        self.anim_path = anim_path
        self._load_animations()
    
    def _load_animations(self) -> None:
        """Lade alle GIF-Animationen."""
        animation_files = {
            PlayerState.IDLE: "__Idle.gif",
            PlayerState.RUN: "__Run.gif",
            PlayerState.JUMP: "__Jump.gif",
            PlayerState.FALL: "__Fall.gif",
            PlayerState.ATTACK: "__Attack.gif",
            PlayerState.CROUCH: "__Crouch.gif",
            PlayerState.DASH: "__Dash.gif",
            PlayerState.ROLL: "__Roll.gif",
            PlayerState.HIT: "__Hit.gif",
            PlayerState.DEATH: "__Death.gif",
            PlayerState.WALL_SLIDE: "__WallSlide.gif",
            PlayerState.WALL_CLIMB: "__WallClimb.gif",
            PlayerState.SLIDE: "__Slide.gif",
        }
        
        for state, filename in animation_files.items():
            filepath = self.anim_path / filename
            try:
                sprite = arcade.load_animated_gif(str(filepath))
                sprite.scale = 1.5  # ← Scale NACH dem Laden setzen
                self.animations[state] = sprite
                print(f"✅ Geladen: {state.value}")
            except (FileNotFoundError, TypeError) as e:
                print(f"⚠️  FEHLER beim Laden von {filename}: {e}")
                # Fallback: statisches Sprite
                try:
                    sprite = arcade.Sprite(str(filepath), scale=1.5)
                    self.animations[state] = sprite
                except:
                    print(f"❌ Fallback auch fehlgeschlagen für {filename}")
                    self.animations[state] = None
    
    def get_animation(self, state: PlayerState) -> arcade.Sprite | None:
        """Gibt das Sprite für einen State zurück."""
        return self.animations.get(state)


# ============================================================================
# PLAYER CLASS MIT STATE MACHINE
# ============================================================================

class Player:
    """Player mit State Machine und Animation Management."""
    
    def __init__(self, x: float, y: float, anim_manager: AnimationManager):
        """Initialisiere den Player."""
        self.x = x
        self.y = y
        self.velocity_x = 0.0
        self.velocity_y = 0.0
        
        # State Management
        self.current_state = PlayerState.IDLE
        self.previous_state = None
        self.anim_manager = anim_manager
        self.sprite = anim_manager.get_animation(PlayerState.IDLE)
        
        if self.sprite:
            self.sprite.center_x = x
            self.sprite.center_y = y
        
        # Input
        self.is_moving_left = False
        self.is_moving_right = False
        self.is_attacking = False
        self.is_dashing = False
        self.is_crouching = False
        
        # Physik
        self.on_ground = False
        self.is_wall_sliding = False
    
    def update_state(self, physics_engine: arcade.PhysicsEnginePlatformer) -> None:
        """Update den State basierend auf Input und Physik."""
        self.on_ground = physics_engine.is_on_ground(self.sprite)
        
        # Priorität der States (von hoch zu niedrig)
        if self.is_attacking:
            self._set_state(PlayerState.ATTACK)
        elif self.is_dashing:
            self._set_state(PlayerState.DASH)
        elif self.is_crouching:
            self._set_state(PlayerState.CROUCH)
        elif not self.on_ground and self.velocity_y > 0:
            self._set_state(PlayerState.JUMP)
        elif not self.on_ground and self.velocity_y <= 0:
            self._set_state(PlayerState.FALL)
        elif self.is_moving_left or self.is_moving_right:
            self._set_state(PlayerState.RUN)
        else:
            self._set_state(PlayerState.IDLE)
    
    def _set_state(self, new_state: PlayerState) -> None:
        """Wechsle zu einem neuen State und lade die Animation."""
        if self.current_state == new_state:
            return  # Kein Wechsel nötig
        
        self.previous_state = self.current_state
        self.current_state = new_state
        
        # Lade neue Animation
        new_sprite = self.anim_manager.get_animation(new_state)
        if new_sprite:
            # Erhalt Position und Bewegung
            old_x = self.sprite.center_x if self.sprite else self.x
            old_y = self.sprite.center_y if self.sprite else self.y
            
            self.sprite = new_sprite
            self.sprite.center_x = old_x
            self.sprite.center_y = old_y
            self.sprite.velocity_x = self.velocity_x
            self.sprite.velocity_y = self.velocity_y
            
            print(f"→ State: {self.current_state.value}")
    
    def handle_input(self, key: int, pressed: bool) -> None:
        """Handle Tastatureingaben."""
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.is_moving_left = pressed
            if pressed:
                self.velocity_x = -MOVE_SPEED
            elif not self.is_moving_right:
                self.velocity_x = 0
        
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.is_moving_right = pressed
            if pressed:
                self.velocity_x = MOVE_SPEED
            elif not self.is_moving_left:
                self.velocity_x = 0
        
        elif key == arcade.key.SPACE and pressed:
            if self.on_ground:
                self.velocity_y = JUMP_FORCE
        
        elif (key == arcade.key.C or key == arcade.key.LCTRL) and pressed:
            self.is_crouching = not self.is_crouching
        
        elif (key == arcade.key.Z or key == arcade.key.LSHIFT) and pressed:
            self.is_dashing = True
        
        elif key == arcade.key.X and pressed:
            self.is_attacking = True
    
    def update(self) -> None:
        """Update Player (Position, Animation, etc.)."""
        if self.sprite:
            self.sprite.velocity_x = self.velocity_x
            self.sprite.velocity_y = self.velocity_y
            self.sprite.update()
            
            self.x = self.sprite.center_x
            self.y = self.sprite.center_y
    
    def reset_actions(self) -> None:
        """Setze einmalige Aktionen zurück (Attack, Dash)."""
        self.is_attacking = False
        self.is_dashing = False


# ============================================================================
# GAME WINDOW
# ============================================================================

class GameWindow(arcade.Window):
    def __init__(self):
        """Initialisiere das Fenster."""
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        
        self.background_color = arcade.color.LIGHT_BLUE
        
        # === ANIMATION MANAGER ===
        self.anim_manager = AnimationManager(ANIMATIONS_PATH)
        
        # === PLAYER ===
        self.player = None
        
        # === MAP & SCENE ===
        self.tile_map = None
        self.scene = None
        
        # === PHYSIK ===
        self.physics_engine = None
        
        # === KAMERA ===
        self.camera = arcade.Camera2D()

    def setup(self) -> None:
        """Setze das Spiel auf."""
        
        # === MAP LADEN ===
        try:
            self.tile_map = arcade.load_tilemap(MAP_FILE_PATH, TILE_SCALING)
            self.scene = arcade.Scene.from_tilemap(self.tile_map)
        except FileNotFoundError:
            print(f"❌ Map nicht gefunden: {MAP_FILE_PATH}")
            self.scene = arcade.Scene()
            return
        
        # === PLAYER ERSTELLEN ===
        self.player = Player(180, 770, self.anim_manager)
        
        if "Player" not in self.scene:
            self.scene.add_sprite_list("Player")
        self.scene.add_sprite("Player", self.player.sprite)
        
        # === PHYSIK ENGINE ===
        walls_layer = None
        if "Wall" in self.scene:
            walls_layer = self.scene["Wall"]
        elif "Platforms" in self.scene:
            walls_layer = self.scene["Platforms"]
        
        if walls_layer:
            self.physics_engine = arcade.PhysicsEnginePlatformer(
                self.player.sprite,
                walls=walls_layer,
                gravity_constant=GRAVITY
            )
        else:
            self.physics_engine = arcade.PhysicsEnginePlatformer(
                self.player.sprite,
                gravity_constant=GRAVITY
            )

    def on_key_press(self, key: int, modifiers: int) -> None:
        """Tastendruck."""
        if key == arcade.key.ESCAPE:
            self.close()
        
        if self.player:
            self.player.handle_input(key, pressed=True)

    def on_key_release(self, key: int, modifiers: int) -> None:
        """Taste losgelassen."""
        if self.player:
            self.player.handle_input(key, pressed=False)

    def on_update(self, delta_time: float) -> None:
        """Update-Loop."""
        if not self.physics_engine or not self.player:
            return
        
        # Update Player State basierend auf Physik + Input
        self.player.update_state(self.physics_engine)
        
        # Update Physik
        self.physics_engine.update()
        
        # Update Player (Animation, etc.)
        self.player.update()
        
        # Setze einmalige Aktionen zurück
        self.player.reset_actions()
        
        # Kamera folgt
        self.camera.position = (self.player.x, self.player.y)

    def on_draw(self) -> None:
        """Zeichne das Spiel."""
        self.clear()
        self.camera.use()
        
        if self.scene:
            self.scene.draw(pixelated=True)
        
        # Debug Info
        arcade.draw_text(
            f"State: {self.player.current_state.value if self.player else 'N/A'}",
            10, SCREEN_HEIGHT - 30,
            arcade.color.WHITE, 14
        )
        arcade.draw_text(
            f"FPS: {arcade.get_fps():.0f}",
            10, SCREEN_HEIGHT - 50,
            arcade.color.WHITE, 14
        )


# ============================================================================
# MAIN
# ============================================================================

def main() -> None:
    """Starte das Spiel."""
    app = GameWindow()
    app.setup()
    arcade.run()


if __name__ == "__main__":
    main()
