"""
Collectible items for Machines of God game.
"""

import math
import random

import pygame


class Collectible(pygame.sprite.Sprite):
    """Base class for all collectible items."""

    def __init__(self, x, y, value=10, speed=100):
        """Initialize the collectible.

        Args:
            x (int): X position
            y (int): Y position
            value (int): Value of the collectible
            speed (int): Speed in pixels per second
        """
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.value = value
        self.speed = speed
        self.collected = False

        # Movement variables
        self.velocity = pygame.math.Vector2(0, self.speed)
        self.wobble_timer = 0
        self.wobble_direction = random.choice([-1, 1])
        self.wobble_speed = random.uniform(1.5, 3.0)
        self.wobble_amount = random.randint(10, 20)

    def update(self, dt):
        """Update the collectible.

        Args:
            dt (float): Time elapsed since last update
        """
        # Wobble horizontally
        self.wobble_timer += dt * self.wobble_speed
        wobble = self.wobble_amount * self.wobble_direction * math.sin(self.wobble_timer)

        # Move down with wobble
        self.rect.x += wobble * dt
        self.rect.y += self.velocity.y * dt

        # Remove if off screen
        screen_height = pygame.display.get_surface().get_size()[1]
        if self.rect.top > screen_height:
            self.kill()

    def collect(self):
        """Collect this item."""
        self.collected = True
        self.kill()
        return self.value


class Star(Collectible):
    """Star collectible for currency."""

    def __init__(self, x, y, value=10):
        """Initialize the star.

        Args:
            x (int): X position
            y (int): Y position
            value (int): Value of the star
        """
        super().__init__(x, y, value=value, speed=80)

        # Create star image
        self.image = pygame.Surface((20, 20), pygame.SRCALPHA)

        # Draw a star shape
        color = (255, 220, 50)  # Golden yellow
        center = (10, 10)
        points = []

        # Calculate star points
        for i in range(10):
            angle = i * 36  # 36 = 360 / 10
            radius = 9 if i % 2 == 0 else 4  # Outer/inner points
            x = center[0] + radius * math.cos(math.radians(angle))
            y = center[1] + radius * math.sin(math.radians(angle))
            points.append((x, y))

        pygame.draw.polygon(self.image, color, points)

        # Add a glow effect
        glow_surface = pygame.Surface((30, 30), pygame.SRCALPHA)
        pygame.draw.circle(glow_surface, (255, 255, 200, 100), (15, 15), 12)

        # Render the glow
        glow_rect = glow_surface.get_rect(center=self.image.get_rect().center)
        self.image.blit(glow_surface, glow_rect.topleft)


class HealthPack(Collectible):
    """Health restoration collectible."""

    def __init__(self, x, y, value=25):
        """Initialize the health pack.

        Args:
            x (int): X position
            y (int): Y position
            value (int): Amount of health to restore
        """
        super().__init__(x, y, value=value, speed=100)

        # Create health pack image
        self.image = pygame.Surface((20, 20), pygame.SRCALPHA)

        # Draw a health pack (red cross)
        pygame.draw.rect(self.image, (220, 20, 20), (5, 8, 10, 4))
        pygame.draw.rect(self.image, (220, 20, 20), (8, 5, 4, 10))

        # Add white background for visibility
        pygame.draw.circle(self.image, (255, 255, 255, 180), (10, 10), 8)


class ShieldPack(Collectible):
    """Shield boost collectible."""

    def __init__(self, x, y, value=50):
        """Initialize the shield pack.

        Args:
            x (int): X position
            y (int): Y position
            value (int): Amount of shield to add
        """
        super().__init__(x, y, value=value, speed=100)

        # Create shield pack image
        self.image = pygame.Surface((20, 20), pygame.SRCALPHA)

        # Draw a shield (blue circle)
        pygame.draw.circle(self.image, (50, 150, 255, 200), (10, 10), 8)
        pygame.draw.circle(self.image, (150, 200, 255, 150), (10, 10), 6)

        # Add outline
        pygame.draw.circle(self.image, (255, 255, 255), (10, 10), 9, 1)
