"""
Enemy classes for Machines of God game.
"""

import math
import random

import pygame


class Enemy(pygame.sprite.Sprite):
    """Base class for enemy entities."""

    def __init__(self, x, y, health=10, speed=100):
        """Initialize the enemy.

        Args:
            x (int): Initial x position
            y (int): Initial y position
            health (int): Initial health points
            speed (int): Movement speed in pixels per second
        """
        super().__init__()

        # Create a placeholder sprite (will be replaced with an image later)
        self.image = pygame.Surface((40, 40))
        self.image.fill((255, 0, 0))

        # Get the rect for positioning
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # Enemy attributes
        self.health = health
        self.speed = speed
        self.value = 100  # Score value when destroyed

        # Movement pattern
        self.movement_type = "linear"  # Can be "linear", "zigzag", "circular"
        self.direction = pygame.math.Vector2(0, 1)  # Down by default
        self.timer = 0

    def update(self, dt):
        """Update the enemy's position and state.

        Args:
            dt (float): Time elapsed since last update in seconds
        """
        # Update movement based on pattern
        if self.movement_type == "linear":
            self._linear_movement(dt)
        elif self.movement_type == "zigzag":
            self._zigzag_movement(dt)
        elif self.movement_type == "circular":
            self._circular_movement(dt)

        # Check if enemy is off-screen
        screen_height = pygame.display.get_surface().get_size()[1]
        if self.rect.top > screen_height:
            self.kill()

    def _linear_movement(self, dt):
        """Basic downward movement.

        Args:
            dt (float): Time elapsed since last update in seconds
        """
        self.rect.y += self.speed * dt

    def _zigzag_movement(self, dt):
        """Zigzag movement pattern.

        Args:
            dt (float): Time elapsed since last update in seconds
        """
        self.timer += dt
        # Oscillate horizontal direction using sine wave
        self.direction.x = math.sin(self.timer * 3) * 0.5
        self.direction.y = 1

        # Normalize and apply speed
        if self.direction.length() > 0:
            self.direction.normalize_ip()

        # Update position
        self.rect.x += self.direction.x * self.speed * dt
        self.rect.y += self.direction.y * self.speed * dt

    def _circular_movement(self, dt):
        """Circular movement pattern.

        Args:
            dt (float): Time elapsed since last update in seconds
        """
        self.timer += dt
        # Create circular motion using sin and cos
        self.direction.x = math.sin(self.timer * 2) * 0.7
        self.direction.y = 0.5 + math.cos(self.timer * 2) * 0.3

        # Normalize and apply speed
        if self.direction.length() > 0:
            self.direction.normalize_ip()

        # Update position
        self.rect.x += self.direction.x * self.speed * dt
        self.rect.y += self.direction.y * self.speed * dt

    def take_damage(self, amount):
        """Reduce enemy health by the specified amount.

        Args:
            amount (int): Amount of damage to take

        Returns:
            bool: True if the enemy is destroyed, False otherwise
        """
        self.health -= amount
        if self.health <= 0:
            self.kill()
            return True
        return False

    def shoot(self, current_time, projectile_group):
        """Method to be overridden by enemy subclasses that can shoot.

        Args:
            current_time (float): Current game time in seconds
            projectile_group (pygame.sprite.Group): Group to add projectiles to
        """
        pass


class BasicEnemy(Enemy):
    """Basic enemy with simple behavior."""

    def __init__(self, x, y):
        """Initialize a basic enemy.

        Args:
            x (int): Initial x position
            y (int): Initial y position
        """
        super().__init__(x, y, health=10, speed=100)

        # Draw a simple enemy shape
        pygame.draw.circle(self.image, (200, 50, 50), (20, 20), 18)
        pygame.draw.circle(self.image, (150, 0, 0), (20, 20), 12)

        # Set transparent color
        self.image.set_colorkey((255, 0, 0))


class ZigzagEnemy(Enemy):
    """Enemy that moves in a zigzag pattern."""

    def __init__(self, x, y):
        """Initialize a zigzag enemy.

        Args:
            x (int): Initial x position
            y (int): Initial y position
        """
        super().__init__(x, y, health=15, speed=120)
        self.movement_type = "zigzag"

        # Draw a simple enemy shape
        pygame.draw.polygon(self.image, (200, 150, 50), [(0, 20), (20, 0), (40, 20), (20, 40)])

        # Set transparent color
        self.image.set_colorkey((255, 0, 0))


class EnemyProjectile(pygame.sprite.Sprite):
    """Projectile fired by enemies."""

    def __init__(self, x, y, speed=300):
        """Initialize a projectile.

        Args:
            x (int): X position
            y (int): Y position
            speed (int): Speed in pixels per second
        """
        super().__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill((100, 100, 255))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.top = y
        self.velocity = pygame.math.Vector2(0, speed)

    def update(self, dt):
        """Update projectile position.

        Args:
            dt (float): Time elapsed since last update
        """
        self.rect.y += self.velocity.y * dt

        # Remove if off screen
        screen_height = pygame.display.get_surface().get_size()[1]
        if self.rect.top > screen_height:
            self.kill()


class ShooterEnemy(Enemy):
    """Enemy that shoots projectiles."""

    def __init__(self, x, y):
        """Initialize a shooter enemy.

        Args:
            x (int): Initial x position
            y (int): Initial y position
        """
        super().__init__(x, y, health=20, speed=80)

        # Draw a simple enemy shape
        pygame.draw.circle(self.image, (50, 50, 200), (20, 20), 18)
        pygame.draw.rect(self.image, (0, 0, 150), pygame.Rect(10, 25, 20, 15))

        # Set transparent color
        self.image.set_colorkey((255, 0, 0))

        # Shooting properties
        self.can_shoot = True
        self.fire_rate = 1.5  # seconds between shots
        self.last_shot_time = random.random() * 1.5  # Randomize first shot

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
            bullet = EnemyProjectile(self.rect.centerx, self.rect.bottom)
            projectile_group.add(bullet)
            return True

        return False
