# Linting Guide for Machines of God

We use [Ruff](https://github.com/astral-sh/ruff) for linting in this project. This guide will help you understand the common linting issues and how to fix them.

## Setup

Ensure you have the dev dependencies installed:

```bash
uv pip install -e ".[dev]"
```

## Running the Linter

```bash
# Check for issues
ruff check src/

# Auto-fix issues where possible
ruff check --fix src/
```

## Common Issues and How to Fix Them

### Line Length (E501)

Lines should be limited to 100 characters (configured in pyproject.toml).

Example with issue:
```python
def some_function_with_a_really_long_name(parameter1, parameter2, parameter3, parameter4, parameter5, parameter6):
    # ...
```

Fixed:
```python
def some_function_with_a_really_long_name(
    parameter1, parameter2, parameter3, 
    parameter4, parameter5, parameter6
):
    # ...
```

### Imports (I)

Imports should be sorted and grouped correctly.

Example with issue:
```python
import pygame
import random
from os import path
import sys
from pygame.locals import *
```

Fixed:
```python
import random
import sys
from os import path

import pygame
from pygame.locals import *
```

### Unused Imports (F401)

Remove unused imports, except in __init__.py files where they're often used to expose modules.

Example with issue:
```python
import pygame
import random  # This is never used
from pygame.locals import *
```

Fixed:
```python
import pygame
from pygame.locals import *
```

### Star Imports (F403)

Avoid wildcard imports as they can pollute the namespace.

Example with issue:
```python
from pygame.locals import *
```

Fixed:
```python
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE
```

### Code Complexity (C901)

Functions should not be too complex (max complexity: 15).

Example with issue:
```python
def handle_enemies(self, enemies, bullets, player):
    # Complex nested logic with many branches...
    # ...
```

Fixed:
```python
def handle_enemy_movement(self, enemies):
    # Simplified logic for just enemy movement
    # ...

def handle_enemy_collisions(self, enemies, bullets):
    # Simplified logic for just collision detection
    # ...

def handle_enemies(self, enemies, bullets, player):
    # Main function delegates to helper functions
    self.handle_enemy_movement(enemies)
    self.handle_enemy_collisions(enemies, bullets)
    # ...
```

## IDE Integration

### VS Code

1. Install the "Ruff" extension
2. Configure it to use the project's pyproject.toml settings

### PyCharm

1. Install the "Ruff" plugin
2. Configure it to use the project's pyproject.toml settings

## Pre-commit Hooks

To ensure code quality before committing, you can set up pre-commit hooks:

1. Install pre-commit: `pip install pre-commit`
2. Create a `.pre-commit-config.yaml` file:

```yaml
repos:
-   repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.0
    hooks:
    -   id: ruff
        args: [--fix]
```

3. Install the hooks: `pre-commit install`

## Help and Support

If you have questions about fixing specific linting issues, please check the [Ruff documentation](https://docs.astral.sh/ruff/) or reach out to the project maintainers. 