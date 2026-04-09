from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import argparse
import string

COLORS = {
    "gray": "#31363E",
    "white": "#E6E8EA",
    "green": "#78B15C",
    "yellow": "#FDCB58",
}

SQUARES = {
    "gray_square": "#31363E",
    "white_square": "#E6E8EA",
}

def hex_to_rgba(value: str):
    value = value.lstrip("#")
    return tuple(int(value[i:i+2], 16) for i in (0, 2, 4)) + (255,)

def get_font(font_path: str | None, font_size: int):
    candidates = [
        font_path,
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf",
    ]
    for candidate in candidates:
        if candidate:
            try:
                return ImageFont.truetype(candidate, font_size)
            except Exception:
                pass
    return ImageFont.load_default()

def rounded_rect_mask(size: int, radius: int):
    mask = Image.new("L", (size, size), 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle((0, 0, size - 1, size - 1), radius=radius, fill=255)
    return mask

def fit_font(letter: str, tile_size: int, font_path: str | None, target_ratio: float = 0.58):
    target = int(tile_size * target_ratio)
    for font_size in range(int(tile_size * 0.9), 8, -1):
        font = get_font(font_path, font_size)
        dummy = Image.new("RGBA", (tile_size, tile_size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(dummy)
        bbox = draw.textbbox((0, 0), letter, font=font)
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]
        if max(w, h) <= target:
            return font
    return get_font(font_path, int(tile_size * 0.45))

def create_tile(
    label: str,
    fill_hex: str,
    out_dir: Path,
    tile_size: int,
    rounded: bool,
    radius: int,
    font_path: str | None,
    border: bool,
    shadow: bool,
):
    bg = hex_to_rgba(fill_hex)
    text_color = (0, 0, 0, 255) if label.startswith("white_") else (255, 255, 255, 255)

    img = Image.new("RGBA", (tile_size, tile_size), (0, 0, 0, 0))
    tile = Image.new("RGBA", (tile_size, tile_size), bg)

    if rounded:
        mask = rounded_rect_mask(tile_size, radius)
        img.alpha_composite(Image.composite(tile, Image.new("RGBA", (tile_size, tile_size), (0, 0, 0, 0)), mask))
    else:
        img.alpha_composite(tile)

    draw = ImageDraw.Draw(img)

    if border:
        border_color = (255, 255, 255, 45) if not label.startswith("white_") else (0, 0, 0, 35)
        if rounded:
            draw.rounded_rectangle((1, 1, tile_size - 2, tile_size - 2), radius=radius, outline=border_color, width=max(1, tile_size // 48))
        else:
            draw.rectangle((1, 1, tile_size - 2, tile_size - 2), outline=border_color, width=max(1, tile_size // 48))

    if "_" in label and not label.endswith("_square"):
        letter = label.split("_", 1)[1].upper()
        font = fit_font(letter, tile_size, font_path)

        bbox = draw.textbbox((0, 0), letter, font=font)
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]
        x = (tile_size - w) / 2 - bbox[0]
        y = (tile_size - h) / 2 - bbox[1] - tile_size * 0.02

        if shadow:
            shadow_fill = (0, 0, 0, 70) if text_color[0] == 255 else (255, 255, 255, 70)
            draw.text((x, y + max(1, tile_size // 64)), letter, font=font, fill=shadow_fill)

        draw.text((x, y), letter, font=font, fill=text_color)

    img.save(out_dir / f"{label}.png")

def main():
    parser = argparse.ArgumentParser(description="Generate Discord Wordle-style emoji PNGs.")
    parser.add_argument("--out", default="wordle_emojis", help="Output folder")
    parser.add_argument("--size", type=int, default=128, help="Tile size in pixels")
    parser.add_argument("--rounded", action="store_true", help="Use rounded tiles")
    parser.add_argument("--radius", type=int, default=22, help="Corner radius when rounded is enabled")
    parser.add_argument("--font", default=None, help="Path to a TTF font")
    parser.add_argument("--border", action="store_true", help="Add subtle tile border")
    parser.add_argument("--shadow", action="store_true", help="Add subtle text shadow")
    parser.add_argument("--letters", default=string.ascii_uppercase, help="Letters to generate")
    args = parser.parse_args()

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    for state, color in COLORS.items():
        for letter in args.letters.upper():
            create_tile(
                f"{state}_{letter}",
                color,
                out_dir,
                args.size,
                args.rounded,
                args.radius,
                args.font,
                args.border,
                args.shadow,
            )

    for name, color in SQUARES.items():
        create_tile(
            name,
            color,
            out_dir,
            args.size,
            args.rounded,
            args.radius,
            args.font,
            args.border,
            False,
        )

    print(f"Generated files in: {out_dir.resolve()}")

if __name__ == "__main__":
    main()
