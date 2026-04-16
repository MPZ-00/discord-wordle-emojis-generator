from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, List, Tuple


class GameGenerator(ABC):
    """Abstract base class for game-specific emoji generators.
    
    All game generators must inherit from this class and implement
    the required methods.
    """

    def __init__(self, tile_size: int, rounded: bool, radius: int, 
                 font_path: str | None, border: bool, shadow: bool):
        """
        Initialize game generator with shared rendering options.
        
        Args:
            tile_size: Size of tiles in pixels
            rounded: Whether to use rounded corners
            radius: Corner radius when rounded is enabled
            font_path: Path to custom TTF font (optional)
            border: Whether to add subtle tile border
            shadow: Whether to add text shadow
        """
        self.tile_size = tile_size
        self.rounded = rounded
        self.radius = radius
        self.font_path = font_path
        self.border = border
        self.shadow = shadow

    @abstractmethod
    def get_tiles(self) -> List[Dict[str, str]]:
        """Return list of tiles to generate.
        
        Each tile dict should contain:
        - 'label': unique identifier for the tile (used as filename)
        - 'color': hex color code (e.g., '#FFFFFF')
        - 'text': text to render on tile (optional, if empty no text rendered)
        
        Returns:
            List of tile specifications
        """
        pass

    def generate(self, out_dir: Path) -> None:
        """Generate all tiles for this game.
        
        Args:
            out_dir: Directory to save PNG files
        """
        from tile_renderer import create_tile
        
        out_dir = Path(out_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        
        tiles = self.get_tiles()
        for tile in tiles:
            create_tile(
                label=tile['label'],
                text=tile.get('text', ''),
                fill_hex=tile['color'],
                out_dir=out_dir,
                tile_size=self.tile_size,
                rounded=self.rounded,
                radius=self.radius,
                font_path=self.font_path,
                border=self.border,
                shadow=self.shadow,
            )
        
        print(f"Generated {len(tiles)} tiles for {self.__class__.__name__} in: {out_dir.resolve()}")
