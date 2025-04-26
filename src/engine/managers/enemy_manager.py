"""
Enemy manager for handling enemy spawning and behavior.
"""

import random

from engine.managers.wave_manager import WaveManager
from entities.enemy import (
    BasicEnemy,
    DartEnemy,
    HeavyBomber,
    ShieldBearerEnemy,
    ShooterEnemy,
    ZigzagEnemy,
)


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

        # Enemy spawn timers
        self.enemy_spawn_timers = {}

    def set_waves(self, waves):
        """Set the wave definitions.

        Args:
            waves: List of wave definitions
        """
        self.wave_manager.set_waves(waves)
        self.enemy_spawn_timers = {}

    def update(self, dt, game_time):
        """Update all enemies and handle spawning.

        Args:
            dt: Time elapsed since last update in seconds
            game_time: Current game time in seconds
        """
        # Update enemies and their shooting
        self._update_enemies(dt, game_time)

        # Process wave spawns
        self._process_wave_spawns(dt)

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

    def _process_wave_spawns(self, dt):
        """Process enemy spawning for the current wave.

        Args:
            dt: Time elapsed since last update in seconds
        """
        current_wave = self.wave_manager.get_current_wave()
        if not current_wave:
            return

        for enemy_def in current_wave["enemies"]:
            enemy_type = enemy_def["type"]

            # Initialize timer if not exists
            if enemy_type not in self.enemy_spawn_timers:
                self.enemy_spawn_timers[enemy_type] = 0

            # Update timer
            self.enemy_spawn_timers[enemy_type] += dt

            # Check if it's time to spawn
            if self.enemy_spawn_timers[enemy_type] >= enemy_def["interval"]:
                self.enemy_spawn_timers[enemy_type] = 0

                # Spawn enemies based on count
                for _ in range(enemy_def["count"]):
                    self._spawn_enemy(enemy_type)

    def _spawn_enemy(self, enemy_type="basic"):
        """Spawn a new enemy at a random position.

        Args:
            enemy_type (str): Type of enemy to spawn
        """
        x = random.randint(50, self.screen_width - 50)

        if enemy_type == "basic":
            enemy = BasicEnemy(x, -50)
        elif enemy_type == "zigzag":
            enemy = ZigzagEnemy(x, -50)
        elif enemy_type == "shooter":
            enemy = ShooterEnemy(x, -50)
        elif enemy_type == "heavy":
            enemy = HeavyBomber(x, -50)
        elif enemy_type == "dart":
            enemy = DartEnemy(x, -50)
        elif enemy_type == "shield":
            enemy = ShieldBearerEnemy(x, -50)
        else:
            enemy = BasicEnemy(x, -50)

        self.enemies.add(enemy)
        self.all_sprites.add(enemy)

    def advance_wave(self):
        """Advance to the next wave if possible.

        Returns:
            bool: True if successfully advanced, False if already at last wave
        """
        result = self.wave_manager.advance_wave()
        if result:
            self.enemy_spawn_timers = {}  # Reset timers for new wave
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
            self.enemy_spawn_timers = {}  # Reset timers for new wave
        return wave_changed

    def clear_enemies(self):
        """Clear all enemies from the screen."""
        for enemy in self.enemies:
            enemy.kill()

    def reset(self):
        """Reset the enemy manager state."""
        self.wave_manager.reset()
        self.enemy_spawn_timers = {}
