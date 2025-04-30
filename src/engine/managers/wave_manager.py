"""
Wave manager for handling enemy wave definitions and timing.
"""

from utils.logger import get_logger


class WaveManager:
    """Manages wave-related functionality including wave definitions, timing and progression."""

    def __init__(self):
        """Initialize the wave manager."""
        # Initialize logger
        self.logger = get_logger()
        self.logger.info("Initializing WaveManager")

        # Wave management
        self.waves = []
        self.wave_index = 0
        self.wave_timer = 0

        self.logger.info("WaveManager initialized successfully")

    def set_waves(self, waves):
        """Set the wave definitions.

        Args:
            waves: List of wave definitions
        """
        self.logger.info("Setting up %d waves", len(waves))
        self.waves = waves
        self.wave_index = 0
        self.wave_timer = 0

        # Log each wave's basic configuration
        for i, wave in enumerate(waves):
            self.logger.debug(
                "Wave %d: duration=%.2f seconds, %d enemy types",
                i + 1,
                wave["duration"],
                len(wave.get("enemies", [])),
            )

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
                self.logger.info(
                    "Wave changed: %d → %d (after %.2f seconds)",
                    old_wave + 1,
                    self.wave_index + 1,
                    current_wave["duration"],
                )
                return True

        return old_wave != self.wave_index

    def get_current_wave(self):
        """Get the current wave definition.

        Returns:
            dict: Current wave definition or None if no waves defined
        """
        if not self.waves or self.wave_index >= len(self.waves):
            self.logger.debug("No current wave available")
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
            old_wave = self.wave_index
            self.wave_index += 1
            self.wave_timer = 0
            self.logger.info(
                "Manually advancing from wave %d to wave %d", old_wave + 1, self.wave_index + 1
            )
            return True
        else:
            self.logger.debug("Cannot advance wave: already at last wave (%d)", self.wave_index + 1)
            return False

    def reset(self):
        """Reset the wave manager state."""
        self.logger.info("Resetting WaveManager to initial state")
        self.wave_index = 0
        self.wave_timer = 0
