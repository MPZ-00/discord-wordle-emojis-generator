"""2048 game emoji generator."""

from typing import List, Dict
from game import GameGenerator


class Game2048Generator(GameGenerator):
    """Generate 2048 game emoji tiles (powers of 2 from 2 to 2048)."""
    
    def get_tiles(self) -> List[Dict[str, str]]:
        """Generate tiles for all 2048 powers (2, 4, 8, ..., 2048).
        
        Color scheme: Based on Wordle palette, transitions from warm (low powers)
        to cool/neutral (high powers) for Discord dark mode.
        
        Returns:
            List of 11 tile specifications for powers 2 to 2048
        """
        power_colors = {
            2: "#FDCB58",      # Wordle yellow - brightest
            4: "#F9C44E",      # Yellow-orange
            8: "#F5B946",      # Orange-yellow
            16: "#F1AE3E",     # Orange
            32: "#E89E3C",     # Orange-red
            64: "#DC8E3A",     # Red-brown
            128: "#D07E38",    # Brown
            256: "#C46E36",    # Dark brown
            512: "#A85C32",    # Brown-gray transition
            1024: "#5A5A62",   # Dark gray (close to Wordle gray)
            2048: "#31363E",   # Darkest (Wordle gray)
        }
        
        tiles = []
        for power in [2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048]:
            tiles.append({
                "label": f"tile_{power}",
                "color": power_colors[power],
                "text": str(power),
            })
        
        return tiles
