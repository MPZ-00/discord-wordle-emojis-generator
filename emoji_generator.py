"""Multi-game emoji generator for Discord.

Supports generating tiles for multiple games including Wordle and 2048.
Each game gets its own output directory.

Examples:
    Generate all games with default settings:
        python emoji_generator.py --all
    
    Generate specific games:
        python emoji_generator.py wordle 2048
    
    Generate with custom options:
        python emoji_generator.py 2048 --size 256 --rounded --border --shadow
"""

import argparse
import string
from pathlib import Path

from games.registry import GameRegistry, initialize_registry


def main():
    parser = argparse.ArgumentParser(
        description="Generate emoji tiles for various games to use in Discord."
    )
    parser.add_argument(
        "games",
        nargs="*",
        default=["all"],
        help="Games to generate: 'all' (default), or specific game names (e.g., 'wordle', '2048')"
    )
    parser.add_argument(
        "--out",
        default="output",
        help="Output root folder (each game gets its own subdirectory)"
    )
    parser.add_argument(
        "--size",
        type=int,
        default=128,
        help="Tile size in pixels (default: 128)"
    )
    parser.add_argument(
        "--rounded",
        action="store_true",
        help="Use rounded tile corners"
    )
    parser.add_argument(
        "--radius",
        type=int,
        default=22,
        help="Corner radius when --rounded is enabled (default: 22)"
    )
    parser.add_argument(
        "--font",
        default="C:\\Windows\\Fonts\\JetBrainsMonoNerdFont-Regular.ttf",
        help="Path to custom TTF font file (default: JetBrainsMono Nerd Font)"
    )
    parser.add_argument(
        "--border",
        action="store_true",
        help="Add subtle tile border"
    )
    parser.add_argument(
        "--shadow",
        action="store_true",
        help="Add subtle text shadow"
    )
    
    args = parser.parse_args()
    
    initialize_registry()
    
    games_to_generate = []
    if args.games == ["all"]:
        games_to_generate = GameRegistry.list_games()
    else:
        games_to_generate = args.games
    
    available_games = GameRegistry.list_games()
    invalid_games = [g for g in games_to_generate if g.lower() not in available_games]
    
    if invalid_games:
        print(f"Error: Unknown games: {', '.join(invalid_games)}")
        print(f"Available games: {', '.join(available_games)}")
        return
    
    output_root = Path(args.out)
    print(f"\nGenerating emoji tiles to: {output_root.resolve()}\n")
    
    for game_name in games_to_generate:
        game_class = GameRegistry.get(game_name)
        if not game_class:
            print(f"Skipping unknown game: {game_name}")
            continue
        
        game_output_dir = output_root / game_name
        generator = game_class(
            tile_size=args.size,
            rounded=args.rounded,
            radius=args.radius,
            font_path=args.font,
            border=args.border,
            shadow=args.shadow,
        )
        generator.generate(game_output_dir)
    
    print(f"\nAll games generated successfully!")


if __name__ == "__main__":
    main()
