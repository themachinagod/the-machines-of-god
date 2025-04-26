"""
Visual effects and utilities for the game engine.
"""

import random

import pygame


class ParallaxBackground:
    """A multi-layered scrolling background system."""

    def __init__(self, screen_width, screen_height):
        """Initialize the parallax background.

        Args:
            screen_width (int): Width of the screen
            screen_height (int): Height of the screen
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.layers = []

        # Create star layers with different speeds
        self._create_star_layers()

        # Create nebula layer
        self._create_nebula_layer()

    def _create_star_layers(self):
        """Create multiple layers of stars with varying speeds."""
        # Distant stars (slowest)
        stars_distant = []
        for _ in range(50):
            x = random.randint(0, self.screen_width)
            y = random.randint(0, self.screen_height)
            size = 1  # Small stars
            color = (150, 150, 200)  # Light blue/purple
            stars_distant.append({"x": x, "y": y, "size": size, "color": color})

        # Mid-distance stars
        stars_mid = []
        for _ in range(75):
            x = random.randint(0, self.screen_width)
            y = random.randint(0, self.screen_height)
            size = 2  # Medium stars
            color = (200, 200, 255)  # Brighter blue/white
            stars_mid.append({"x": x, "y": y, "size": size, "color": color})

        # Close stars (fastest)
        stars_close = []
        for _ in range(50):
            x = random.randint(0, self.screen_width)
            y = random.randint(0, self.screen_height)
            size = 3  # Larger stars
            color = (255, 255, 255)  # Bright white
            stars_close.append({"x": x, "y": y, "size": size, "color": color})

        # Add layers to the background
        self.layers.append({"objects": stars_distant, "speed": 10, "type": "stars"})
        self.layers.append({"objects": stars_mid, "speed": 20, "type": "stars"})
        self.layers.append({"objects": stars_close, "speed": 30, "type": "stars"})

    def _create_nebula_layer(self):
        """Create a nebula cloud layer effect."""
        nebulae = []
        for _ in range(3):
            x = random.randint(0, self.screen_width)
            y = random.randint(0, self.screen_height)
            size = random.randint(100, 300)
            # Create a random color with transparency
            color = (
                random.randint(50, 150),  # R
                random.randint(50, 150),  # G
                random.randint(150, 250),  # B
                random.randint(30, 80),  # Alpha
            )
            nebulae.append({"x": x, "y": y, "size": size, "color": color})

        # Add nebula layer
        self.layers.append({"objects": nebulae, "speed": 5, "type": "nebula"})

    def update(self, dt):
        """Update all background layers.

        Args:
            dt (float): Time elapsed since last update in seconds
        """
        # Update each layer
        for layer in self.layers:
            for obj in layer["objects"]:
                # Move objects down
                obj["y"] += layer["speed"] * dt

                # Wrap around screen when objects go off-screen
                if obj["y"] - obj["size"] > self.screen_height:
                    obj["y"] = -obj["size"]
                    obj["x"] = random.randint(0, self.screen_width)

    def render(self, screen):
        """Render all background layers.

        Args:
            screen (pygame.Surface): Screen to render to
        """
        # Render each layer in order (bottom to top)
        for layer in self.layers:
            if layer["type"] == "stars":
                for obj in layer["objects"]:
                    # Draw simple circular stars
                    pygame.draw.circle(
                        screen, obj["color"], (int(obj["x"]), int(obj["y"])), obj["size"]
                    )
            elif layer["type"] == "nebula":
                for obj in layer["objects"]:
                    # Create a surface with alpha for the nebula
                    size = obj["size"]
                    nebula_surface = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)

                    # Draw nebula cloud as a gradient circle
                    for radius in range(size, 0, -10):
                        alpha = int(255 * (radius / size))
                        color = list(obj["color"])
                        if len(color) >= 4:
                            color[3] = min(color[3], alpha)
                        else:
                            color.append(alpha)
                        pygame.draw.circle(nebula_surface, tuple(color), (size, size), radius)

                    # Blit the nebula to the screen
                    screen.blit(nebula_surface, (int(obj["x"] - size), int(obj["y"] - size)))
