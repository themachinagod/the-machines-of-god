"""
Player class for Machines of God game.
"""

import math
import os

import pygame

# Define constants
COLOR_PROJECTILE = (255, 255, 100)


class PlayerProjectile(pygame.sprite.Sprite):
    """Player projectile class."""

    def __init__(self, x, y, direction_x, direction_y, damage, is_missile, speed=500):
        """Initialize player projectile.

        Args:
            x (int): X-coordinate
            y (int): Y-coordinate
            direction_x (float): X direction vector component
            direction_y (float): Y direction vector component
            damage (int): Damage the projectile deals
            is_missile (bool): True if this is a missile
            speed (int, optional): Speed of the projectile. Defaults to 500.
        """
        super().__init__()
        self.image = pygame.Surface((4, 12))
        self.image.fill(COLOR_PROJECTILE)

        # For angled projectiles, adjust the image
        if direction_x != 0:
            # Rotate the image based on direction
            angle = math.degrees(math.atan2(direction_y, direction_x)) - 90
            self.image = pygame.transform.rotate(self.image, angle)

        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

        # Normalize the direction if needed
        dir_length = math.sqrt(direction_x**2 + direction_y**2)
        if dir_length > 0:
            direction_x /= dir_length
            direction_y /= dir_length

        # Set velocity based on direction and speed
        self.velocity = pygame.math.Vector2(direction_x * speed, direction_y * speed)

        self.damage = damage
        self.is_missile = is_missile

    def update(self, dt):
        """Update projectile position.

        Args:
            dt (float): Time elapsed since last frame
        """
        # Move the projectile
        self.rect.x += self.velocity.x * dt
        self.rect.y += self.velocity.y * dt

        # Remove if off screen
        screen_width, screen_height = pygame.display.get_surface().get_size()
        if (
            self.rect.bottom < 0
            or self.rect.top > screen_height
            or self.rect.right < 0
            or self.rect.left > screen_width
        ):
            self.kill()


class PlayerMissile(pygame.sprite.Sprite):
    """Homing missile fired by player."""

    def __init__(self, x, y, direction_x, direction_y, damage=5, target=None, speed=400):
        """Initialize a missile.

        Args:
            x (int): X position
            y (int): Y position
            direction_x (float): X direction vector component
            direction_y (float): Y direction vector component
            damage (int): Damage amount
            target (pygame.sprite.Sprite): Target to track
            speed (int): Speed in pixels per second
        """
        super().__init__()
        self.image = pygame.Surface((10, 25), pygame.SRCALPHA)

        # Draw missile body
        pygame.draw.rect(self.image, (100, 100, 100), (3, 5, 4, 15))
        pygame.draw.polygon(self.image, (100, 100, 100), [(3, 5), (5, 0), (7, 5)])

        # Draw missile exhaust
        pygame.draw.rect(self.image, (255, 120, 50), (4, 20, 2, 5))

        # Rotate the image based on direction
        if direction_x != 0 or direction_y != 0:
            angle = math.degrees(math.atan2(direction_y, direction_x)) - 90
            self.image = pygame.transform.rotate(self.image, angle)

        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

        self.position = pygame.math.Vector2(x, y)

        # Normalize the direction if needed
        dir_length = math.sqrt(direction_x**2 + direction_y**2)
        if dir_length > 0:
            direction_x /= dir_length
            direction_y /= dir_length

        # Initial velocity in the direction specified
        self.velocity = pygame.math.Vector2(direction_x * speed, direction_y * speed)
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

                # Update missile rotation to match direction
                angle = math.degrees(math.atan2(self.velocity.y, self.velocity.x)) - 90
                self.image = pygame.transform.rotate(
                    pygame.Surface((10, 25), pygame.SRCALPHA), angle
                )

                # Redraw missile on rotated surface
                pygame.draw.rect(self.image, (100, 100, 100), (3, 5, 4, 15))
                pygame.draw.polygon(self.image, (100, 100, 100), [(3, 5), (5, 0), (7, 5)])
                pygame.draw.rect(self.image, (255, 120, 50), (4, 20, 2, 5))

                # Update rect
                old_center = self.rect.center
                self.rect = self.image.get_rect()
                self.rect.center = old_center

        # Update position
        self.position += self.velocity * dt
        self.rect.centerx = int(self.position.x)
        self.rect.centery = int(self.position.y)

        # Remove if off screen
        screen_width, screen_height = pygame.display.get_surface().get_size()
        if (
            self.rect.bottom < 0
            or self.rect.top > screen_height
            or self.rect.right < 0
            or self.rect.left > screen_width
        ):
            self.kill()


class Player(pygame.sprite.Sprite):
    """Player spacecraft controlled by the user."""

    def __init__(self, x, y):
        """Initialize the player.

        Args:
            x (int): Initial x position.
            y (int): Initial y position.
        """
        super().__init__()

        # Track screen boundaries
        self.screen_width = 0
        self.screen_height = 0

        # Load the player ship image instead of drawing a shape
        try:
            # Get the path to the assets directory
            assets_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "assets"
            )
            ship_path = os.path.join(assets_path, "sprites", "playership.png")

            # Load the image with alpha channel
            self.original_image = pygame.image.load(ship_path).convert_alpha()

            # Scale the image to 37.5% of original size (25% smaller than before)
            scale_factor = 0.375  # 75% of previous 0.5 scale
            original_size = self.original_image.get_size()
            new_size = (int(original_size[0] * scale_factor), int(original_size[1] * scale_factor))
            self.original_image = pygame.transform.scale(self.original_image, new_size)

            self.image = self.original_image.copy()
        except Exception as e:
            print(f"Error loading player ship image: {e}")
            # Fallback to a simple shape if image loading fails
            self.image = pygame.Surface([32, 32], pygame.SRCALPHA)
            ship_color = (0, 255, 255)  # Cyan color
            pygame.draw.polygon(self.image, ship_color, [(16, 4), (4, 28), (28, 28)])
            pygame.draw.rect(self.image, (100, 100, 255), (12, 26, 8, 6))  # Blue exhaust
            pygame.draw.rect(self.image, (200, 255, 255), (14, 12, 4, 6))  # Light cyan
            pygame.draw.line(self.image, (0, 200, 200), (4, 28), (16, 18), 2)
            pygame.draw.line(self.image, (0, 200, 200), (28, 28), (16, 18), 2)
            self.original_image = self.image.copy()

        # Player rect
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

        # Movement
        self.velocity = pygame.math.Vector2(0, 0)
        self.lat_speed = 150
        self.vert_speed = 150

        # Rotation
        self.angle = 0  # Angle in degrees, 0 = up, increases clockwise
        self.rotation_speed = 180  # Degrees per second
        self.return_to_center_speed = 90  # Speed at which angle returns to 0 when keys are released
        self.rotation_pause_time = 0.8  # Seconds to wait before starting snap back
        self.rotation_pause_timer = 0  # Timer to track pause duration

        # Health and lives
        self.max_health = 100
        self.health = self.max_health
        self.lives = 3

        # Upgrades (all start at 0 = not unlocked)
        self.upgrades = {
            "primary": 0,
            "secondary": 0,
            "shield": 0,
            "magnet": 0,
        }

        # Primary weapon (projectiles)
        self.primary_level = 0  # Used to determine weapon pattern and damage
        self.primary_damage = 1  # Base damage of projectiles
        self.primary_cooldown = 0.5  # Time between shots
        self.primary_last_shot = 0  # Time of last shot
        self.primary_pattern = "single_slow"  # Current weapon pattern

        # Shield properties
        self.max_shield = 0
        self.shield = 0
        self.shield_recharge_rate = 0

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

    def _handle_rotation(self, dt, keys):
        """Handle ship rotation and auto-centering.

        Args:
            dt (float): Time elapsed since last update in seconds
            keys (dict): Dictionary of pressed keys

        Returns:
            bool: True if the player is actively rotating, False otherwise
        """
        rotating = False
        if keys[pygame.K_COMMA]:
            self.angle = (self.angle - self.rotation_speed * dt) % 360
            self._update_image()
            rotating = True
            # Reset pause timer when rotating
            self.rotation_pause_timer = 0

        if keys[pygame.K_PERIOD]:
            self.angle = (self.angle + self.rotation_speed * dt) % 360
            self._update_image()
            rotating = True
            # Reset pause timer when rotating
            self.rotation_pause_timer = 0

        # If not rotating and angle is not 0, handle return to center
        if not rotating and self.angle != 0:
            # Update pause timer
            self.rotation_pause_timer += dt

            # Only start returning to center after pause time has elapsed
            if self.rotation_pause_timer >= self.rotation_pause_time:
                # Find shortest direction back to 0
                clockwise_distance = (360 - self.angle) % 360
                counterclockwise_distance = self.angle

                # Determine which direction is shorter
                if clockwise_distance < counterclockwise_distance:
                    # Rotate clockwise
                    rotation_amount = min(self.return_to_center_speed * dt, clockwise_distance)
                    self.angle = (self.angle + rotation_amount) % 360
                else:
                    # Rotate counter-clockwise
                    rotation_amount = min(
                        self.return_to_center_speed * dt, counterclockwise_distance
                    )
                    self.angle = (self.angle - rotation_amount) % 360

                # Snap to exactly 0 if we're very close
                if self.angle > 350 or self.angle < 10:
                    self.angle = 0

                self._update_image()

        return rotating

    def set_screen_boundaries(self, width, height):
        """Set the screen boundaries for the player.

        Args:
            width (int): Screen width
            height (int): Screen height
        """
        self.screen_width = width
        self.screen_height = height

    def update(self, dt, keys):
        """Update the player's position and state.

        Args:
            dt (float): Time elapsed since last update in seconds
            keys (dict): Dictionary of pressed keys
        """
        # Handle rotation with auto-centering
        self._handle_rotation(dt, keys)

        # Reset velocity
        self.velocity.x = 0
        self.velocity.y = 0

        # Calculate forward and sideways directions based on angle
        # 0 degrees = up, 90 degrees = right, etc.
        forward_x = math.sin(math.radians(self.angle))
        forward_y = -math.cos(math.radians(self.angle))
        right_x = math.sin(math.radians(self.angle + 90))
        right_y = -math.cos(math.radians(self.angle + 90))

        # Movement controls - use appropriate speed values
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            # Move forward
            self.velocity.x += forward_x * self.lat_speed
            self.velocity.y += forward_y * self.vert_speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            # Move backward
            self.velocity.x -= forward_x * self.lat_speed
            self.velocity.y -= forward_y * self.vert_speed
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            # Strafe left
            self.velocity.x -= right_x * self.lat_speed
            self.velocity.y -= right_y * self.vert_speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            # Strafe right
            self.velocity.x += right_x * self.lat_speed
            self.velocity.y += right_y * self.vert_speed

        # Normalize diagonal movement to prevent faster diagonal speed
        if self.velocity.length() > 0:
            self.velocity.normalize_ip()
            self.velocity.x *= self.lat_speed
            self.velocity.y *= self.vert_speed

        # Update position
        self.rect.x += self.velocity.x * dt
        self.rect.y += self.velocity.y * dt

        # Keep player on screen - use our stored boundaries
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > self.screen_width and self.screen_width > 0:
            self.rect.right = self.screen_width

        if self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > self.screen_height and self.screen_height > 0:
            self.rect.bottom = self.screen_height

        # Shield recharge
        if self.shield < self.max_shield and self.shield_recharge_rate > 0:
            self.shield = min(self.max_shield, self.shield + self.shield_recharge_rate * dt)

    def _update_image(self):
        """Update the image based on the current angle."""
        # Rotate the original image
        self.image = pygame.transform.rotate(self.original_image, -self.angle)
        # Keep the center position
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center

    def shoot(self, current_time, projectile_group):
        """Fire projectiles if the cooldown has elapsed.

        Args:
            current_time (float): Current game time in seconds
            projectile_group (pygame.sprite.Group): Group to add projectiles to
        """
        # Debug information for weapon firing
        print(f"DEBUG: Attempting to shoot with pattern: {self.primary_pattern}")
        print(
            f"DEBUG: Cooldown status - Last shot: {self.primary_last_shot}, "
            f"Current: {current_time}, "
            f"Diff: {current_time - self.primary_last_shot}, "
            f"Cooldown: {self.primary_cooldown}"
        )

        # Check if cooldown has elapsed
        if current_time - self.primary_last_shot < self.primary_cooldown:
            return False  # Still on cooldown

        # Calculate projectile direction based on player angle
        direction_x = math.sin(math.radians(self.angle))
        direction_y = -math.cos(math.radians(self.angle))

        # Update last shot time
        self.primary_last_shot = current_time

        # Calculate the position at the front of the ship
        # Get half the height of the ship for the offset
        ship_offset = self.rect.height // 2

        # Calculate the position at the front of the ship based on current angle and offset
        x = self.rect.centerx + direction_x * ship_offset
        y = self.rect.centery + direction_y * ship_offset

        # Fix for potential None or invalid pattern - ensure we default to basic pattern if needed
        if not hasattr(self, "primary_pattern") or self.primary_pattern is None:
            print("DEBUG: primary_pattern was None! Setting to default 'single_slow'")
            self.primary_pattern = "single_slow"

        print(f"DEBUG: Using weapon pattern: {self.primary_pattern}")

        # Create projectiles based on pattern
        if self.primary_pattern == "single_slow":
            # Single projectile
            projectile = PlayerProjectile(
                x, y, direction_x, direction_y, self.primary_damage, False
            )
            projectile_group.add(projectile)

        elif self.primary_pattern == "single_medium":
            # Single medium-speed projectile (faster than slow, but not as fast as fast)
            print("DEBUG: Firing single_medium projectile")
            projectile = PlayerProjectile(
                x, y, direction_x, direction_y, self.primary_damage, False, speed=650
            )
            projectile_group.add(projectile)

        elif self.primary_pattern == "single_fast":
            # Single faster projectile
            projectile = PlayerProjectile(
                x, y, direction_x, direction_y, self.primary_damage, False, speed=800
            )
            projectile_group.add(projectile)

        elif self.primary_pattern == "double":
            # Two projectiles side by side
            # Calculate offsets perpendicular to direction
            perp_x = math.sin(math.radians(self.angle + 90))
            perp_y = -math.cos(math.radians(self.angle + 90))

            # Create two projectiles offset to either side
            offset = 10  # Pixels
            projectile1 = PlayerProjectile(
                x + perp_x * offset,
                y + perp_y * offset,
                direction_x,
                direction_y,
                self.primary_damage,
                False,
            )
            projectile2 = PlayerProjectile(
                x - perp_x * offset,
                y - perp_y * offset,
                direction_x,
                direction_y,
                self.primary_damage,
                False,
            )
            projectile_group.add(projectile1)
            projectile_group.add(projectile2)

        elif self.primary_pattern == "triple":
            # Three projectiles in a spread
            projectile1 = PlayerProjectile(
                x, y, direction_x, direction_y, self.primary_damage, False
            )

            # Add angled projectiles (20 degrees to each side)
            angle1 = self.angle - 20
            angle2 = self.angle + 20

            dir1_x = math.sin(math.radians(angle1))
            dir1_y = -math.cos(math.radians(angle1))

            dir2_x = math.sin(math.radians(angle2))
            dir2_y = -math.cos(math.radians(angle2))

            projectile2 = PlayerProjectile(x, y, dir1_x, dir1_y, self.primary_damage, False)
            projectile3 = PlayerProjectile(x, y, dir2_x, dir2_y, self.primary_damage, False)

            projectile_group.add(projectile1)
            projectile_group.add(projectile2)
            projectile_group.add(projectile3)

        elif self.primary_pattern == "triple_narrow":
            # Three projectiles in a narrower spread
            projectile1 = PlayerProjectile(
                x, y, direction_x, direction_y, self.primary_damage, False
            )

            # Add angled projectiles (10 degrees to each side)
            angle1 = self.angle - 10
            angle2 = self.angle + 10

            dir1_x = math.sin(math.radians(angle1))
            dir1_y = -math.cos(math.radians(angle1))

            dir2_x = math.sin(math.radians(angle2))
            dir2_y = -math.cos(math.radians(angle2))

            projectile2 = PlayerProjectile(x, y, dir1_x, dir1_y, self.primary_damage, False)
            projectile3 = PlayerProjectile(x, y, dir2_x, dir2_y, self.primary_damage, False)

            projectile_group.add(projectile1)
            projectile_group.add(projectile2)
            projectile_group.add(projectile3)

        elif self.primary_pattern == "quad":
            # Four projectiles
            projectile1 = PlayerProjectile(
                x, y, direction_x, direction_y, self.primary_damage, False
            )

            # Add angled projectiles (15 degrees to each side)
            angle1 = self.angle - 15
            angle2 = self.angle + 15

            dir1_x = math.sin(math.radians(angle1))
            dir1_y = -math.cos(math.radians(angle1))

            dir2_x = math.sin(math.radians(angle2))
            dir2_y = -math.cos(math.radians(angle2))

            # Add a fourth projectile slightly behind or offset
            angle3 = self.angle - 180  # Behind
            dir3_x = math.sin(math.radians(angle3))
            dir3_y = -math.cos(math.radians(angle3))

            projectile2 = PlayerProjectile(x, y, dir1_x, dir1_y, self.primary_damage, False)
            projectile3 = PlayerProjectile(x, y, dir2_x, dir2_y, self.primary_damage, False)
            projectile4 = PlayerProjectile(x, y, dir3_x, dir3_y, self.primary_damage, False)

            projectile_group.add(projectile1)
            projectile_group.add(projectile2)
            projectile_group.add(projectile3)
            projectile_group.add(projectile4)

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
        self.missile_count -= 1  # Use one missile

        # Calculate missile direction based on player angle
        direction_x = math.sin(math.radians(self.angle))
        direction_y = -math.cos(math.radians(self.angle))

        # Calculate the position at the front of the ship
        ship_offset = self.rect.height // 2
        front_x = self.rect.centerx + direction_x * ship_offset
        front_y = self.rect.centery + direction_y * ship_offset

        # Fire missiles based on level
        if self.secondary_level == 1:
            # Single missile
            missile = PlayerMissile(
                front_x,
                front_y,
                direction_x,
                direction_y,
                damage=5,
                target=target,
            )
            missile_group.add(missile)
        else:  # Level 2 or 3
            # Calculate perpendicular offset
            perp_x = math.sin(math.radians(self.angle + 90))
            perp_y = -math.cos(math.radians(self.angle + 90))

            # Offset amount
            offset = 15

            # Dual missiles, offset to each side
            left = PlayerMissile(
                front_x + perp_x * offset,
                front_y + perp_y * offset,
                direction_x,
                direction_y,
                damage=5,
                target=target,
            )
            right = PlayerMissile(
                front_x - perp_x * offset,
                front_y - perp_y * offset,
                direction_x,
                direction_y,
                damage=5,
                target=target,
            )
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
