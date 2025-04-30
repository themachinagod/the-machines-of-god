"""
Level management for the game.
"""

from utils.logger import get_logger


class LevelManager:
    """Manages level progression, timing, and difficulty scaling."""

    def __init__(self, game):
        """Initialize the level manager.

        Args:
            game: Reference to the main game object
        """
        # Initialize logger
        self.logger = get_logger()
        self.logger.info("Initializing LevelManager")

        self.game = game

        # Level structure
        self.current_level = 1
        self.level_time = 0
        self.level_duration = 90  # Level lasts 90 seconds
        self.logger.debug(
            "Initial level settings: level=%d, duration=%d seconds",
            self.current_level,
            self.level_duration,
        )

        # Level completion
        self.level_complete = False
        self.completion_timer = 0
        self.completion_delay = 3.0  # Time to show completion message

        self.logger.info("LevelManager initialized successfully")

    def update(self, dt):
        """Update level timing and check for completion.

        Args:
            dt (float): Time elapsed since last update

        Returns:
            bool: True if level state changed, False otherwise
        """
        state_changed = False

        # Update level timer
        self.level_time += dt

        # Log every ~10 seconds as a debug message
        if int(self.level_time) % 10 == 0 and dt > 0 and (self.level_time - dt) % 10 > 9:
            self.logger.debug(
                "Level time: %.2f / %.2f seconds", self.level_time, self.level_duration
            )

        # Check for level completion
        if self.level_time >= self.level_duration and not self.level_complete:
            self.level_complete = True
            state_changed = True
            self.logger.info(
                "Level %d complete! (Time: %.2f seconds)", self.current_level, self.level_time
            )
            print(f"Level {self.current_level} complete!")

            # Return True to indicate level is complete, but don't transition states
            # Let the playing state handle showing the summary and transitioning
            return True

        # Handle level completion delay - REMOVED automatic transition
        # The playing state now handles this

        return state_changed

    def _save_game_state(self):
        """Save the current game state for level progression."""
        self.logger.info("Saving game state after level %d", self.current_level)

        # Ensure we have a reference to game to save state
        if hasattr(self.game, "_save_game_data"):
            self.game._save_game_data()
            self.logger.debug("Game state saved successfully")
        else:
            self.logger.warning("Could not save game state - no _save_game_data method found")

        # Mark game as having saved data
        self.game.has_saved_game = True

    def scale_difficulty(self, waves):
        """Scale difficulty based on current level.

        Args:
            waves (list): Wave definitions to adjust

        Returns:
            list: Adjusted wave definitions
        """
        self.logger.info(
            "Scaling difficulty for level %d (input: %d waves)", self.current_level, len(waves)
        )

        # Make a copy of the waves to avoid modifying the original
        scaled_waves = []
        for wave_index, wave in enumerate(waves):
            scaled_wave = {"duration": wave["duration"], "enemies": []}

            for enemy_def in wave["enemies"]:
                # Create a new enemy definition with adjusted values
                scaled_enemy = enemy_def.copy()

                # Increase enemy count based on level (careful not to overwhelm)
                base_count = enemy_def["count"]
                scaled_enemy["count"] = min(base_count + self.current_level // 2, base_count * 3)

                # Decrease spawn interval for faster action
                base_interval = enemy_def["interval"]
                scaled_enemy["interval"] = max(base_interval * 0.8 ** (self.current_level - 1), 0.5)

                self.logger.debug(
                    "Wave %d, enemy type %s: count %d -> %d, interval %.2f -> %.2f",
                    wave_index + 1,
                    enemy_def["type"],
                    base_count,
                    scaled_enemy["count"],
                    base_interval,
                    scaled_enemy["interval"],
                )

                scaled_wave["enemies"].append(scaled_enemy)

            scaled_waves.append(scaled_wave)

        # Scale level duration slightly for higher levels
        old_duration = self.level_duration
        self.level_duration = 90 + (self.current_level - 1) * 15
        self.logger.debug(
            "Level duration adjusted: %d -> %d seconds", old_duration, self.level_duration
        )

        self.logger.info("Difficulty scaling complete: created %d scaled waves", len(scaled_waves))
        return scaled_waves

    def advance_level(self):
        """Advance to the next level."""
        old_level = self.current_level
        self.current_level += 1
        self.logger.info("Advancing from level %d to level %d", old_level, self.current_level)
        self.reset_level_state()

    def reset_level_state(self):
        """Reset level state for a new level start."""
        self.logger.debug("Resetting level state for level %d", self.current_level)
        self.level_time = 0
        self.level_complete = False
        self.completion_timer = 0

    def reset_for_new_game(self):
        """Reset level manager for a new game."""
        self.logger.info("Resetting level manager for new game")
        self.current_level = 1
        self.reset_level_state()

    def is_level_complete(self):
        """Check if current level is complete.

        Returns:
            bool: True if level is complete, False otherwise
        """
        return self.level_complete
