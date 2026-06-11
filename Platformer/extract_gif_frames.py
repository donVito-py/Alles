"""
GIF Frame Extractor für Arcade Platformer
Zerlegt alle GIFs in einzelne PNG-Frames und organisiert sie in Ordnern.
"""

from PIL import Image
from pathlib import Path
import sys

# ============================================================================
# KONFIGURATION
# ============================================================================

INPUT_DIR = Path("FreeKnight_v1/11")  # Wo deine GIFs liegen
OUTPUT_DIR = Path("FreeKnight_v1_frames")  # Wo die PNGs hingehen

# Mapping: GIF-Datei → State-Name (für Ordner)
GIF_MAPPING = {
    "__Idle.gif": "idle",
    "__Run.gif": "run",
    "__Jump.gif": "jump",
    "__Fall.gif": "fall",
    "__Attack.gif": "attack",
    "__Attack2.gif": "attack2",
    "__AttackCombo2hit.gif": "attack_combo",
    "__CrouchAttack.gif": "crouch_attack",
    "__Crouch.gif": "crouch",
    "__CrouchWalk.gif": "crouch_walk",
    "__Dash.gif": "dash",
    "__Roll.gif": "roll",
    "__Slide.gif": "slide",
    "__SlideAll.gif": "slide_all",
    "__Hit.gif": "hit",
    "__Death.gif": "death",
    "__DeathNoMovement.gif": "death_no_movement",
    "__WallSlide.gif": "wall_slide",
    "__WallClimb.gif": "wall_climb",
    "__WallHang.gif": "wall_hang",
    "__TurnAround.gif": "turn_around",
    "__Fall.gif": "fall",
    "__JumpFallInbetween.gif": "jump_fall_inbetween",
}


# ============================================================================
# FUNKTIONEN
# ============================================================================

def extract_gif_frames(gif_path: Path, output_folder: Path, state_name: str) -> int:
    """
    Zerlege ein GIF in einzelne PNG-Frames.
    
    Args:
        gif_path: Pfad zur GIF-Datei
        output_folder: Ordner wo PNGs gespeichert werden
        state_name: Name für die Frames (z.B. "idle")
    
    Returns:
        Anzahl der extrahierten Frames
    """
    try:
        img = Image.open(gif_path)
    except FileNotFoundError:
        print(f"❌ Nicht gefunden: {gif_path}")
        return 0
    
    frame_count = 0
    
    try:
        # Durchlaufe alle Frames im GIF
        for frame_idx in range(img.n_frames):
            img.seek(frame_idx)
            
            # Konvertiere zu RGBA (falls nötig)
            frame = img.convert("RGBA")
            
            # Speichere als PNG
            output_filename = f"{state_name}_{frame_idx:03d}.png"
            output_path = output_folder / output_filename
            frame.save(output_path, "PNG")
            
            frame_count += 1
            print(f"  ✅ Frame {frame_idx}: {output_filename}")
    
    except EOFError:
        # Manche GIFs haben ein EOFError bei letztem Frame
        pass
    
    return frame_count


def main():
    """Hauptprogramm."""
    
    # Überprüfe ob Input-Dir existiert
    if not INPUT_DIR.exists():
        print(f"❌ Input-Ordner nicht gefunden: {INPUT_DIR}")
        sys.exit(1)
    
    # Erstelle Output-Dir
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    print(f"📁 Output-Ordner: {OUTPUT_DIR}\n")
    
    # Zähler
    total_gifs = 0
    total_frames = 0
    
    # Durchlaufe alle GIFs
    for gif_filename, state_name in sorted(GIF_MAPPING.items()):
        gif_path = INPUT_DIR / gif_filename
        
        # Überspringe wenn nicht existiert
        if not gif_path.exists():
            print(f"⏭️  Übersprungen (nicht gefunden): {gif_filename}")
            continue
        
        # Erstelle State-Ordner
        state_folder = OUTPUT_DIR / state_name
        state_folder.mkdir(parents=True, exist_ok=True)
        
        print(f"\n📷 Verarbeite: {gif_filename} → {state_name}/")
        
        # Zerlege GIF
        frame_count = extract_gif_frames(gif_path, state_folder, state_name)
        
        if frame_count == 0:
            print(f"⚠️  Keine Frames gefunden in {gif_filename}")
        else:
            print(f"✅ {frame_count} Frames extrahiert")
            total_gifs += 1
            total_frames += frame_count
    
    print("\n" + "="*60)
    print(f"✅ FERTIG!")
    print(f"   GIFs verarbeitet: {total_gifs}")
    print(f"   Frames erstellt: {total_frames}")
    print(f"   Output-Ordner: {OUTPUT_DIR}")
    print("="*60)


if __name__ == "__main__":
    main()
