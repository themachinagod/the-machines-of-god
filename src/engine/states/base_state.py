"""
Base State class for the game state system.
"""


class State:
    """Base class for all game states."""

    def __init__(self, game):
        """Initialize the state.

        Args:
            game: Reference to the main game object
        """
        self.game = game

    def enter(self):
        """Called when entering the state."""
        pass

    def exit(self):
        """Called when exiting the state."""
        pass

    def handle_event(self, event):
        """Handle input events.

        Args:
            event: The pygame event to handle
        """
        pass

    def update(self, dt):
        """Update the state.

        Args:
            dt: Time elapsed since last update in seconds
        """
        pass

    def render(self, screen):
        """Render the state.

        Args:
            screen: The pygame surface to render to
        """
        pass 