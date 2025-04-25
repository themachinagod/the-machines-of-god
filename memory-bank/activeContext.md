# Machines of God - Active Development Context

## Current Development Focus
- Building core game engine components
- Implementing entity component system
- Refining visual rendering pipeline
- Establishing game world physics

## Recent Developments
- Switched to Poetry for package management and virtual environments
- Updated Pygame from version 2.1.0 to 2.6.1
- Added Black formatter (version 23.9.0) for consistent code styling
- Added isort (version 5.12.0) for organizing import statements
- Implemented basic entity component system architecture
- Added type annotations and mypy type checking
- Set up Ruff linter configuration
- Created initial project structure with Poetry for package management

## Immediate Next Steps
- Complete physics engine integration
- Finalize character movement mechanics
- Implement inventory system
- Expand game world generation logic

## Known Issues
- Some graphics rendering is inefficient and needs optimization
- Collision detection system needs refinement
- Asset loading system is not properly cached

## Current Focus

We are currently in the initial setup phase of the project. The immediate focus is on establishing the basic project structure, setting up the game engine, and creating a simple prototype with the following features:

1. Basic player movement
2. Simple enemy spawning
3. Core game loop implementation
4. Rendering system foundation

## Current Challenges

- Need to implement the core game engine components
- Setup the main game loop with proper timing
- Design and implement initial player controls
- Create asset placeholders for early development
- Ensure code follows the linting standards
- Begin adding type annotations to critical components

## Next Steps

### Immediate Tasks (Current Sprint)
- Setup the basic Pygame window and game loop
- Implement the state management system
- Create player spacecraft with basic movement
- Implement simple scrolling background
- Clean up existing code to meet Ruff linting standards
- Add type annotations to core engine components

### Upcoming Tasks (Next Sprint)
- Basic enemy spawning system
- Collision detection between player and enemies
- Simple projectile system
- HUD elements (score, lives)
- Increase type annotation coverage

## Active Decisions

### In Progress
- Determining the optimal player control scheme (keyboard vs. controller priority)
- Designing the component interface for game entities
- Planning the asset creation/acquisition strategy
- Finalizing code style and linting rules
- Defining type annotation standards and conventions

### Recently Decided
- Use Poetry for package and dependency management
- Use Pygame as the primary game library
- Implement a component-based entity system
- Structure the game with a state machine architecture
- Target 60 FPS for smooth gameplay
- Use Ruff for linting with PEP 8 style guidelines (100 char line length)
- Use mypy for static type checking with a progressive typing strategy
- Require Python 3.12 to leverage latest language features

## Development Environment

Currently setting up the development environment with:
- Python 3.12
- Poetry for package and environment management
- Pygame 2.1.0
- Ruff for linting and code quality
- mypy for static type checking
- VSCode with Python extensions
- Git for version control

## Current Prototype Goals

The first prototype should demonstrate:
- Smooth vertical scrolling
- Responsive player controls
- Basic enemy patterns
- Simple shooting mechanics

This will validate the core gameplay feel and technical approach before expanding to more complex features. 