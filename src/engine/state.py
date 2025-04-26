"""
State classes for Machines of God game.
Handles different game states like menu, playing, paused, etc.

This module is kept for backward compatibility.
The actual state classes have been moved to the states/ directory.
"""

from engine.states import MenuState, PlayingState, ShopState, State
from engine.visual import ParallaxBackground

# Export all state classes
__all__ = ["State", "MenuState", "ShopState", "PlayingState", "ParallaxBackground"]
