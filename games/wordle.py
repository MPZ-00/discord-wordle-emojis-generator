"""Wordle emoji generator."""

from typing import List, Dict
from game import GameGenerator


class WordleGenerator(GameGenerator):
    """Generate Wordle-style emoji tiles (letters + states + squares)."""
    
    def get_tiles(self) -> List[Dict[str, str]]:
        """Generate tiles for all letters in all Wordle states plus squares.
        
        Returns:
            List of 30 tile specifications (26 letters × 4 states + 2 squares)
        """
        colors = {
            "gray": "#31363E",
            "white": "#E6E8EA",
            "green": "#78B15C",
            "yellow": "#FDCB58",
        }
        
        tiles = []
        
        for state, color in colors.items():
            for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                tiles.append({
                    "label": f"{state}_{letter}",
                    "color": color,
                    "text": letter,
                })
        
        squares = {
            "gray_square": colors["gray"],
            "white_square": colors["white"],
        }
        
        for name, color in squares.items():
            tiles.append({
                "label": name,
                "color": color,
                "text": "",
            })
        
        return tiles
