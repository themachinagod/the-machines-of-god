"""
Collectible manager for handling collectible spawning and behavior.
"""

import random

from entities.collectible import HealthPack, ShieldPack, Star
from utils.logger import get_logger


class CollectibleManager:
    """Manages all collectible-related activities including spawning and behavior."""

    def __init__(self, screen_width, screen_height, all_sprites, collectibles_group):
        """Initialize the collectible manager.

        Args:
            screen_width: Width of the game screen
            screen_height: Height of the game screen
            all_sprites: Group containing all game sprites
            collectibles_group: Group containing collectible sprites
        """
        # Initialize logger
        self.logger = get_logger()
        self.logger.info("Initializing CollectibleManager")

        self.screen_width = screen_width
        self.screen_height = screen_height
        self.all_sprites = all_sprites
        self.collectibles = collectibles_group
        self.logger.debug("Screen dimensions: %dx%d", screen_width, screen_height)

        # Spawn rates as percentages (should sum to 100)
        self.spawn_rates = {"star": 70, "health": 20, "shield": 10}
        self.logger.debug("Initial spawn rates: %s", self.spawn_rates)

        # Spawn timing
        self.spawn_timer = 0
        self.spawn_interval = 2.0  # seconds between spawns
        self.logger.debug("Spawn interval set to %.2f seconds", self.spawn_interval)

        # Magnet effect
        self.magnet_active = False
        self.magnet_position = (0, 0)
        self.magnet_radius = 200
        self.magnet_strength = 300
        self.logger.debug(
            "Magnet settings - radius: %d, strength: %d", self.magnet_radius, self.magnet_strength
        )

        self.logger.info("CollectibleManager initialized successfully")

    def update(self, dt):
        """Update all collectibles and handle spawning.

        Args:
            dt: Time elapsed since last update in seconds
        """
        # Update all collectibles
        for collectible in self.collectibles:
            collectible.update(dt)

        # Update collectible positions with magnet effect if active
        if self.magnet_active:
            self.logger.debug("Applying magnet effect at position %s", self.magnet_position)
            self._apply_magnet_effect(dt)

        # Automatic spawning disabled - collectibles now only appear when enemies are destroyed
        # Uncomment the following lines to enable automatic spawning:
        # self.spawn_timer += dt
        # if self.spawn_timer >= self.spawn_interval:
        #     self.spawn_timer = 0
        #     self._spawn_random_collectible()

    def _apply_magnet_effect(self, dt):
        """Apply magnet effect to collectibles.

        Args:
            dt: Time elapsed since last update in seconds
        """
        mag_x, mag_y = self.magnet_position
        affected_count = 0

        for collectible in self.collectibles:
            # Calculate distance to magnet
            dx = mag_x - collectible.rect.centerx
            dy = mag_y - collectible.rect.centery
            distance = (dx**2 + dy**2) ** 0.5

            # Apply force if within radius
            if distance <= self.magnet_radius:
                affected_count += 1
                # Calculate normalized direction vector
                if distance > 0:  # Avoid division by zero
                    dx /= distance
                    dy /= distance

                # Force decreases linearly with distance
                force_factor = 1 - (distance / self.magnet_radius)
                speed = self.magnet_strength * force_factor * dt

                # Apply movement
                collectible.rect.x += dx * speed
                collectible.rect.y += dy * speed

        if affected_count > 0:
            self.logger.debug("Magnet affected %d collectibles", affected_count)

    def _spawn_random_collectible(self):
        """Spawn a random collectible based on spawn rates."""
        # Generate random position
        x = random.randint(50, self.screen_width - 50)
        y = random.randint(100, self.screen_height - 100)
        self.logger.debug("Spawning random collectible at position (%d, %d)", x, y)

        # Determine collectible type based on spawn rates
        collectible_type = self._select_collectible_type()
        self.logger.debug("Selected collectible type: %s", collectible_type)

        # Create the collectible
        if collectible_type == "star":
            value = random.randint(5, 15)
            collectible = Star(x, y, value=value)
            self.logger.debug("Created Star with value %d", value)
        elif collectible_type == "health":
            collectible = HealthPack(x, y)
            self.logger.debug("Created HealthPack")
        elif collectible_type == "shield":
            collectible = ShieldPack(x, y)
            self.logger.debug("Created ShieldPack")
        else:
            collectible = Star(x, y)  # Default to star
            self.logger.debug("Created default Star")

        # Add to sprite groups
        self.collectibles.add(collectible)
        self.all_sprites.add(collectible)

    def _select_collectible_type(self):
        """Select a collectible type based on spawn rates.

        Returns:
            str: The selected collectible type
        """
        roll = random.randint(1, 100)
        self.logger.debug("Collectible type roll: %d", roll)
        cumulative = 0

        for ctype, rate in self.spawn_rates.items():
            cumulative += rate
            if roll <= cumulative:
                return ctype

        return "star"  # Default

    def set_spawn_rates(self, rates):
        """Set the spawn rates for collectibles.

        Args:
            rates: Dictionary of spawn rates (should sum to 100)
        """
        self.logger.info("Setting new spawn rates: %s", rates)

        # Validate total is 100%
        total = sum(rates.values())
        if abs(total - 100) > 0.001:  # Allow for floating point error
            # Normalize to 100
            self.spawn_rates = {k: v * 100 / total for k, v in rates.items()}
            self.logger.debug("Normalized spawn rates to 100%%: %s", self.spawn_rates)
        else:
            self.spawn_rates = rates

        self.logger.debug("Spawn rates updated successfully")

    def activate_magnet(self, position, radius=200, strength=300):
        """Activate the magnet effect.

        Args:
            position: (x, y) position of the magnet center
            radius: Radius of effect in pixels
            strength: Strength of the magnet effect
        """
        self.logger.info(
            "Activating magnet at position %s with radius %d and strength %d",
            position,
            radius,
            strength,
        )
        self.magnet_active = True
        self.magnet_position = position
        self.magnet_radius = radius
        self.magnet_strength = strength

    def deactivate_magnet(self):
        """Deactivate the magnet effect."""
        self.logger.info("Deactivating magnet")
        self.magnet_active = False

    def clear_collectibles(self):
        """Remove all collectibles from the game."""
        count = len(self.collectibles)
        self.logger.info("Clearing %d collectibles", count)
        for collectible in self.collectibles:
            collectible.kill()

    def reset(self):
        """Reset the collectible manager state."""
        self.logger.info("Resetting CollectibleManager")
        self.spawn_timer = 0
        self.magnet_active = False

    def spawn_collectibles(self, x, y, bonus_chance=False):
        """Spawn collectibles at a specified position.

        Args:
            x (int): X position to spawn at
            y (int): Y position to spawn at
            bonus_chance (bool): If True, higher chance of spawning valuable collectibles
        """
        self.logger.debug(
            "Attempting to spawn collectible at (%d, %d), bonus chance: %s", x, y, bonus_chance
        )

        # Default 30% chance to spawn a collectible
        spawn_chance = 30
        if bonus_chance:
            spawn_chance = 50  # 50% with bonus

        # Roll for spawn
        roll = random.randint(1, 100)
        self.logger.debug("Spawn roll: %d (need <= %d)", roll, spawn_chance)

        if roll <= spawn_chance:
            # Determine collectible type based on spawn rates
            collectible_type = self._select_collectible_type()
            self.logger.debug("Spawning collectible of type: %s", collectible_type)

            # Create the collectible
            if collectible_type == "star":
                value = random.randint(5, 15)
                collectible = Star(x, y, value=value)
                self.logger.debug("Created Star with value %d", value)
            elif collectible_type == "health":
                collectible = HealthPack(x, y)
                self.logger.debug("Created HealthPack")
            elif collectible_type == "shield":
                collectible = ShieldPack(x, y)
                self.logger.debug("Created ShieldPack")
            else:
                collectible = Star(x, y)  # Default to star
                self.logger.debug("Created default Star")

            # Add to sprite groups
            self.collectibles.add(collectible)
            self.all_sprites.add(collectible)
        else:
            self.logger.debug("No collectible spawned (roll failed)")
