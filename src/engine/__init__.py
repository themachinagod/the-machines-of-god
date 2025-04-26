"""
Engine module for Machines of God game.
Contains core game engine functionality.
"""

# For backward compatibility
from .state import *
from .states import MenuState, PlayingState, ShopState, State
from .visual import ParallaxBackground

# Define public exports
__all__ = ["MenuState", "PlayingState", "ShopState", "State", "ParallaxBackground"]
