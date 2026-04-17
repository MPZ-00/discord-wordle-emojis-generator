"""Connect 4 game emoji generator with theme support."""

from typing import List, Dict
from game import GameGenerator


class Connect4ThemedGenerator(GameGenerator):
    """Generate Connect 4 emoji tiles using theme color palettes.
    
    Supports multiple color themes. Pieces are rounded style.
    Column headers use themed backgrounds.
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
        """Generate rounded tiles for Connect 4 with theme suffix.
        
        Includes:
        - Empty, player1, player2 (rounded style per theme)
        - Column headers (themed background, no shadow)
        
        Returns:
            List of tile specifications
        """
        tiles = []
        suffix = f"_{self.theme_name}"
        
        # Game pieces (filled, rounded appearance)
        for piece in ["empty", "player1", "player2"]:
            tiles.append({
                "label": f"{piece}{suffix}",
                "color": self._int_to_hex(self.theme_colors["background" if piece == "empty" else piece]),
                "text": " ",
                "style": "round",
            })
        
        # Column headers with themed background
        for col in range(1, 8):
            tiles.append({
                "label": f"col{col}{suffix}",
                "color": self._int_to_hex(self.theme_colors["background"]),
                "text": str(col),
                "style": "header",
            })
        
        return tiles



