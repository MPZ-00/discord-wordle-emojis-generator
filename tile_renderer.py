"""Shared tile rendering utilities for all games."""

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path


def hex_to_rgba(value: str) -> tuple:
    """Convert hex color to RGBA tuple."""
    value = value.lstrip("#")
    return tuple(int(value[i:i+2], 16) for i in (0, 2, 4)) + (255,)


def get_font(font_path: str | None, font_size: int) -> ImageFont.FreeTypeFont:
    """Load font, with fallback to system defaults."""
    candidates = [
        font_path,
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf",
        "C:\\Windows\\Fonts\\arial.ttf",
    ]
    for candidate in candidates:
        if candidate:
            try:
                return ImageFont.truetype(candidate, font_size)
            except Exception:
                pass
    return ImageFont.load_default()


def rounded_rect_mask(size: int, radius: int) -> Image.Image:
    """Create a mask for rounded rectangle."""
    mask = Image.new("L", (size, size), 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle((0, 0, size - 1, size - 1), radius=radius, fill=255)
    return mask


def fit_font(letter: str, tile_size: int, font_path: str | None, 
             target_ratio: float = 0.58) -> ImageFont.FreeTypeFont:
    """Find best font size to fit letter within target ratio of tile."""
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
    text: str,
    fill_hex: str,
    out_dir: Path,
    tile_size: int,
    rounded: bool,
    radius: int,
    font_path: str | None,
    border: bool,
    shadow: bool,
) -> None:
    """Create and save a single tile PNG.
    
    Args:
        label: Tile name (used as filename without extension)
        text: Text to render on tile (if empty, no text rendered)
        fill_hex: Hex color code for tile background
        out_dir: Output directory for PNG
        tile_size: Tile size in pixels
        rounded: Whether to use rounded corners
        radius: Corner radius
        font_path: Path to TTF font (optional)
        border: Whether to add subtle border
        shadow: Whether to add text shadow
    """
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

    if text:
        font = fit_font(text, tile_size, font_path)
        bbox = draw.textbbox((0, 0), text, font=font)
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]
        x = (tile_size - w) / 2 - bbox[0]
        y = (tile_size - h) / 2 - bbox[1] - tile_size * 0.02

        if shadow:
            shadow_fill = (0, 0, 0, 70) if text_color[0] == 255 else (255, 255, 255, 70)
            draw.text((x, y + max(1, tile_size // 64)), text, font=font, fill=shadow_fill)

        draw.text((x, y), text, font=font, fill=text_color)

    img.save(out_dir / f"{label}.png")
