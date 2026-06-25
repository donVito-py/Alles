"""
ANIMATION MANAGER - Erklärte Version
=====================================

Dieser Code verwaltet die Animations-Frames des Players.
Er lädt PNG-Bilder und wechselt zwischen ihnen basierend auf der Zeit.
"""

from pathlib import Path
import arcade

# ============================================================================
# TEIL 1: ANIMATIONSSEQUENZ - Eine einzelne Animation
# ============================================================================

class AnimationSequence:
    """
    Eine einzelne Animation mit mehreren Frames.
    
    Beispiel: Die "idle"-Animation hat 10 Frames (idle_000.png bis idle_009.png)
    Diese Klasse verwaltet:
    - Welche Frames gehören zu dieser Animation?
    - Welcher Frame soll gerade angezeigt werden?
    - Wie schnell wechseln die Frames?
    """
    
    def __init__(self, frame_dir: Path, state_name: str, duration: float = 0.1):
        """
        Initialisiere eine Animation.
        
        Args:
            frame_dir: Ordner wo die Frames liegen (z.B. "FreeKnight_v1_frames")
            state_name: Name der Animation (z.B. "idle", "run", "jump")
            duration: Wie lange ein Frame angezeigt wird (in Sekunden)
                      0.1 = 100ms pro Frame = 10 Frames pro Sekunde
                      0.05 = 50ms pro Frame = 20 Frames pro Sekunde (schneller)
        
        Beispiel:
            anim = AnimationSequence(Path("frames"), "idle", duration=0.12)
            Lädt alle Dateien: frames/idle_000.png, frames/idle_001.png, etc.
        """
        self.state_name = state_name
        self.duration = duration
        
        # Liste mit den Dateiempfaden aller Frames
        # Beispiel: ["frames/idle_000.png", "frames/idle_001.png", ...]
        self.frames: list[str] = []
        
        # Welcher Frame wird gerade gezeigt? (Index in self.frames)
        # Beispiel: 0 = erster Frame, 1 = zweiter Frame, etc.
        self.current_frame_idx = 0
        
        # Timer wie lange der aktuelle Frame schon gezeigt wird
        # Wenn frame_timer >= duration, zum nächsten Frame wechseln
        self.frame_timer = 0.0
        
        # Lade alle Frames aus dem Ordner
        self._load_frames(frame_dir / state_name)
    
    def _load_frames(self, frame_dir: Path) -> None:
        """
        Lade alle PNG-Frames aus einem Ordner.
        
        Der Ordner sollte Dateien wie diese enthalten:
        - idle_000.png
        - idle_001.png
        - idle_002.png
        - etc.
        
        Diese Methode:
        1. Schaut in den Ordner rein
        2. Findet alle PNG-Dateien mit dem Namen "state_name_XXX.png"
        3. Sortiert sie (damit sind sie in der richtigen Reihenfolge: 000, 001, 002...)
        4. Speichert die Dateiempfade in self.frames
        """
        
        # Überprüfe ob der Ordner existiert
        if not frame_dir.exists():
            print(f"⚠️  Ordner nicht gefunden: {frame_dir}")
            return
        
        # Finde alle PNG-Dateien die mit dem State-Namen anfangen
        # z.B. "idle_*.png" für state_name="idle"
        png_files = sorted(frame_dir.glob(f"{self.state_name}_*.png"))
        
        # Wenn keine Dateien gefunden, melde das
        if not png_files:
            print(f"❌ Keine Frames gefunden in {frame_dir}")
            return
        
        # Konvertiere Pfade zu Strings und speichere sie
        self.frames = [str(f) for f in png_files]
        
        # Melde Erfolg in der Konsole
        print(f"✅ {self.state_name}: {len(self.frames)} Frames geladen")
        # Beispiel Output: "✅ idle: 10 Frames geladen"
    
    def get_current_frame(self) -> str | None:
        """
        Gib den Dateiempfad des aktuellen Frames zurück.
        
        Beispiel:
            path = anim.get_current_frame()
            # Ergebnis: "frames/idle_003.png"
        
        Returns:
            Dateiempfad des aktuellen Frames, oder None wenn keine Frames
        """
        
        # Wenn keine Frames geladen wurden, gib None zurück
        if not self.frames:
            return None
        
        # Gib den Frame-Pfad beim aktuellen Index zurück
        return self.frames[self.current_frame_idx]
    
    def update(self, delta_time: float) -> None:
        """
        Update die Animation (wechsle zu nächstem Frame wenn nötig).
        
        Diese Methode wird jeden Frame aufgerufen (z.B. 60x pro Sekunde).
        Sie zählt die Zeit und wechselt zum nächsten Frame wenn die Zeit abgelaufen ist.
        
        Beispiel:
            delta_time = 0.016 (ca. 1/60 Sekunde bei 60 FPS)
            anim.update(0.016)
            # Nach ~6 Aufrufen: 0.016*6 = 0.096 > 0.1, wechsele zu nächstem Frame
        
        Args:
            delta_time: Zeit seit letztem Frame-Update (in Sekunden)
        """
        
        # Wenn keine Frames, mache nichts
        if not self.frames or len(self.frames) == 0:
            return
        
        # Addiere die Zeit hinzu
        self.frame_timer += delta_time
        # Beispiel: Wenn duration=0.1 und wir rufen 6x mit 0.016 auf:
        # frame_timer wird: 0.016, 0.032, 0.048, 0.064, 0.080, 0.096
        # Nach 7x: frame_timer = 0.112 > 0.1 → Zeit abgelaufen!
        
        # Wenn genug Zeit verstrichen ist, wechsele zum nächsten Frame
        if self.frame_timer >= self.duration:
            # Setze Timer zurück
            self.frame_timer = 0.0
            
            # Gehe zum nächsten Frame
            self.current_frame_idx = (self.current_frame_idx + 1) % len(self.frames)
            # Das % len(self.frames) sorgt dafür, dass wir wieder bei 0 anfangen
            # Beispiel: Wenn 10 Frames und idx=9, dann: (9+1) % 10 = 0
    
    def reset(self) -> None:
        """
        Setze die Animation zurück (auf Frame 0).
        
        Beispiel: Wenn ein neuer State anfängt, starten wir wieder bei Frame 0,
        nicht irgendwo in der Mitte.
        """
        self.current_frame_idx = 0
        self.frame_timer = 0.0


# ============================================================================
# TEIL 2: ANIMATION MANAGER - Verwaltet ALLE Animationen
# ============================================================================

class AnimationManager:
    """
    Verwaltet alle Animationen des Players.
    
    Statt einzelne AnimationSequences zu erstellen, macht dieser Manager das:
    - Lädt alle Animationen beim Start
    - Speichert sie in einem Dictionary (schnell zugreifen)
    - Gibt die richtige Animation für jeden State
    
    Beispiel:
        manager = AnimationManager(Path("FreeKnight_v1_frames"))
        idle_anim = manager.get_animation(PlayerState.IDLE)
        idle_anim.update(delta_time)
    """
    
    def __init__(self, frames_path: Path):
        """
        Initialisiere alle Animationen.
        
        Args:
            frames_path: Ordner mit allen State-Ordnern
                        (z.B. "FreeKnight_v1_frames" mit Unterordnern "idle", "run", etc.)
        """
        
        # Dictionary wo alle Animationen gespeichert werden
        # Beispiel: {PlayerState.IDLE: AnimationSequence(...), 
        #            PlayerState.RUN: AnimationSequence(...), ...}
        self.animations: dict = {}
        
        # Speichere den Pfad
        self.frames_path = frames_path
        
        # Lade alle Animationen
        self._load_animations()
    
    def _load_animations(self) -> None:
        """
        Lade alle Animation-Sequenzen und konfiguriere ihr Timing.
        
        Diese Methode:
        1. Definiert für jeden State den Namen und die Frame-Dauer
        2. Erstellt für jeden State eine AnimationSequence
        3. Speichert sie zum späteren Zugriff
        
        Das Timing kann man hier anpassen:
        - 0.06 = sehr schnell (Dash)
        - 0.10 = normal (Run)
        - 0.15 = langsam (Idle)
        """
        
        # Konfiguration: Welcher State, wie schnell?
        # Das ist wie eine Rezept-Liste: "Für Idle: 0.12 Sekunden pro Frame"
        animation_configs = {
            "idle": 0.12,              # Langsam (gemütlich stehen)
            "run": 0.10,               # Normal (laufen)
            "jump": 0.15,              # Langsam (Sprung sollte dramatisch sein)
            "fall": 0.15,              # Langsam
            "attack": 0.08,            # Schnell (schneller Angriff)
            "attack2": 0.08,           # Schnell
            "attack_combo": 0.08,      # Schnell
            "crouch": 0.10,            # Normal
            "crouch_attack": 0.08,     # Schnell
            "crouch_walk": 0.10,       # Normal
            "dash": 0.06,              # SEHR SCHNELL (schneller Dash)
            "roll": 0.08,              # Schnell
            "hit": 0.12,               # Langsam (Treffer-Animation)
            "death": 0.15,             # Langsam (dramatisch)
            "wall_slide": 0.12,        # Langsam
            "wall_climb": 0.10,        # Normal
            "wall_hang": 0.20,         # SEHR LANGSAM (hängt gemütlich)
            "slide": 0.10,             # Normal
        }
        
        # Durchlaufe alle Konfigurationen
        for state_name, frame_duration in animation_configs.items():
            # Erstelle eine neue AnimationSequence für diesen State
            anim = AnimationSequence(
                self.frames_path,      # Wo sind die Frames?
                state_name,            # Welcher State? (z.B. "idle")
                duration=frame_duration  # Wie schnell? (z.B. 0.12 Sekunden)
            )
            
            # Speichere diese Animation für später
            self.animations[state_name] = anim
            # Beispiel: animations["idle"] = AnimationSequence(...)
    
    def get_animation(self, state_name: str) -> AnimationSequence | None:
        """
        Gib die Animation für einen State zurück.
        
        Beispiel:
            anim = manager.get_animation("idle")
            # Ergebnis: Die AnimationSequence für idle
        
        Args:
            state_name: Name des States (z.B. "idle", "run", "attack")
        
        Returns:
            Die AnimationSequence für diesen State, oder None wenn nicht gefunden
        """
        
        # Schau im Dictionary nach
        return self.animations.get(state_name)
        # Wenn nicht vorhanden, gib None zurück


# ============================================================================
# BEISPIEL: WIE MAN DAS BENUTZT
# ============================================================================

def example_usage():
    """
    So würde man den AnimationManager in der Praxis benutzen:
    """
    
    # 1. Manager erstellen (lädt alle Animationen)
    manager = AnimationManager(Path("FreeKnight_v1_frames"))
    
    # 2. Spezifische Animation holen
    idle_animation = manager.get_animation("idle")
    run_animation = manager.get_animation("run")
    
    # 3. In der Game Loop: Update die Animation
    for frame in range(600):  # 10 Sekunden bei 60 FPS
        # Simuliere: wir sind gerade im "idle" State
        delta_time = 1/60  # ~16ms pro Frame
        idle_animation.update(delta_time)
        
        # Hole den aktuellen Frame-Pfad
        current_frame = idle_animation.get_current_frame()
        print(f"Frame {frame}: {current_frame}")
        
        # Lade das Bild und zeige es (Pseudo-Code):
        # texture = arcade.load_texture(current_frame)
        # sprite.texture = texture
    
    # 4. Wenn der State wechselt (z.B. zu "run"):
    run_animation.reset()  # Starte von vorne
    
    # 5. Weiter mit der neuen Animation
    for frame in range(300):
        delta_time = 1/60
        run_animation.update(delta_time)
        current_frame = run_animation.get_current_frame()
        print(f"Running: {current_frame}")


# ============================================================================
# ZUSAMMENFASSUNG
# ============================================================================

"""
FLUSSDIAGRAMM:

┌─────────────────────────────────────┐
│   AnimationManager.__init__()        │
│   (Lädt alle Animationen beim Start) │
└────────────┬────────────────────────┘
             │
             ├─→ idle: AnimationSequence (10 Frames)
             ├─→ run: AnimationSequence (8 Frames)
             ├─→ jump: AnimationSequence (5 Frames)
             ├─→ attack: AnimationSequence (12 Frames)
             └─→ ... etc

IN JEDEM GAME FRAME:
┌──────────────────────────────────────┐
│  player.update(delta_time)           │
└────────────┬─────────────────────────┘
             │
             ├─→ current_anim.update(delta_time)
             │       │
             │       └─→ frame_timer += delta_time
             │       └─→ Wenn frame_timer >= duration:
             │           • Wechsle zum nächsten Frame
             │           • Setze Timer zurück
             │
             └─→ current_frame = current_anim.get_current_frame()
                 └─→ Lade das Bild


TIMING-BEISPIEL (Idle mit 0.12s pro Frame):
┌─────────────────────────────────┐
│ Frame 0  │ Frame 1  │ Frame 2   │
│ Time: 0s │ Time: 0.12s │ Time: 0.24s │
│ idle_000.png │ idle_001.png │ idle_002.png │
└─────────────────────────────────┘
  ^
  └─ Das wechselt automatisch wenn frame_timer >= 0.12
"""
