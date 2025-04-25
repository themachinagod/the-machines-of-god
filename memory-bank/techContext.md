# Machines of God - Technical Context

## Technology Stack

### Core Technologies
- **Python 3.12+**: Primary programming language
- **Pygame 2.6.1+**: Game development library
- **NumPy**: For efficient numerical operations
- **PyInstaller**: For creating distributable executables

### Development Tools
- **Visual Studio Code**: Primary IDE
- **Git**: Version control
- **GitHub**: Repository hosting and project management
- **Poetry**: Python package manager and dependency management
- **Ruff**: Fast Python linter written in Rust
- **Black**: Code formatter for consistent styling
- **isort**: Import statement organizer
- **mypy**: Static type checker for Python
- **Pytest**: Unit testing framework

## Development Environment Setup

### Requirements
- Python 3.12+
- Poetry package manager
- Pygame 2.6.1+
- NumPy
- Ruff (for linting)
- Black (for formatting)
- isort (for import organization)
- mypy (for type checking)
- Pytest (for testing)
- PyInstaller (for distribution)

### Installation
```bash
# Clone repository
git clone https://github.com/username/machines-of-god.git
cd machines-of-god

# Set up environment with Poetry
poetry install
# For development dependencies
poetry install --with dev

# Activate the virtual environment
poetry shell

# Run the game
python src/main.py
# Or without activating the environment
poetry run python src/main.py

# Run linting
poetry run ruff check src/
# Auto-fix issues where possible
poetry run ruff check --fix src/

# Run formatting
poetry run black src/
poetry run isort src/

# Run type checking
poetry run mypy src/
```

## Project Structure
```
machines-of-god/
├── assets/                # Game assets
│   ├── images/            # Sprites, backgrounds, UI elements
│   ├── sounds/            # Sound effects
│   ├── fonts/             # Font files
│   └── music/             # Background music
├── src/                   # Source code
│   ├── main.py            # Entry point
│   ├── engine/            # Core game engine
│   │   ├── __init__.py
│   │   ├── game.py        # Main game class
│   │   ├── state.py       # Game state management
│   │   ├── entity.py      # Entity component system
│   │   └── ...
│   ├── entities/          # Game entities
│   │   ├── __init__.py
│   │   ├── player.py      # Player spacecraft
│   │   ├── enemy.py       # Enemy entities
│   │   ├── projectile.py  # Projectiles and weapons
│   │   └── ...
│   ├── states/            # Game states
│   │   ├── __init__.py
│   │   ├── menu.py        # Main menu
│   │   ├── playing.py     # Gameplay state
│   │   ├── pause.py       # Pause menu
│   │   └── ...
│   ├── ui/                # User interface
│   │   ├── __init__.py
│   │   ├── menu.py        # Menu UI
│   │   ├── hud.py         # Heads-up display
│   │   └── ...
│   └── utils/             # Utility functions
│       ├── __init__.py
│       ├── resource.py    # Resource loading
│       ├── config.py      # Configuration
│       └── ...
├── data/                  # Game data
│   ├── levels/            # Level definitions
│   ├── config.json        # Game configuration
│   └── save/              # Save files
├── tests/                 # Unit tests
├── docs/                  # Documentation
│   ├── linting_guide.md   # Guide for code linting
│   └── typing_guide.md    # Guide for type annotations
├── pyproject.toml         # Project metadata and dependencies
├── README.md              # Project overview
└── LICENSE                # License information
```

## Technical Constraints

### Performance Targets
- **FPS Target**: 60 FPS minimum
- **Resolution**: 1280x720 native, scaling for other resolutions
- **Memory Usage**: <500MB RAM
- **Load Times**: <5 seconds for level loading

### Cross-Platform Considerations
- Primary focus on Windows
- Secondary support for Linux and macOS
- Consistent performance across supported platforms

## Dependencies Management

### Core Dependencies
- **pygame**: Game development library
- **numpy**: Numerical operations
- **json**: Save game and configuration
- **logging**: Debug and error logging
- **pytest**: Testing framework

### Versioning
- All dependencies specified in pyproject.toml with version constraints
- Poetry for dependency management
- Virtual environment created and managed by Poetry

## Code Quality

### Linting and Formatting
- **Ruff**: Used for code linting and formatting
- Config is in pyproject.toml and includes:
  - PEP 8 style compliance (with line length of 100)
  - Import sorting
  - Code complexity checks
  - Various code quality rules
- Appropriate rule exemptions for game development context

### Type Checking
- **mypy**: Static type checking
- Progressive typing strategy:
  - Start with basic type annotations for critical code paths
  - Increase type coverage over time
  - Eventually enforce strict typing
- Type stubs for pygame provided by types-pygame package
- Custom type aliases for game-specific concepts

### Testing
- Unit tests with pytest
- Test directory structure mirrors source structure
- Mocking framework for testing components in isolation

## Build and Distribution

### Build Process
- PyInstaller for creating standalone executables
- Build scripts for automating the process
- Asset compression for reducing package size

### Distribution Channels
- GitHub Releases
- Potential distribution on game platforms (Steam, itch.io) in the future

## Technical Debt Management

- Regular refactoring sessions planned
- Unit tests required for core systems
- Code reviews for all significant changes
- Documentation requirements for complex systems 