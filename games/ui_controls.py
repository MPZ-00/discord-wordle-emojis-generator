"""UI Control and utility emoji generator."""

from typing import List, Dict
from pathlib import Path
from game import GameGenerator


class UIControlsGenerator(GameGenerator):
    """Generate control and utility icons for Discord UI."""
    
    # Path to icon assets relative to project root
    ASSETS_DIR = Path(__file__).parent.parent / "assets" / "icons"
    
    def get_tiles(self) -> List[Dict[str, str | int]]:
        """Generate tiles for UI controls and utilities.
        
           Includes empty tile state, directional arrows, and interactive emojis.
        
        Returns:
            List of tile specifications for UI controls
        """
        tiles = []
        
        # Empty tile state (dark gray, no icon)
        tiles.append({
            "label": "tile_empty",
            "type": "solid",
            "color": "#31363E",  # Dark gray, matching 2048 empty spaces
            "text": "",
        })
       
           # Directional arrows (rotations of arrow_right)
           tiles.extend([
               {
                   "label": "arrow_up",
                   "type": "icon",
                   "color": "#FFFFFF",
                   "icon": str(self.ASSETS_DIR / "arrow_right.svg"),
                   "rotation": 90,
               },
               {
                   "label": "arrow_right",
                   "type": "icon",
                   "color": "#FFFFFF",
                   "icon": str(self.ASSETS_DIR / "arrow_right.svg"),
                   "rotation": 0,
               },
               {
                   "label": "arrow_down",
                   "type": "icon",
                   "color": "#FFFFFF",
                   "icon": str(self.ASSETS_DIR / "arrow_right.svg"),
                   "rotation": 270,
               },
               {
                   "label": "arrow_left",
                   "type": "icon",
                   "color": "#FFFFFF",
                   "icon": str(self.ASSETS_DIR / "arrow_right.svg"),
                   "rotation": 180,
               },
           ])
       
           # Interactive emojis
           tiles.extend([
               {
                   "label": "video_game",
                   "type": "solid",
                   "color": "#FFFFFF",
                   "text": "🎮",
               },
               {
                   "label": "tada",
                   "type": "icon",
                   "color": "#FFFFFF",
                   "icon": str(self.ASSETS_DIR / "tada.svg"),
                   "rotation": 0,
               },
               {
                   "label": "hourglass",
                   "type": "solid",
                   "color": "#FFFFFF",
                   "text": "⏳",
               },
           ])
        
        return tiles

    def generate(self, out_dir: Path) -> None:
        """Generate all tiles for this game.
        
        Args:
            out_dir: Directory to save PNG files
        """
        from tile_renderer import create_tile, create_icon_tile
        
        out_dir = Path(out_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        
        tiles = self.get_tiles()
        for tile in tiles:
            if tile["type"] == "icon":
                create_icon_tile(
                    label=tile["label"],
                    icon_path=tile["icon"],
                    fill_hex=tile["color"],
                    out_dir=out_dir,
                    tile_size=self.tile_size,
                    rounded=self.rounded,
                    radius=self.radius,
                    border=self.border,
                    rotation=tile.get("rotation", 0),
                )
            else:  # solid tile with text
                create_tile(
                    label=tile["label"],
                    text=tile.get("text", ""),
                    fill_hex=tile["color"],
                    out_dir=out_dir,
                    tile_size=self.tile_size,
                    rounded=self.rounded,
                    radius=self.radius,
                    font_path=self.font_path,
                    border=self.border,
                    shadow=self.shadow,
                )
        
        print(f"Generated {len(tiles)} tiles for {self.__class__.__name__} in: {out_dir.resolve()}")