"""
Player class for Machines of God game.
"""

import pygame


class PlayerProjectile(pygame.sprite.Sprite):
    """Projectile fired by the player."""

    def __init__(self, x, y, speed=-400):
        """Initialize a projectile.

        Args:
            x (int): X position
            y (int): Y position
            speed (int): Speed in pixels per second
                (negative for upward movement)
        """
        super().__init__()
        self.image = pygame.Surface((5, 15))
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.velocity = pygame.math.Vector2(0, speed)

    def update(self, dt):
        """Update projectile position.

        Args:
            dt (float): Time elapsed since last update
        """
        self.rect.y += self.velocity.y * dt

        # Remove if off screen
        if self.rect.bottom < 0:
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
        self.image = pygame.Surface((50, 50))
        self.image.fill((0, 255, 0))

        # Draw a simple spaceship shape
        points = [(25, 0), (0, 50), (25, 35), (50, 50)]
        pygame.draw.polygon(self.image, (200, 200, 255), points)

        # Set transparent color
        self.image.set_colorkey((0, 255, 0))

        # Get the rect for positioning
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

        # Movement attributes
        self.speed = 300  # pixels per second
        self.velocity = pygame.math.Vector2(0, 0)

        # Gameplay attributes
        self.health = 100
        self.shield = 0
        self.lives = 3
        self.score = 0

        # Weapon attributes
        self.weapon_level = 1
        self.fire_rate = 0.2  # seconds between shots
        self.last_shot_time = 0

    def update(self, dt, keys):
        """Update the player's position and state.

        Args:
            dt (float): Time elapsed since last update in seconds
            keys (dict): Dictionary of pressed keys
        """
        # Reset velocity
        self.velocity.x = 0
        self.velocity.y = 0

        # Movement controls
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.velocity.x = -self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.velocity.x = self.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.velocity.y = -self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.velocity.y = self.speed

        # Normalize diagonal movement to prevent faster diagonal speed
        if self.velocity.length() > 0:
            self.velocity.normalize_ip()
            self.velocity *= self.speed

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

    def shoot(self, current_time, projectile_group):
        """Create a projectile if enough time has passed since the last shot.

        Args:
            current_time (float): Current game time in seconds
            projectile_group (pygame.sprite.Group): Group to add projectiles to

        Returns:
            bool: True if a projectile was created, False otherwise
        """
        if current_time - self.last_shot_time >= self.fire_rate:
            self.last_shot_time = current_time

            # Create a proper projectile
            bullet = PlayerProjectile(self.rect.centerx, self.rect.top)
            projectile_group.add(bullet)
            return True

        return False

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
            self.lives -= 1
            if self.lives > 0:
                # Respawn with full health
                self.health = 100
                return True
            else:
                # Game over
                return False

        return True
