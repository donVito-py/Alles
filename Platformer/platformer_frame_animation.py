import arcade
from enum import Enum
from pathlib import Path

# ============================================================================
# KONSTANTEN
# ============================================================================
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "Platti - Frame-Based Animation"
TILE_SCALING = 1.0
MAP_FILE_PATH = "Platfomer.tmx"

# Pfad zu den Frame-Ordnern
FRAMES_PATH = Path("FreeKnight_v1_frames")  # Output vom extract_gif_frames.py Script

# Movement
MOVE_SPEED = 300
JUMP_FORCE = 400
GRAVITY = 5

# Animation
FRAME_DURATION = 0.1  # Sekunden pro Frame (später per State anpassbar)

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
    ATTACK2 = "attack2"
    ATTACK_COMBO = "attack_combo"
    CROUCH = "crouch"
    CROUCH_ATTACK = "crouch_attack"
    CROUCH_WALK = "crouch_walk"
    DASH = "dash"
    ROLL = "roll"
    HIT = "hit"
    DEATH = "death"
    WALL_SLIDE = "wall_slide"
    WALL_CLIMB = "wall_climb"
    WALL_HANG = "wall_hang"
    SLIDE = "slide"


# ============================================================================
# ANIMATION MANAGER
# ============================================================================

class AnimationSequence:
    """Verwaltet eine Sequenz von Frame-Bildern."""
    
    def __init__(self, frame_dir: Path, state_name: str, duration: float = 0.1):
        """
        Initialisiere eine Animation.
        
        Args:
            frame_dir: Ordner mit den Frame-PNGs
            state_name: Name der Animation (z.B. "idle")
            duration: Sekunden pro Frame
        """
        self.state_name = state_name
        self.duration = duration
        self.frames: list[str] = []
        self.current_frame_idx = 0
        self.frame_timer = 0.0
        
        # Lade alle Frames aus dem Ordner
        self._load_frames(frame_dir / state_name)
    
    def _load_frames(self, frame_dir: Path) -> None:
        """Lade alle PNG-Frames aus einem Ordner."""
        if not frame_dir.exists():
            print(f"⚠️  Frame-Ordner nicht gefunden: {frame_dir}")
            return
        
        # Sammle alle PNG-Dateien (sortiert)
        png_files = sorted(frame_dir.glob(f"{self.state_name}_*.png"))
        
        if not png_files:
            print(f"❌ Keine Frames gefunden in {frame_dir}")
            return
        
        self.frames = [str(f) for f in png_files]
        print(f"✅ {self.state_name}: {len(self.frames)} Frames geladen")
    
    def get_current_frame(self) -> str | None:
        """Gibt den aktuellen Frame zurück."""
        if not self.frames:
            return None
        return self.frames[self.current_frame_idx]
    
    def update(self, delta_time: float) -> None:
        """Update die Animation."""
        if not self.frames or len(self.frames) == 0:
            return
        
        self.frame_timer += delta_time
        
        if self.frame_timer >= self.duration:
            self.frame_timer = 0.0
            self.current_frame_idx = (self.current_frame_idx + 1) % len(self.frames)
    
    def reset(self) -> None:
        """Setze Animation auf Frame 0 zurück."""
        self.current_frame_idx = 0
        self.frame_timer = 0.0


class AnimationManager:
    """Verwaltet alle Animationen des Players."""
    
    def __init__(self, frames_path: Path):
        """Initialisiere alle Animationen."""
        self.animations: dict[PlayerState, AnimationSequence] = {}
        self.frames_path = frames_path
        self._load_animations()
    
    def _load_animations(self) -> None:
        """Lade alle Animation-Sequenzen."""
        animation_configs = {
            PlayerState.IDLE: 0.12,
            PlayerState.RUN: 0.1,
            PlayerState.JUMP: 0.15,
            PlayerState.FALL: 0.15,
            PlayerState.ATTACK: 1.08,
            PlayerState.ATTACK2: 0.08,
            PlayerState.ATTACK_COMBO: 0.08, 
            PlayerState.CROUCH: 0.1,
            PlayerState.CROUCH_ATTACK: 0.08,
            PlayerState.CROUCH_WALK: 0.1,
            PlayerState.DASH: 0.06,
            PlayerState.ROLL: 0.08,
            PlayerState.HIT: 0.12,
            PlayerState.DEATH: 0.15,
            PlayerState.WALL_SLIDE: 0.12,
            PlayerState.WALL_CLIMB: 0.1,
            PlayerState.WALL_HANG: 0.2,
            PlayerState.SLIDE: 0.1,
        }
        
        for state, frame_duration in animation_configs.items():
            anim = AnimationSequence(self.frames_path, state.value, duration=frame_duration)
            self.animations[state] = anim
    
    def get_animation(self, state: PlayerState) -> AnimationSequence | None:
        """Gibt die Animation für einen State zurück."""
        return self.animations.get(state)


# ============================================================================
# PLAYER CLASS MIT STATE MACHINE
# ============================================================================

class Player:
    """Player mit State Machine und Frame-basierter Animation."""
    
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
        self.current_animation = anim_manager.get_animation(PlayerState.IDLE)
        
        # Sprite (wird mit aktuellem Frame aktualisiert)
        self.sprite = arcade.Sprite(
            "tower.png",
            scale=1.5
        )
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
    
    def update_state(self, physics_engine: arcade.PhysicsEnginePlatformer) -> None:
        """Update den State basierend auf Input und Physik."""
        # Überprüfe ob auf Boden
        #grounding_info = physics_engine.check_grounding(self.sprite)
        #self.on_ground = grounding_info.get("is_grounded", False)
        
        # Priorität der States
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
        """Wechsle zu einem neuen State."""
        if self.current_state == new_state:
            return
        
        self.previous_state = self.current_state
        self.current_state = new_state
        
        # Lade neue Animation und reset Frame
        new_animation = self.anim_manager.get_animation(new_state)
        if new_animation and new_animation.frames:
            self.current_animation = new_animation
            self.current_animation.reset()
            
            # Lade ersten Frame
            self._update_sprite_texture()
            
            print(f"→ State: {self.current_state.value}")
    
    def _update_sprite_texture(self) -> None:
        """Aktualisiere das Sprite-Texture mit aktuellem Frame."""
        if not self.current_animation:
            return
        
        frame_path = self.current_animation.get_current_frame()
        if frame_path:
            try:
                # Lade Frame-Bild als Texture
                texture = arcade.load_texture(frame_path)
                self.sprite.texture = texture
            except:
                print(f"⚠️  Konnte nicht laden: {frame_path}")
    
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
                self.velocity_x = 1
        
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
        """Update Player."""
        if self.sprite and self.current_animation:
            self.sprite.velocity_x = self.velocity_x
            self.sprite.velocity_y = self.velocity_y
            self.sprite.update()
            
            # Update Animation
            self.current_animation.update(1/60)  # Annahme: 60 FPS
            self._update_sprite_texture()
            
            self.x = self.sprite.center_x
            self.y = self.sprite.center_y
    
    def reset_actions(self) -> None:
        """Setze einmalige Aktionen zurück."""
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
        self.anim_manager = AnimationManager(FRAMES_PATH)
        
        # === PLAYER ===
        self.player = None
        
        # === MAP & SCENE ===
        self.tile_map = None
        self.scene = None
        
        # === PHYSIK ===
        self.physics_engine = arcade.PhysicsEnginePlatformer
              
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
        
        # Update Player State
        self.player.update_state(self.physics_engine)
        
        # Update Physik
        self.physics_engine.update()
        
        # Update Player (Animation, etc.)
        self.player.update()
        
        # Setze Aktionen zurück
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
