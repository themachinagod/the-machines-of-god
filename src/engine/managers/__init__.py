"""
Game manager modules for Machines of God.
These managers handle specific aspects of the game to avoid god classes.
"""

from .collectible_manager import CollectibleManager
from .collision_manager import CollisionManager
from .enemy_manager import EnemyManager
from .level_manager import LevelManager
from .ui_manager import UIManager

__all__ = [
    "EnemyManager",
    "CollectibleManager",
    "CollisionManager",
    "LevelManager",
    "UIManager",
]
