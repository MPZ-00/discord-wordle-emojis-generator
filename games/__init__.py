"""Game-specific emoji generators."""

from .wordle import WordleGenerator
from .game_2048 import Game2048Generator

__all__ = ["WordleGenerator", "Game2048Generator"]
