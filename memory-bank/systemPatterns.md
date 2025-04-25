# Machines of God - System Patterns

## Architecture Overview

"Machines of God" will use a component-based architecture with state management patterns to create a modular, maintainable codebase. The game will be built with Pygame, leveraging its sprite and group management system for efficient rendering and collision detection.

## Core Patterns

### Component-Based Architecture
- Game objects will be composed of reusable components (rendering, collision, movement, etc.)
- Components will have a standard interface with init, update, and draw methods
- This allows for easy extension and composition of game entities

### State Management
- Game will use a state machine to manage different game states (menu, playing, paused, game over)
- Each state will handle its own update and draw operations
- State transitions will be managed centrally with proper entry/exit procedures

### Event System
- Observer pattern for game events (collisions, power-ups, level completion)
- Event queue for processing input and game events
- Event handlers for responding to specific events

## Key System Relationships

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  Game Engine    │────▶│  State Manager  │────▶│     States      │
└─────────────────┘     └─────────────────┘     └─────────────────┘
         │                                             │
         ▼                                             ▼
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  Entity Manager │────▶│   Game Entity   │────▶│   Components    │
└─────────────────┘     └─────────────────┘     └─────────────────┘
         │                      │                      │
         ▼                      ▼                      ▼
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│ Collision System│     │ Rendering System│     │   Input System  │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

## Technical Decisions

### Pygame
- Chosen for its simplicity, Python integration, and cross-platform support
- Using Pygame's sprite group system for efficient rendering and collision detection
- Extending basic Pygame functionality with custom components

### Rendering Approach
- Layer-based rendering for background, gameplay elements, UI, and effects
- Dirty rectangle optimization to improve performance
- Pre-rendering static elements where possible

### Physics and Collision
- Using Pygame's built-in collision detection for basic hitboxes
- Custom collision detection for more precise interactions (like per-pixel collision for bosses)
- Simplified physics model appropriate for a vertical shooter

### Save System
- JSON-based save files for game progress
- Encrypted saves to prevent tampering
- Autosave functionality at key progression points

## Design Patterns in Use

- **Factory Pattern**: For creating different types of enemies, projectiles, and power-ups
- **Observer Pattern**: For event handling and communication between game components
- **State Pattern**: For managing game states and enemy behaviors
- **Command Pattern**: For input handling and potential replay/undo features
- **Singleton Pattern**: For global managers (sound, resource, input)
- **Component Pattern**: For composable game entities 