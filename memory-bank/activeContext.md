# Machines of God - Active Development Context

## Current Development Focus
- Implementing proper Sky Force inspired game mechanics
- Developing upgrade and progression systems
- Building enemy variety and level structure
- Creating a polished visual experience

## Recent Developments
- Created bare-bones prototype with basic movement and shooting
- Implemented simple enemy spawning and collision detection
- Added scrolling background and basic HUD
- Set up the core game loop and state system
- Added initial collectible system with stars
- Implemented basic shop interface
- Added save game functionality for persistence of upgrades and stars
- Implemented missile system with homing capabilities
- Added enemy variety with different behaviors and stats
- Added "Resume Game" and "New Game" options to main menu
- Implemented enemy variance with difficulty scaling and random stat adjustments
- Added directional player movement with ship rotation using comma/period keys
- Implemented directional firing system that matches the ship's orientation
- Created visually distinct ship with clear directional indicators
- Added automatic snap-back-to-center with pause timer for improved control feel
- Refactored complex game logic to improve code maintainability
- Added complete missile guidance system with proper targeting
- Fixed missile and projectile collision detection and response
- Improved weapon pattern implementations (single, double, triple, quad)

## Upgrade System Requirements

### Ship Component System
The ship should be composed of multiple upgradable components, each affecting different aspects of gameplay:

1. **Hull (Health System)**
   - **Level 0:** 50 health (starting)
   - **Level 1:** 75 health
   - **Level 2:** 100 health
   - **Level 3:** 125 health
   - **Level 4:** 150 health
   - **Level 5:** 200 health

2. **Engines (Vertical Movement)**
   - **Level 0:** 250 pixels/sec (starting)
   - **Level 1:** 300 pixels/sec
   - **Level 2:** 350 pixels/sec
   - **Level 3:** 400 pixels/sec
   - **Level 4:** 450 pixels/sec
   - **Level 5:** 500 pixels/sec

3. **Thrusters (Lateral Movement)**
   - **Level 0:** 250 pixels/sec (starting)
   - **Level 1:** 300 pixels/sec
   - **Level 2:** 350 pixels/sec
   - **Level 3:** 400 pixels/sec
   - **Level 4:** 450 pixels/sec
   - **Level 5:** 500 pixels/sec

4. **Primary Weapon System**
   - **Level 0:** Single shot, slow rate (starting)
   - **Level 1:** Single shot, medium rate
   - **Level 2:** Double shot (side by side)
   - **Level 3:** Triple shot (spread)
   - **Level 4:** Quad shot (2x2 pattern)
   - **Level 5:** Five shot (X pattern)

5. **Shield Generator**
   - **Level 0:** No shield (starting)
   - **Level 1:** 50 shield, slow recharge
   - **Level 2:** 75 shield, medium recharge
   - **Level 3:** 100 shield, fast recharge

6. **Secondary Weapons (Missiles)**
   - **Level 0:** No missiles (starting)
   - **Level 1:** Single missile, slow rate
   - **Level 2:** Dual missiles, slow rate
   - **Level 3:** Dual missiles, medium rate

7. **Magnet**
   - **Level 0:** No magnet (starting)
   - **Level 1:** Small radius for collectibles
   - **Level 2:** Medium radius for collectibles
   - **Level 3:** Large radius for collectibles

### Upgrade Costs
- Each component should have progressive costs
- Early upgrades should be affordable, later ones expensive
- Component cost progression: Base cost × (1.5 ^ level)

### Game Balance
- Starting ship should be weak but controllable
- Mid-game ship should feel significantly improved
- Fully upgraded ship should feel powerful but not invincible
- Each upgrade should provide a noticeable improvement

## Enemy System Requirements

### Enemy Types
1. **Basic Fighter**
   - Simple downward movement
   - No shooting capability
   - Low health
   - Worth few stars

2. **Zig-Zag Fighter**
   - Moves in a zig-zag pattern
   - No shooting capability
   - Low health
   - Worth few stars

3. **Shooter**
   - Moves down slowly
   - Fires at regular intervals
   - Medium health
   - Worth medium stars

4. **Heavy Bomber**
   - Moves slowly
   - Takes multiple hits to destroy
   - Worth many stars

5. **Kamikaze**
   - Tracks player position
   - Attempts to crash into player
   - Medium health
   - Worth medium stars

### Enemy Spawning
- Should be wave-based
- Later waves should include more difficult enemies
- Spawn patterns should create interesting gameplay
- Random element to spawning to keep gameplay fresh

## Level Design Requirements

### Level Structure
1. **Beginning (30 seconds)**
   - Mostly basic fighters
   - Few zig-zag fighters
   - Predictable patterns

2. **Middle (60 seconds)**
   - Mix of basic, zig-zag, and shooters
   - Introduction of more complex patterns
   - Increased density of enemies

3. **End (30 seconds)**
   - All enemy types
   - Complex patterns
   - Introduction of heavy bombers
   - Lead-up to boss fight

4. **Boss (varies)**
   - Unique attack patterns
   - Multiple phases
   - Health bar
   - Special attacks

### Difficulty Progression
- Each level should be more difficult than the last
- Difficulty within a level should ramp up
- Difficulty should be balanced with player upgrades

## Technical Requirements

### Player Class Structure
```python
class Player:
    # Core properties
    health = 0       # Current health
    max_health = 0   # Maximum health from Hull level
    shield = 0       # Current shield
    max_shield = 0   # Maximum shield from Shield level
    
    # Movement properties
    vert_speed = 0   # From Engine level
    lat_speed = 0    # From Thruster level
    
    # Weapon properties
    primary_level = 0
    secondary_level = 0
    primary_cooldown = 0
    secondary_cooldown = 0
    
    # Upgrade levels
    upgrades = {
        "hull": 0,
        "engine": 0,
        "thruster": 0,
        "primary": 0,
        "shield": 0,
        "secondary": 0,
        "magnet": 0
    }
    
    def update_stats(self):
        # Update all stats based on upgrade levels
        pass
        
    def fire_primary(self):
        # Create projectile pattern based on primary level
        pass
        
    def fire_secondary(self):
        # Create missiles based on secondary level
        pass
```

### Save System
- Save all upgrade levels
- Save accumulated stars
- Save unlocked levels
- JSON format for easy editing/debugging

## Implementation Priorities

1. **Phase 1: Core Component System** ✓
   - Refactor Player class to support component system ✓
   - Implement proper upgrade effects ✓
   - Balance starting attributes ✓

2. **Phase 2: Enemy Variety** ✓
   - Implement all enemy types ✓
   - Create spawn patterns ✓
   - Balance difficulty ⚠️ (In progress)

3. **Phase 3: Level Structure**
   - Design proper level flow ⚠️ (In progress)
   - Implement boss encounters
   - Add level selection

4. **Phase 4: Polish**
   - Improved visual effects
   - Sound effects and music
   - Menu and UI improvements ⚠️ (In progress)

## Development Environment

- Python 3.12
- Poetry for package and environment management
- Pygame 2.6.1
- Entity Component System architecture
- State machine for game flow management

## Sky Force Clone Implementation Plan

### Core Gameplay Systems
1. **Aircraft Control System**
   - Smooth, responsive movement with speed adjustments
   - Screen boundary constraints
   - Special maneuvers (barrel roll for temporary invincibility)

2. **Weapon Systems**
   - Primary weapon (upgradeable rate of fire, power, spread)
   - Secondary weapons (missiles, bombs, lasers)
   - Special weapons (screen-clearing mega bomb, freeze ray)
   - Heat-seeking missiles for targeting specific enemies

3. **Level System**
   - Structured stage-based progression
   - Boss encounters at end of each stage
   - Difficulty scaling with stage progression
   - Checkpoint system within longer stages

4. **Upgrade Progression**
   - Permanent ship upgrades using collected stars/currency
   - Weapon upgrades (damage, fire rate, spread patterns)
   - Shield upgrades (capacity, recharge rate)
   - Speed/maneuverability upgrades
   - Magnet strength for collecting items

5. **In-game Powerups**
   - Shield pickups for temporary invulnerability
   - Weapon powerups for temporary weapon enhancements
   - Score multipliers
   - Health/repair pickups

6. **Resource Collection**
   - Stars as primary currency for permanent upgrades
   - Special collectibles for rare upgrades or unlocks
   - Mission-specific collectibles

7. **Mission System**
   - Primary mission (complete the level)
   - Secondary objectives (rescue humans, destroy specific targets)
   - Achievement-like challenges for replayability

8. **Enemy Variety**
   - Basic enemies with simple movement patterns
   - Advanced enemies with shooting capabilities
   - Shielded enemies requiring multiple hits
   - Environmental hazards and obstacles
   - Mini-bosses and main stage bosses

### Technical Architecture

1. **Entity Component System**
   - Component-based architecture for flexible entity creation
   - Health, collision, weapon, movement, AI components
   - Entity manager for efficient updates and rendering

2. **Rendering Pipeline**
   - Multi-layered background with parallax scrolling
   - Particle effects system for explosions, engines, weapons
   - Dynamic lighting effects
   - Screen shake and other visual feedback

3. **Audio System**
   - Dynamic music that adapts to gameplay intensity
   - Comprehensive sound effects for feedback
   - Audio mixing and prioritization

4. **Save System**
   - Persistent player progression
   - Unlocked levels and achievements
   - Purchased upgrades
   - High scores and statistics

5. **UI Framework**
   - Main menu, level select, upgrade shop interfaces
   - In-game HUD with health, score, objectives
   - Pause menu with options
   - Post-mission results screen

### Implementation Phases

#### Phase 1: Core Mechanics Refinement
- [x] Basic player movement and shooting
- [ ] Improved collision detection and response
- [ ] Proper enemy spawning patterns
- [ ] Enhanced visual feedback for actions
- [ ] Basic powerup system

#### Phase 2: Progression Systems
- [ ] Star collection system
- [ ] Permanent upgrade shop structure
- [ ] Save/load upgrade progress
- [ ] Implement upgrade effects (damage, speed, etc.)
- [ ] Mission objectives system

#### Phase 3: Content Development
- [ ] Multiple enemy types with unique behaviors
- [ ] Boss enemy implementation
- [ ] Level design with increasing difficulty
- [ ] Additional weapon types and special abilities
- [ ] Visual polish (effects, UI improvements)

#### Phase 4: Polish and Refinement
- [ ] Tutorial system
- [ ] Difficulty balancing
- [ ] Performance optimization
- [ ] Additional sound effects and music
- [ ] Screen transitions and polish

## Next Steps

### Immediate Tasks (Current Sprint)
1. Finalize missile collision detection fix
2. Complete "Resume Game" and "New Game" functionality testing
3. Implement boss enemy encounter for end of level
4. Enhance visual effects for collisions, explosions, and weapons
5. Add sound effects for actions and background music
6. Refine upgrade balance based on testing

### Planned Tasks (Next Sprint)
1. Add multiple levels with increasing difficulty
2. Implement proper game completion screen
3. Add achievement system for gameplay rewards
4. Enhance visual polish with improved sprites and animations
5. Implement difficulty settings

## Technical Architecture

The game now follows a state-based architecture with the following key components:

1. **Game Engine**
   - Main game loop
   - State management
   - Save/load system
   - Input handling

2. **Game States**
   - Menu State (with resume/new game options)
   - Playing State (core gameplay)
   - Shop State (upgrade system)

3. **Entity System**
   - Player with upgradable components
   - Multiple enemy types with varied behaviors
   - Projectiles and homing missiles
   - Collectibles for resources

4. **Save System**
   - JSON-based save file for game progress
   - Stores upgrade levels and collected stars
   - Supports separate new game and resume functionality

The current implementation provides a solid foundation for future expansion while maintaining good separation of concerns between the different game components.

## Current Status & Progress

### Completed Features
- Player movement and shooting mechanics
- Basic enemy spawning system
- Collision detection and damage systems
- Scrolling background with parallax effect
- HUD display with player stats
- Shop system for purchasing upgrades
- Save/load system for game progress
- Multiple weapon types based on upgrades
- Enemy variety with different behaviors
- Collectible items (stars, health, shields)
- Missile system with target tracking
- Menu system with game flow control
- Enemy difficulty scaling and variance
- Directional movement with rotation controls
- Auto-centering ship rotation with pause timer
- Visually distinct ship with directional indicators
- Multiple projectile patterns with directional firing
- Component-based upgrade system
- Wave-based enemy spawning system
- Progressive shop pricing model
- Full save/resume game functionality

### In Progress Features
- Further enemy variety with boss encounters
- Level progression system
- Additional weapon types and powerups
- Visual effects improvements

### Known Issues
- Missiles should disappear on contact with enemies (fixed)
- Game shows previous upgrades in shop but they aren't applied correctly after restart (fixed with new game/resume system)
- Need more visual feedback for damage and collisions
- Enemy spawn patterns need further refinement
- Game difficulty progression needs balancing

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