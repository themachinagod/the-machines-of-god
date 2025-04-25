# Machines of God

A vertical scrolling shoot 'em up game inspired by classics like Sky Force, built with Pygame.

## Overview

"Machines of God" is a vertical shooter where players control a spacecraft fighting against waves of enemy forces across multiple challenging levels. The game features weapon upgrades, boss battles, and a progression system that rewards both skill and persistence.

## Features

- Fast-paced vertical scrolling shooter gameplay
- Multiple enemy types with varied attack patterns
- Weapon power-ups and upgrade system
- Boss battles at the end of each level
- Progressive difficulty system
- Score multipliers and achievement system

## Getting Started

### Prerequisites

- Python 3.12 or higher
- Poetry package manager (https://python-poetry.org/docs/#installation)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/username/machines-of-god.git
cd machines-of-god
```

2. Set up the environment with Poetry:
```bash
# Install dependencies and create virtual environment
poetry install

# For development dependencies
poetry install --with dev

# Activate the virtual environment
poetry shell
```

3. Run the game:
```bash
# With the Poetry environment activated
python src/main.py

# Or without activating the environment
poetry run python src/main.py
```

## Development

This project is in active development. Check the memory-bank directory for project documentation and current development status.

### Code Style and Linting

We use Ruff for linting and code quality checks, Black for code formatting, and isort for organizing imports. To maintain code quality:

```bash
# Check code for issues
poetry run ruff check src/

# Auto-fix issues where possible
poetry run ruff check --fix src/

# Format code with Black
poetry run black src/

# Sort imports with isort
poetry run isort src/
```

The code style rules are configured in the `pyproject.toml` file and follow PEP 8 with some adjustments for game development. Black is configured with a line length of 100 characters, and isort is set to be compatible with Black's formatting style.

### Type Checking

We use mypy for static type checking. To check types:

```bash
# Run the type checker
poetry run mypy src/
```

Type checking rules are configured in `pyproject.toml` and we follow a progressive typing strategy, adding more type annotations as the project matures.

Check out the `docs/typing_guide.md` for examples and best practices.

## Controls

- Arrow keys or WASD: Move the spacecraft
- Space: Fire primary weapon
- Z, X: Special weapons/abilities
- P: Pause game
- ESC: Exit to menu

## License

[Insert License Information Here]

## Acknowledgements

- Inspired by Sky Force series by Infinite Dreams
- Built with Pygame
- [Additional acknowledgements as needed] 