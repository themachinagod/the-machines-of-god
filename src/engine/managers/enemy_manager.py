"""
Enemy manager for handling enemy spawning and behavior.
"""

import math
import random
from enum import Enum

from engine.managers.wave_manager import WaveManager
from entities.enemy import (
    BasicEnemy,
    DartEnemy,
    HeavyBomber,
    ShieldBearerEnemy,
    ShooterEnemy,
    ZigzagEnemy,
)


class FormationType(Enum):
    """Types of enemy formations."""

    RANDOM = "random"  # Random spawning (original behavior)
    LINE = "line"  # Horizontal line formation
    V_SHAPE = "v_shape"  # V-shaped formation
    CIRCLE = "circle"  # Circle formation
    ARC = "arc"  # Arc formation
    DIAMOND = "diamond"  # Diamond formation


class FormationPattern:
    """Defines a pattern for spawning enemies in formation."""

    def __init__(
        self,
        formation_type,
        enemy_type,
        count,
        screen_width,
        spawn_delay=0.2,
        x_offset=None,
        spacing=60,
    ):
        """Initialize a formation pattern.

        Args:
            formation_type (FormationType): Type of formation
            enemy_type (str): Type of enemy to spawn
            count (int): Number of enemies in the formation
            screen_width (int): Width of the screen for positioning
            spawn_delay (float): Delay between spawning each enemy in the formation
            x_offset (int, optional): Horizontal offset from center. If None, centered.
            spacing (int): Spacing between enemies in the formation
        """
        self.formation_type = formation_type
        self.enemy_type = enemy_type
        self.count = count
        self.screen_width = screen_width
        self.spawn_delay = spawn_delay
        self.x_offset = x_offset if x_offset is not None else 0
        self.spacing = spacing

        # Spawning state
        self.spawned_count = 0
        self.spawn_timer = 0
        self.complete = False

    def update(self, dt):
        """Update spawning timer.

        Args:
            dt (float): Time elapsed since last update in seconds

        Returns:
            tuple: (should_spawn, x_position) or None if no spawn should occur
        """
        if self.complete:
            return None

        self.spawn_timer += dt
        if self.spawn_timer >= self.spawn_delay and self.spawned_count < self.count:
            self.spawn_timer = 0
            x_pos = self._get_position_for_index(self.spawned_count)
            self.spawned_count += 1

            if self.spawned_count >= self.count:
                self.complete = True

            return (True, x_pos)

        return None

    def _get_position_for_index(self, index):
        """Get the x position for an enemy in the formation.

        Args:
            index (int): Index of enemy in the formation

        Returns:
            int: X position to spawn the enemy
        """
        center = self.screen_width // 2 + self.x_offset

        if self.formation_type == FormationType.RANDOM:
            # Random position, like original behavior
            return random.randint(50, self.screen_width - 50)

        elif self.formation_type == FormationType.LINE:
            # Horizontal line formation
            total_width = (self.count - 1) * self.spacing
            start_x = center - total_width // 2
            return start_x + index * self.spacing

        elif self.formation_type == FormationType.V_SHAPE:
            # V-shaped formation
            half = self.count // 2
            if index < half:
                # Left side of V
                return center - (half - index) * self.spacing
            else:
                # Right side of V
                return center + (index - half) * self.spacing

        elif self.formation_type == FormationType.CIRCLE:
            # Circle formation
            radius = self.count * self.spacing / (2 * math.pi)
            angle = 2 * math.pi * index / self.count
            return center + int(math.cos(angle) * radius)

        elif self.formation_type == FormationType.ARC:
            # Arc formation (half circle)
            radius = self.count * self.spacing / math.pi
            angle = math.pi * index / (self.count - 1) if self.count > 1 else 0
            return center + int(math.cos(angle) * radius)

        elif self.formation_type == FormationType.DIAMOND:
            # Diamond formation
            quarter = self.count // 4
            if index < quarter:
                # Top left
                return center - (quarter - index) * self.spacing
            elif index < quarter * 2:
                # Top right
                return center + (index - quarter) * self.spacing
            elif index < quarter * 3:
                # Bottom right
                return center + (quarter * 2 - index) * self.spacing
            else:
                # Bottom left
                return center - (index - quarter * 3) * self.spacing

        else:
            return center  # Default to center


class EnemyManager:
    """Manages all enemy-related activities including spawning and behavior."""

    def __init__(self, screen_width, screen_height, all_sprites, enemy_group, enemy_projectiles):
        """Initialize the enemy manager.

        Args:
            screen_width: Width of the game screen
            screen_height: Height of the game screen
            all_sprites: Group containing all game sprites
            enemy_group: Group containing enemy sprites
            enemy_projectiles: Group containing enemy projectile sprites
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.all_sprites = all_sprites
        self.enemies = enemy_group
        self.enemy_projectiles = enemy_projectiles

        # Create wave manager
        self.wave_manager = WaveManager()

        # Active formations
        self.active_formations = []

        # Enemy spawn timers
        self.formation_timers = {}

    def set_waves(self, waves):
        """Set the wave definitions.

        Args:
            waves: List of wave definitions
        """
        # Process wave definitions to add formations
        for wave in waves:
            if "formations" not in wave:
                # Convert traditional enemy definitions to formations
                formations = []
                for enemy_def in wave.get("enemies", []):
                    enemy_type = enemy_def["type"]
                    count = enemy_def["count"]
                    interval = enemy_def["interval"]

                    # Choose a random formation type for variety
                    if enemy_type == "zigzag":
                        formation_type = FormationType.V_SHAPE
                    elif enemy_type == "shooter":
                        formation_type = FormationType.LINE
                    elif enemy_type == "heavy":
                        formation_type = FormationType.DIAMOND
                    elif enemy_type == "shield":
                        formation_type = FormationType.ARC
                    elif enemy_type == "dart":
                        formation_type = FormationType.CIRCLE
                    else:
                        formation_type = random.choice(
                            [FormationType.LINE, FormationType.V_SHAPE, FormationType.ARC]
                        )

                    # Create a formation for this enemy type
                    formations.append(
                        {
                            "type": formation_type.value,
                            "enemy_type": enemy_type,
                            "count": count,
                            "interval": interval,
                            "x_offset": random.randint(-150, 150),  # Some variety
                        }
                    )
                wave["formations"] = formations

        self.wave_manager.set_waves(waves)
        self.active_formations = []
        self.formation_timers = {}

    def update(self, dt, game_time):
        """Update all enemies and handle spawning.

        Args:
            dt: Time elapsed since last update in seconds
            game_time: Current game time in seconds
        """
        # Update enemies and their shooting
        self._update_enemies(dt, game_time)

        # Process formation spawns
        self._process_formation_spawns(dt)

    def _update_enemies(self, dt, game_time):
        """Update enemies and their shooting.

        Args:
            dt: Time elapsed since last update in seconds
            game_time: Current game time in seconds
        """
        # Update enemies and handle enemy shooting
        for enemy in self.enemies:
            enemy.update(dt)
            # Let shooter enemies shoot
            if hasattr(enemy, "can_shoot") and enemy.can_shoot:
                if enemy.shoot(game_time, self.enemy_projectiles):
                    # Add new projectiles to all_sprites
                    for proj in self.enemy_projectiles:
                        if proj not in self.all_sprites:
                            self.all_sprites.add(proj)

        # Update active formations and remove completed ones
        self.active_formations = [f for f in self.active_formations if not f.complete]

    def _process_formation_spawns(self, dt):
        """Process formation spawning for the current wave.

        Args:
            dt: Time elapsed since last update in seconds
        """
        current_wave = self.wave_manager.get_current_wave()
        if not current_wave:
            return

        # Process existing formations
        for formation in list(self.active_formations):
            result = formation.update(dt)
            if result:
                spawn, x_pos = result
                if spawn:
                    self._spawn_enemy(formation.enemy_type, x_pos)

        # Check if we need to start new formations
        if "formations" in current_wave:
            for formation_def in current_wave.get("formations", []):
                formation_key = f"{formation_def['type']}_{formation_def['enemy_type']}"

                # Initialize timer if not exists
                if formation_key not in self.formation_timers:
                    self.formation_timers[formation_key] = 0

                # Update timer
                self.formation_timers[formation_key] += dt

                # Check if it's time to spawn a new formation
                if self.formation_timers[formation_key] >= formation_def["interval"]:
                    self.formation_timers[formation_key] = 0

                    # Create a new formation
                    formation = FormationPattern(
                        FormationType(formation_def["type"]),
                        formation_def["enemy_type"],
                        formation_def["count"],
                        self.screen_width,
                        spawn_delay=0.2,  # Spawn one enemy every 0.2 seconds
                        x_offset=formation_def.get("x_offset", 0),
                    )
                    self.active_formations.append(formation)

    def _spawn_enemy(self, enemy_type="basic", x_pos=None):
        """Spawn a new enemy at the specified position.

        Args:
            enemy_type (str): Type of enemy to spawn
            x_pos (int, optional): X position to spawn at. If None, random position.
        """
        if x_pos is None:
            x_pos = random.randint(50, self.screen_width - 50)

        if enemy_type == "basic":
            enemy = BasicEnemy(x_pos, -50)
        elif enemy_type == "zigzag":
            enemy = ZigzagEnemy(x_pos, -50)
        elif enemy_type == "shooter":
            enemy = ShooterEnemy(x_pos, -50)
        elif enemy_type == "heavy":
            enemy = HeavyBomber(x_pos, -50)
        elif enemy_type == "dart":
            enemy = DartEnemy(x_pos, -50)
        elif enemy_type == "shield":
            enemy = ShieldBearerEnemy(x_pos, -50)
        else:
            enemy = BasicEnemy(x_pos, -50)

        self.enemies.add(enemy)
        self.all_sprites.add(enemy)

    def advance_wave(self):
        """Advance to the next wave if possible.

        Returns:
            bool: True if successfully advanced, False if already at last wave
        """
        result = self.wave_manager.advance_wave()
        if result:
            self.formation_timers = {}  # Reset timers for new wave
            self.active_formations = []
        return result

    def get_current_wave_index(self):
        """Get the current wave index.

        Returns:
            int: Current wave index (0-based)
        """
        return self.wave_manager.get_current_wave_index()

    def get_total_waves(self):
        """Get the total number of waves.

        Returns:
            int: Total number of waves
        """
        return self.wave_manager.get_total_waves()

    def update_wave_timer(self, dt):
        """Update the wave timer.

        Args:
            dt: Time elapsed since last update in seconds

        Returns:
            bool: True if wave changed, False otherwise
        """
        wave_changed = self.wave_manager.update_wave_timer(dt)
        if wave_changed:
            self.formation_timers = {}  # Reset timers for new wave
            self.active_formations = []
        return wave_changed

    def clear_enemies(self):
        """Clear all enemies from the screen."""
        for enemy in self.enemies:
            enemy.kill()
        self.active_formations = []

    def reset(self):
        """Reset the enemy manager state."""
        self.wave_manager.reset()
        self.formation_timers = {}
        self.active_formations = []
