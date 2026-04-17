"""Connect 4 theme preset generators for bot themes."""

from .game_connect4 import Connect4ThemedGenerator


# Theme color presets (source of truth - matches bot themes)
THEME_PRESETS = {
    "dark": {
        "background": 0x282C34,
        "player1": 0xE06C75,      # brightRed
        "player2": 0x61AFEF,      # brightBlue
        "foreground": 0xDCDFE4,
    },
    "light": {
        "background": 0xFAFAFA,
        "player1": 0xE45649,      # red
        "player2": 0x0184BC,      # blue
        "foreground": 0x383A42,
    },
    "xcad": {
        "background": 0x1A1A1A,
        "player1": 0xBA5AFF,      # brightRed (magenta in xcad)
        "player2": 0x5C78FF,      # brightBlue
        "foreground": 0xF1F1F1,
    },
}


class Connect4DarkGenerator(Connect4ThemedGenerator):
    """Generate Connect 4 tiles with Dark theme."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, theme_name="dark", theme_colors=THEME_PRESETS["dark"], **kwargs)


class Connect4LightGenerator(Connect4ThemedGenerator):
    """Generate Connect 4 tiles with Light theme."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, theme_name="light", theme_colors=THEME_PRESETS["light"], **kwargs)


class Connect4XcadGenerator(Connect4ThemedGenerator):
    """Generate Connect 4 tiles with Xcad theme."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, theme_name="xcad", theme_colors=THEME_PRESETS["xcad"], **kwargs)
