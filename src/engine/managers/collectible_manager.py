"""
Collectible manager for handling collectible spawning and behavior.
"""

import random

from entities.collectible import HealthPack, ShieldPack, Star


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
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.all_sprites = all_sprites
        self.collectibles = collectibles_group

        # Spawn rates as percentages (should sum to 100)
        self.spawn_rates = {"star": 70, "health": 20, "shield": 10}

        # Spawn timing
        self.spawn_timer = 0
        self.spawn_interval = 2.0  # seconds between spawns

        # Magnet effect
        self.magnet_active = False
        self.magnet_position = (0, 0)
        self.magnet_radius = 200
        self.magnet_strength = 300

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

        for collectible in self.collectibles:
            # Calculate distance to magnet
            dx = mag_x - collectible.rect.centerx
            dy = mag_y - collectible.rect.centery
            distance = (dx**2 + dy**2) ** 0.5

            # Apply force if within radius
            if distance <= self.magnet_radius:
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

    def _spawn_random_collectible(self):
        """Spawn a random collectible based on spawn rates."""
        # Generate random position
        x = random.randint(50, self.screen_width - 50)
        y = random.randint(100, self.screen_height - 100)

        # Determine collectible type based on spawn rates
        collectible_type = self._select_collectible_type()

        # Create the collectible
        if collectible_type == "star":
            collectible = Star(x, y, value=random.randint(5, 15))
        elif collectible_type == "health":
            collectible = HealthPack(x, y)
        elif collectible_type == "shield":
            collectible = ShieldPack(x, y)
        else:
            collectible = Star(x, y)  # Default to star

        # Add to sprite groups
        self.collectibles.add(collectible)
        self.all_sprites.add(collectible)

    def _select_collectible_type(self):
        """Select a collectible type based on spawn rates.

        Returns:
            str: The selected collectible type
        """
        roll = random.randint(1, 100)
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
        # Validate total is 100%
        total = sum(rates.values())
        if abs(total - 100) > 0.001:  # Allow for floating point error
            # Normalize to 100
            self.spawn_rates = {k: v * 100 / total for k, v in rates.items()}
        else:
            self.spawn_rates = rates

    def activate_magnet(self, position, radius=200, strength=300):
        """Activate the magnet effect.

        Args:
            position: (x, y) position of the magnet center
            radius: Radius of effect in pixels
            strength: Strength of the magnet effect
        """
        self.magnet_active = True
        self.magnet_position = position
        self.magnet_radius = radius
        self.magnet_strength = strength

    def deactivate_magnet(self):
        """Deactivate the magnet effect."""
        self.magnet_active = False

    def clear_collectibles(self):
        """Remove all collectibles from the game."""
        for collectible in self.collectibles:
            collectible.kill()

    def reset(self):
        """Reset the collectible manager state."""
        self.spawn_timer = 0
        self.magnet_active = False

    def spawn_collectibles(self, x, y, bonus_chance=False):
        """Spawn collectibles at a specified position.

        Args:
            x (int): X position to spawn at
            y (int): Y position to spawn at
            bonus_chance (bool): If True, higher chance of spawning valuable collectibles
        """
        # Default 30% chance to spawn a collectible
        spawn_chance = 30
        if bonus_chance:
            spawn_chance = 50  # 50% with bonus

        # Roll for spawn
        if random.randint(1, 100) <= spawn_chance:
            # Determine collectible type based on spawn rates
            collectible_type = self._select_collectible_type()

            # Create the collectible
            if collectible_type == "star":
                collectible = Star(x, y, value=random.randint(5, 15))
            elif collectible_type == "health":
                collectible = HealthPack(x, y)
            elif collectible_type == "shield":
                collectible = ShieldPack(x, y)
            else:
                collectible = Star(x, y)  # Default to star

            # Add to sprite groups
            self.collectibles.add(collectible)
            self.all_sprites.add(collectible)
