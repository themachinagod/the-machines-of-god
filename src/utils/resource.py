"""
Resource manager for Machines of God game.
Handles loading and caching game resources like images, sounds, fonts, etc.
"""

import os

import pygame


class ResourceManager:
    """Handles loading and caching game resources."""

    def __init__(self):
        """Initialize the resource manager."""
        self.images = {}
        self.sounds = {}
        self.fonts = {}
        self.music = {}

        # Base directories for resources
        self.image_dir = os.path.join("assets", "images")
        self.sound_dir = os.path.join("assets", "sounds")
        self.font_dir = os.path.join("assets", "fonts")
        self.music_dir = os.path.join("assets", "music")

    def get_image(self, filename):
        """Get an image resource, loading it if not already loaded.

        Args:
            filename (str): Name of the image file

        Returns:
            pygame.Surface: The loaded image
        """
        if filename not in self.images:
            try:
                filepath = os.path.join(self.image_dir, filename)
                image = pygame.image.load(filepath).convert_alpha()
                self.images[filename] = image
            except pygame.error as e:
                print(f"Error loading image {filename}: {e}")
                # Create a placeholder image
                image = pygame.Surface((50, 50))
                image.fill((255, 0, 255))  # Magenta for missing texture
                pygame.draw.line(image, (0, 0, 0), (0, 0), (50, 50), 2)
                pygame.draw.line(image, (0, 0, 0), (50, 0), (0, 50), 2)
                self.images[filename] = image

        return self.images[filename]

    def get_sound(self, filename):
        """Get a sound resource, loading it if not already loaded.

        Args:
            filename (str): Name of the sound file

        Returns:
            pygame.mixer.Sound: The loaded sound or None if loading failed
        """
        if filename not in self.sounds:
            try:
                filepath = os.path.join(self.sound_dir, filename)
                self.sounds[filename] = pygame.mixer.Sound(filepath)
            except pygame.error as e:
                print(f"Error loading sound {filename}: {e}")
                self.sounds[filename] = None

        return self.sounds[filename]

    def get_font(self, filename, size):
        """Get a font resource, loading it if not already loaded.

        Args:
            filename (str): Name of the font file or None for default
            size (int): Font size in points

        Returns:
            pygame.font.Font: The loaded font
        """
        key = f"{filename}_{size}"
        if key not in self.fonts:
            try:
                if filename:
                    filepath = os.path.join(self.font_dir, filename)
                    self.fonts[key] = pygame.font.Font(filepath, size)
                else:
                    # Use default font
                    self.fonts[key] = pygame.font.Font(None, size)
            except pygame.error as e:
                print(f"Error loading font {filename} size {size}: {e}")
                # Fall back to default font
                self.fonts[key] = pygame.font.Font(None, size)

        return self.fonts[key]

    def play_music(self, filename, loops=-1, fade_ms=0):
        """Play a music file.

        Args:
            filename (str): Name of the music file
            loops (int): Number of times to repeat (-1 for infinite)
            fade_ms (int): Fade-in time in milliseconds

        Returns:
            bool: True if music started playing, False otherwise
        """
        try:
            filepath = os.path.join(self.music_dir, filename)
            pygame.mixer.music.load(filepath)
            pygame.mixer.music.play(loops, fade_ms=fade_ms)
            self.music[filename] = True
            return True
        except pygame.error as e:
            print(f"Error playing music {filename}: {e}")
            return False

    def stop_music(self, fade_ms=0):
        """Stop the currently playing music.

        Args:
            fade_ms (int): Fade-out time in milliseconds
        """
        pygame.mixer.music.fadeout(fade_ms)


# Create a singleton instance
resource_manager = ResourceManager()
