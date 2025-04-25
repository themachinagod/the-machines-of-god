"""
Player class for Machines of God game.
"""

import pygame


class PlayerProjectile(pygame.sprite.Sprite):
    """Projectile fired by the player."""

    def __init__(self, x, y, speed=-400, damage=1):
        """Initialize a projectile.

        Args:
            x (int): X position
            y (int): Y position
            speed (int): Speed in pixels per second
                (negative for upward movement)
            damage (int): Damage amount
        """
        super().__init__()
        self.image = pygame.Surface((8, 20), pygame.SRCALPHA)

        # Create a more visible laser effect
        pygame.draw.line(self.image, (255, 255, 100), (4, 0), (4, 20), 4)
        pygame.draw.line(self.image, (255, 255, 255), (4, 0), (4, 20), 2)

        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.velocity = pygame.math.Vector2(0, speed)
        self.damage = damage

    def update(self, dt):
        """Update projectile position.

        Args:
            dt (float): Time elapsed since last update
        """
        self.rect.y += self.velocity.y * dt

        # Remove if off screen
        if self.rect.bottom < 0:
            self.kill()


class PlayerMissile(pygame.sprite.Sprite):
    """Homing missile fired by player."""

    def __init__(self, x, y, speed=-200, damage=5, target=None):
        """Initialize a missile.

        Args:
            x (int): X position
            y (int): Y position
            speed (int): Speed in pixels per second
            damage (int): Damage amount
            target (pygame.sprite.Sprite): Target to track
        """
        super().__init__()
        self.image = pygame.Surface((10, 25), pygame.SRCALPHA)

        # Draw missile body
        pygame.draw.rect(self.image, (100, 100, 100), (3, 5, 4, 15))
        pygame.draw.polygon(self.image, (100, 100, 100), [(3, 5), (5, 0), (7, 5)])

        # Draw missile exhaust
        pygame.draw.rect(self.image, (255, 120, 50), (4, 20, 2, 5))

        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y

        self.position = pygame.math.Vector2(x, y)
        self.velocity = pygame.math.Vector2(0, speed)
        self.acceleration = pygame.math.Vector2(0, 0)
        self.max_speed = speed
        self.damage = damage
        self.target = target
        self.turn_rate = 5.0  # How fast the missile can turn

    def update(self, dt):
        """Update missile position.

        Args:
            dt (float): Time elapsed since last update
        """
        # Track target if available
        if self.target and self.target.alive():
            # Calculate direction to target
            target_pos = pygame.math.Vector2(self.target.rect.centerx, self.target.rect.centery)
            direction = target_pos - self.position

            # Normalize and scale
            if direction.length() > 0:
                direction.normalize_ip()
                direction *= self.turn_rate * 100 * dt

                # Add to velocity with limit
                self.velocity += direction
                if self.velocity.length() > abs(self.max_speed):
                    self.velocity.normalize_ip()
                    self.velocity *= abs(self.max_speed)

        # Update position
        self.position += self.velocity * dt
        self.rect.centerx = int(self.position.x)
        self.rect.centery = int(self.position.y)

        # Remove if off screen
        screen_height = pygame.display.get_surface().get_size()[1]
        if (
            self.rect.bottom < 0
            or self.rect.top > screen_height
            or self.rect.right < 0
            or self.rect.left > pygame.display.get_surface().get_size()[0]
        ):
            self.kill()


class Player(pygame.sprite.Sprite):
    """Player spacecraft controlled by the user."""

    def __init__(self, x, y):
        """Initialize the player.

        Args:
            x (int): Initial x position
            y (int): Initial y position
        """
        super().__init__()

        # Create a placeholder sprite (will be replaced with an image later)
        self.image = pygame.Surface((50, 50), pygame.SRCALPHA)

        # Draw a better looking spaceship
        # Main body
        pygame.draw.polygon(self.image, (120, 180, 255), [(25, 0), (10, 40), (40, 40)])
        # Wings
        pygame.draw.polygon(self.image, (70, 130, 200), [(0, 50), (10, 40), (15, 50)])
        pygame.draw.polygon(self.image, (70, 130, 200), [(50, 50), (40, 40), (35, 50)])
        # Thrusters
        pygame.draw.rect(self.image, (255, 150, 50), (20, 42, 10, 8))

        # Get the rect for positioning
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

        # Component upgrade levels
        self.upgrades = {
            "hull": 0,
            "engine": 0,
            "thruster": 0,
            "primary": 0,
            "shield": 0,
            "secondary": 0,
            "magnet": 0,
        }

        # Movement properties
        self.vert_speed = 250  # Level 0 vertical speed
        self.lat_speed = 250  # Level 0 lateral speed
        self.velocity = pygame.math.Vector2(0, 0)

        # Health and shield properties
        self.max_health = 50  # Level 0 health
        self.health = self.max_health
        self.max_shield = 0  # Level 0 shield
        self.shield = 0
        self.shield_recharge_rate = 0  # Points per second
        self.lives = 3

        # Weapon properties
        self.primary_level = 0
        self.primary_pattern = "single_slow"
        self.primary_cooldown = 0.5  # seconds between shots
        self.primary_last_shot = 0

        # Secondary weapon (missiles)
        self.secondary_level = 0
        self.missile_count = 0
        self.missile_cooldown = 0
        self.missile_last_shot = 0

        # Magnet properties
        self.magnet_radius = 0

        # Score
        self.score = 0

    def update_stats(self):
        """Update all stats based on upgrade levels."""
        # This would be called whenever upgrades change
        # Currently implemented through direct setting in ShopState
        pass

    def update(self, dt, keys):
        """Update the player's position and state.

        Args:
            dt (float): Time elapsed since last update in seconds
            keys (dict): Dictionary of pressed keys
        """
        # Reset velocity
        self.velocity.x = 0
        self.velocity.y = 0

        # Movement controls - use appropriate speed values
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.velocity.x = -self.lat_speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.velocity.x = self.lat_speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.velocity.y = -self.vert_speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.velocity.y = self.vert_speed

        # Normalize diagonal movement to prevent faster diagonal speed
        if self.velocity.length() > 0:
            self.velocity.normalize_ip()
            self.velocity.x *= self.lat_speed
            self.velocity.y *= self.vert_speed

        # Update position
        self.rect.x += self.velocity.x * dt
        self.rect.y += self.velocity.y * dt

        # Keep player on screen
        screen_width, screen_height = pygame.display.get_surface().get_size()

        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > screen_width:
            self.rect.right = screen_width

        if self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > screen_height:
            self.rect.bottom = screen_height

        # Shield recharge
        if self.shield < self.max_shield and self.shield_recharge_rate > 0:
            self.shield = min(self.max_shield, self.shield + self.shield_recharge_rate * dt)

    def shoot(self, current_time, projectile_group):
        """Create projectiles based on primary weapon level.

        Args:
            current_time (float): Current game time in seconds
            projectile_group (pygame.sprite.Group): Group to add projectiles to

        Returns:
            bool: True if projectiles were created, False otherwise
        """
        # Check cooldown
        if current_time - self.primary_last_shot < self.primary_cooldown:
            return False

        self.primary_last_shot = current_time

        # Create projectiles based on weapon pattern
        if self.primary_pattern == "single_slow":
            # Single slow shot
            bullet = PlayerProjectile(self.rect.centerx, self.rect.top)
            projectile_group.add(bullet)
        elif self.primary_pattern == "single_medium":
            # Single medium rate shot
            bullet = PlayerProjectile(self.rect.centerx, self.rect.top)
            projectile_group.add(bullet)
            # Faster cooldown handled by the shop
        elif self.primary_pattern == "double":
            # Double shot (side by side)
            left = PlayerProjectile(self.rect.centerx - 10, self.rect.top)
            right = PlayerProjectile(self.rect.centerx + 10, self.rect.top)
            projectile_group.add(left, right)
        elif self.primary_pattern == "triple":
            # Triple shot (spread)
            left = PlayerProjectile(self.rect.centerx - 15, self.rect.top)
            left.velocity = pygame.math.Vector2(-50, left.velocity.y)

            center = PlayerProjectile(self.rect.centerx, self.rect.top)

            right = PlayerProjectile(self.rect.centerx + 15, self.rect.top)
            right.velocity = pygame.math.Vector2(50, right.velocity.y)

            projectile_group.add(left, center, right)
        elif self.primary_pattern == "quad":
            # Quad shot (2x2 pattern)
            top_left = PlayerProjectile(self.rect.centerx - 10, self.rect.top)
            top_right = PlayerProjectile(self.rect.centerx + 10, self.rect.top)

            bottom_left = PlayerProjectile(self.rect.centerx - 10, self.rect.top + 15)
            bottom_right = PlayerProjectile(self.rect.centerx + 10, self.rect.top + 15)

            projectile_group.add(top_left, top_right, bottom_left, bottom_right)
        elif self.primary_pattern == "five":
            # Five shot (X pattern)
            center = PlayerProjectile(self.rect.centerx, self.rect.top)

            top_left = PlayerProjectile(self.rect.centerx - 15, self.rect.top)
            top_left.velocity = pygame.math.Vector2(-50, top_left.velocity.y)

            top_right = PlayerProjectile(self.rect.centerx + 15, self.rect.top)
            top_right.velocity = pygame.math.Vector2(50, top_right.velocity.y)

            far_left = PlayerProjectile(self.rect.centerx - 25, self.rect.top + 10)
            far_left.velocity = pygame.math.Vector2(-100, far_left.velocity.y)

            far_right = PlayerProjectile(self.rect.centerx + 25, self.rect.top + 10)
            far_right.velocity = pygame.math.Vector2(100, far_right.velocity.y)

            projectile_group.add(center, top_left, top_right, far_left, far_right)

        return True

    def fire_missile(self, current_time, missile_group, target=None):
        """Fire missiles if available.

        Args:
            current_time (float): Current game time in seconds
            missile_group (pygame.sprite.Group): Group to add missiles to
            target (pygame.sprite.Sprite): Optional target for missile

        Returns:
            bool: True if missiles were fired, False otherwise
        """
        # Check if missiles are available
        if self.missile_count <= 0 or self.secondary_level <= 0:
            return False

        # Check cooldown
        if current_time - self.missile_last_shot < self.missile_cooldown:
            return False

        self.missile_last_shot = current_time

        # Fire missiles based on level
        if self.secondary_level == 1:
            # Single missile
            missile = PlayerMissile(self.rect.centerx, self.rect.top, target=target)
            missile_group.add(missile)
        else:  # Level 2 or 3
            # Dual missiles
            left = PlayerMissile(self.rect.centerx - 15, self.rect.top, target=target)
            right = PlayerMissile(self.rect.centerx + 15, self.rect.top, target=target)
            missile_group.add(left, right)

        return True

    def take_damage(self, amount):
        """Reduce player health by the specified amount.

        Args:
            amount (int): Amount of damage to take

        Returns:
            bool: True if the player is still alive, False otherwise
        """
        if self.shield > 0:
            # Shield absorbs damage
            if self.shield >= amount:
                self.shield -= amount
                return True
            else:
                # Shield is depleted, remaining damage goes to health
                remaining_damage = amount - self.shield
                self.shield = 0
                self.health -= remaining_damage
        else:
            # No shield, damage goes directly to health
            self.health -= amount

        # Check if player is still alive
        if self.health <= 0:
            self.health = 0  # Prevent health from going negative
            self.lives -= 1

            # Return false if player is out of lives
            if self.lives <= 0:
                return False

            # Respawn with full health if lives remain
            self.health = self.max_health

        return True
