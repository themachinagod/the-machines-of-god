# Type Checking Guide for Machines of God

We use [mypy](https://github.com/python/mypy) for static type checking in this project. This guide will help you understand how to use type annotations and fix common type-related issues.

## Setup

Ensure you have the dev dependencies installed:

```bash
uv pip install -e ".[dev]"
```

## Running the Type Checker

```bash
# Check the entire codebase
mypy src/

# Check a specific file
mypy src/main.py
```

## Type Annotation Basics

### Variables and Constants

```python
# Type annotations for variables
player_name: str = "Player 1"
lives: int = 3
speed: float = 5.0
is_game_over: bool = False

# For constants, use uppercase
MAX_ENEMIES: int = 10
DEFAULT_SPEED: float = 200.0
```

### Functions and Methods

```python
def add_score(points: int) -> int:
    """Add points to the score and return the new total."""
    global score
    score += points
    return score

def get_player_position() -> tuple[float, float]:
    """Return the player's x, y position."""
    return player.x, player.y

def is_collision(sprite1: pygame.sprite.Sprite, sprite2: pygame.sprite.Sprite) -> bool:
    """Check if two sprites are colliding."""
    return pygame.sprite.collide_rect(sprite1, sprite2)
```

### Class Typing

```python
class Player:
    def __init__(self, x: float, y: float, speed: float = 5.0) -> None:
        self.x: float = x
        self.y: float = y
        self.speed: float = speed
        self.health: int = 100
        self.bullets: list[Bullet] = []

    def move(self, dx: float, dy: float) -> None:
        """Move the player by the given amount."""
        self.x += dx * self.speed
        self.y += dy * self.speed

    def get_position(self) -> tuple[float, float]:
        """Return the player's position."""
        return self.x, self.y
```

### Collections

```python
# Lists
enemies: list[Enemy] = []
high_scores: list[int] = [1000, 900, 800]

# Dictionaries
settings: dict[str, bool] = {"sound": True, "music": True}
player_stats: dict[str, int] = {"health": 100, "ammo": 50}

# Sets
active_powerups: set[str] = {"shield", "rapid_fire"}

# Optional values (may be None)
from typing import Optional
current_boss: Optional[Enemy] = None  # In Python 3.10+, you can also use Enemy | None
```

## Python 3.12 Typing Features

### Type Parameter Syntax

Python 3.12 adds a new syntax for generic types with type parameters:

```python
# Python 3.12 type parameter syntax
class GameState[T]:
    def __init__(self, initial_value: T) -> None:
        self.value: T = initial_value
        
    def get(self) -> T:
        return self.value
        
    def set(self, new_value: T) -> None:
        self.value = new_value

# Usage
game_level = GameState[int](1)
player_name = GameState[str]("Player 1")
```

### TypedDict Improvements

With Python 3.12, TypedDict has improved handling for required vs optional keys:

```python
from typing import TypedDict, NotRequired

class EnemyConfig(TypedDict):
    type: str  # Required
    health: int  # Required
    speed: float  # Required
    drops: NotRequired[list[str]]  # Optional
    spawn_effect: NotRequired[str]  # Optional

# Usage
basic_enemy: EnemyConfig = {
    "type": "basic",
    "health": 10,
    "speed": 50.0,
}

boss_enemy: EnemyConfig = {
    "type": "boss",
    "health": 500,
    "speed": 30.0,
    "drops": ["weapon_upgrade", "shield"],
    "spawn_effect": "explosion"
}
```

## Using Type Aliases

Type aliases can make complex types more readable:

```python
from typing import TypeAlias, Optional, Callable

# Type aliases
Position: TypeAlias = tuple[float, float]
Velocity: TypeAlias = tuple[float, float]
SpriteList: TypeAlias = list[pygame.sprite.Sprite]
CollisionHandler: TypeAlias = Callable[[pygame.sprite.Sprite, pygame.sprite.Sprite], None]

# Using the aliases
def move_sprite(sprite: pygame.sprite.Sprite, position: Position) -> None:
    sprite.rect.x, sprite.rect.y = position

def register_collision(handler: CollisionHandler) -> None:
    collision_handlers.append(handler)
```

## Special Cases in Game Development

### Pygame-specific Types

```python
# Pygame surfaces
screen: pygame.Surface
background: pygame.Surface

# Rect objects
player_rect: pygame.Rect = pygame.Rect(100, 100, 50, 50)

# Sprite groups
all_sprites: pygame.sprite.Group = pygame.sprite.Group()
enemies: pygame.sprite.Group = pygame.sprite.Group()
```

### Dealing with Event Handlers

Event handlers often have varied parameter types. Use union types for flexibility:

```python
from typing import Union, Callable

EventHandler: TypeAlias = Callable[[pygame.event.Event], None]

def register_event_handler(event_type: int, handler: EventHandler) -> None:
    event_handlers[event_type] = handler
```

## Common Type Issues and Solutions

### Missing Type Annotations

Issue:
```python
def get_enemy_count():  # Missing return type
    return len(enemies)
```

Solution:
```python
def get_enemy_count() -> int:
    return len(enemies)
```

### Incompatible Types

Issue:
```python
health: int = 100
health = "full"  # Error: Incompatible types (str, int)
```

Solution:
```python
health: int = 100
health_status: str = "full"  # Use a different variable for different types
```

### Optional Values

Issue:
```python
active_powerup = None
active_powerup.activate()  # Error: 'None' has no attribute 'activate'
```

Solution:
```python
from typing import Optional

active_powerup: Optional[PowerUp] = None
if active_powerup is not None:
    active_powerup.activate()
```

## Type Checking Configuration

Our mypy configuration is in `pyproject.toml`. Key settings include:

- `python_version = "3.12"`: Type checking is based on Python 3.12 features
- `check_untyped_defs = true`: Check functions without type annotations
- `disallow_untyped_defs = false`: Currently allowing functions without type annotations
- `warn_return_any = true`: Warn when a function returns Any

As the project matures, we'll gradually make type checking more strict by enabling additional checks.

## IDE Integration

### VS Code

1. Install the "Python" extension (which includes mypy support)
2. Configure settings.json to use mypy:
   ```
   "python.linting.mypyEnabled": true,
   "python.linting.enabled": true
   ```

### PyCharm

1. Go to Settings → Tools → Python Integrated Tools
2. Set "Type Checker" to "mypy"

## Help and Resources

- [mypy documentation](https://mypy.readthedocs.io/)
- [Python type hints cheat sheet](https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html)
- Standard library: `from typing import ...`
- Python 3.12+: New typing features like type parameters `class Box[T]:` 