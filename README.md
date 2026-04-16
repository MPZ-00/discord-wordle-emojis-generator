# Emoji Generator for Discord Games

Generate PNG emoji tiles for multiple games to use in Discord. Supports Wordle, 2048, and extensible for future games.

## What It Generates

### Wordle
- `gray_A` to `gray_Z`, `white_A` to `white_Z`, `green_A` to `green_Z`, `yellow_A` to `yellow_Z`
- `gray_square`, `white_square`
- **Total: 106 tiles** (26 letters × 4 states + 2 squares)

### 2048
- `tile_2.png` to `tile_2048.png` (powers of 2)
- Colors span dark mode palette: warm (low powers) → cool/neutral (high powers)
- **Total: 11 tiles**

## Features

- Optional rounded tiles
- Optional subtle tile border
- Optional light text shadow
- Custom tile size
- Optional custom TTF font

## Requirements

- Python 3.10+
- Pillow (see `requirements.txt`)

## Quick Start

```bash
python -m pip install -r requirements.txt
python emoji_generator.py
```

This generates all games (Wordle + 2048) into `output/` directory, organized as:
```
output/
├── wordle/
│   ├── gray_A.png
│   ├── green_Z.png
│   └── ... (106 total)
└── 2048/
    ├── tile_2.png
    ├── tile_4.png
    └── ... (11 total)
```

## Usage Examples

**Generate all games with default settings:**
```bash
python emoji_generator.py
```

**Generate all games with rendering options (rounded, border, shadow):**
```bash
python emoji_generator.py --rounded --border --shadow
```

**Generate specific games:**
```bash
python emoji_generator.py wordle 2048
python emoji_generator.py 2048       # Only 2048 tiles
python emoji_generator.py wordle     # Only Wordle tiles
```

**Custom tile size (default 128 pixels):**
```bash
python emoji_generator.py --size 256
python emoji_generator.py 2048 --size 96
```

**Custom font:**
```bash
python emoji_generator.py --font "/path/to/font.ttf"
```

**Custom output directory:**
```bash
python emoji_generator.py --out my_emojis
```

**Combine options:**
```bash
python emoji_generator.py 2048 --size 256 --rounded --border --shadow --out discord_assets
```

## Showcase Files In This Repo

This repository intentionally keeps only a small showcase set in `generated_rounded_128`:

- `gray_A.png`
- `green_A.png`
- `yellow_A.png`
- `white_A.png`
- `gray_square.png`
- `white_square.png`

Generate the full set locally using the script.

## Architecture

The system is modular and extensible:

```
emoji_generator.py          # Main CLI entry point
tile_renderer.py            # Shared tile rendering utilities
game.py                     # Abstract GameGenerator base class
games/
├── __init__.py
├── registry.py              # Game discovery and registration
├── wordle.py                # WordleGenerator implementation
└── game_2048.py             # Game2048Generator implementation
```

### Adding a New Game

1. Create a new file in `games/` (e.g., `games/my_game.py`)
2. Implement `GameGenerator` abstract class:
   ```python
   from game import GameGenerator
   from typing import List, Dict
   
   class MyGameGenerator(GameGenerator):
       def get_tiles(self) -> List[Dict[str, str]]:
           return [
               {"label": "tile_name", "color": "#HEXCOLOR", "text": "X"},
               # ...
           ]
   ```
3. Register in `games/registry.py`:
   ```python
   from .my_game import MyGameGenerator
   GameRegistry.register("mygame", MyGameGenerator)
   ```
4. Use immediately:
   ```bash
   python emoji_generator.py mygame --size 128 --rounded
   ```

### 2048 Color Scheme

Powers of 2 are mapped to a color gradient optimized for Discord dark mode:
- `2` → Bright yellow (#FDCB58, from Wordle palette)
- `4-64` → Warm tones (yellows through oranges)
- `128-256` → Brown tones
- `512-1024` → Gray-brown transition
- `2048` → Dark gray (#31363E, from Wordle palette)

This gradient ensures visual progression while maintaining contrast on dark backgrounds.
