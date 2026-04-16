"""Game registry for dynamic game discovery and validation."""

from typing import Dict, Type
from game import GameGenerator


class GameRegistry:
    """Registry mapping game names to generator classes."""
    
    _registry: Dict[str, Type[GameGenerator]] = {}
    
    @classmethod
    def register(cls, name: str, generator_class: Type[GameGenerator]) -> None:
        """Register a game generator.
        
        Args:
            name: Game identifier (e.g., 'wordle', '2048')
            generator_class: GameGenerator subclass
        """
        cls._registry[name.lower()] = generator_class
    
    @classmethod
    def get(cls, name: str) -> Type[GameGenerator] | None:
        """Retrieve a registered game generator.
        
        Args:
            name: Game identifier
            
        Returns:
            GameGenerator subclass or None if not found
        """
        return cls._registry.get(name.lower())
    
    @classmethod
    def list_games(cls) -> list[str]:
        """Return list of registered game names."""
        return sorted(cls._registry.keys())
    
    @classmethod
    def get_all(cls) -> Dict[str, Type[GameGenerator]]:
        """Return all registered games."""
        return cls._registry.copy()


def initialize_registry() -> None:
    """Register all available game generators."""
    from .wordle import WordleGenerator
    from .game_2048 import Game2048Generator
    
    GameRegistry.register("wordle", WordleGenerator)
    GameRegistry.register("2048", Game2048Generator)
