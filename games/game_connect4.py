"""Connect 4 game emoji generator with theme support."""

from typing import List, Dict
from game import GameGenerator


class Connect4ThemedGenerator(GameGenerator):
    """Generate Connect 4 emoji tiles using theme color palettes.
    
    Supports multiple color themes. All tiles use suffixes based on theme name.
    """
    
    def __init__(self, *args, theme_name: str, theme_colors: dict, **kwargs):
        """Initialize with theme configuration.
        
        Args:
            *args: Passed to parent GameGenerator
            theme_name: Theme identifier (e.g., 'dark', 'light', 'xcad')
            theme_colors: Dict with keys: 'background', 'player1', 'player2', 'foreground'
            **kwargs: Passed to parent GameGenerator
        """
        super().__init__(*args, **kwargs)
        self.theme_name = theme_name
        self.theme_colors = theme_colors
    
    @staticmethod
    def _int_to_hex(color_int: int) -> str:
        """Convert integer color to hex string."""
        return f"#{color_int:06X}"
    
    def get_tiles(self) -> List[Dict[str, str]]:
        """Generate tiles for Connect 4 with theme suffix.
        
        Includes:
        - Empty cell for board spaces
        - Player 1 chip
        - Player 2 chip
        - Column headers (1-7)
        
        All labels include theme suffix (e.g., empty_dark, player1_light)
        
        Returns:
            List of tile specifications
        """
        tiles = []
        suffix = f"_{self.theme_name}"
        
        # Board tiles: empty, player1 chip, player2 chip
        tiles.append({
            "label": f"empty{suffix}",
            "color": self._int_to_hex(self.theme_colors["background"]),
            "text": " ",
        })
        
        tiles.append({
            "label": f"player1{suffix}",
            "color": self._int_to_hex(self.theme_colors["player1"]),
            "text": " ",
        })
        
        tiles.append({
            "label": f"player2{suffix}",
            "color": self._int_to_hex(self.theme_colors["player2"]),
            "text": " ",
        })
        
        # Column headers (1-7)
        for col in range(1, 8):
            tiles.append({
                "label": f"col{col}{suffix}",
                "color": self._int_to_hex(self.theme_colors["foreground"]),
                "text": str(col),
            })
        
        return tiles

