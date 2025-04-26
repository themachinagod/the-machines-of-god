"""
Wave manager for handling enemy wave definitions and timing.
"""


class WaveManager:
    """Manages wave-related functionality including wave definitions, timing and progression."""

    def __init__(self):
        """Initialize the wave manager."""
        # Wave management
        self.waves = []
        self.wave_index = 0
        self.wave_timer = 0

    def set_waves(self, waves):
        """Set the wave definitions.

        Args:
            waves: List of wave definitions
        """
        self.waves = waves
        self.wave_index = 0
        self.wave_timer = 0

    def update_wave_timer(self, dt):
        """Update the wave timer.

        Args:
            dt: Time elapsed since last update in seconds

        Returns:
            bool: True if wave changed, False otherwise
        """
        # Update wave timing
        old_wave = self.wave_index
        self.wave_timer += dt

        # Check if we need to switch to next wave
        if self.waves and self.wave_index < len(self.waves):
            current_wave = self.waves[self.wave_index]
            if (
                self.wave_timer >= current_wave["duration"]
                and self.wave_index < len(self.waves) - 1
            ):
                self.wave_index += 1
                self.wave_timer = 0
                return True

        return old_wave != self.wave_index

    def get_current_wave(self):
        """Get the current wave definition.

        Returns:
            dict: Current wave definition or None if no waves defined
        """
        if not self.waves or self.wave_index >= len(self.waves):
            return None
        return self.waves[self.wave_index]

    def get_current_wave_index(self):
        """Get the current wave index.

        Returns:
            int: Current wave index (0-based)
        """
        return self.wave_index

    def get_total_waves(self):
        """Get the total number of waves.

        Returns:
            int: Total number of waves
        """
        return len(self.waves)

    def advance_wave(self):
        """Advance to the next wave if possible.

        Returns:
            bool: True if successfully advanced, False if already at last wave
        """
        if self.wave_index < len(self.waves) - 1:
            self.wave_index += 1
            self.wave_timer = 0
            return True
        return False

    def reset(self):
        """Reset the wave manager state."""
        self.wave_index = 0
        self.wave_timer = 0
