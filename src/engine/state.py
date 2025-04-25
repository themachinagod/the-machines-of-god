"""
State classes for Machines of God game.
Handles different game states like menu, playing, paused, etc.
"""

import pygame


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


class MenuState(State):
    """Menu state for the game."""

    def __init__(self, game):
        """Initialize the menu state.

        Args:
            game: Reference to the main game object
        """
        super().__init__(game)
        self.font = pygame.font.Font(None, 72)
        self.title_text = self.font.render("Machines of God", True, (255, 255, 255))
        self.title_rect = self.title_text.get_rect(center=(game.width // 2, game.height // 3))

        self.font_small = pygame.font.Font(None, 36)
        self.start_text = self.font_small.render("Press SPACE to Start", True, (200, 200, 200))
        self.start_rect = self.start_text.get_rect(center=(game.width // 2, game.height // 2))

        self.exit_text = self.font_small.render("Press ESC to Exit", True, (200, 200, 200))
        self.exit_rect = self.exit_text.get_rect(center=(game.width // 2, game.height // 2 + 50))

    def handle_event(self, event):
        """Handle input events for the menu state.

        Args:
            event: The pygame event to handle
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.game.change_state("playing")

    def render(self, screen):
        """Render the menu state.

        Args:
            screen: The pygame surface to render to
        """
        # Draw background (could be a starfield or something)
        screen.fill((0, 0, 40))

        # Draw title and menu options
        screen.blit(self.title_text, self.title_rect)
        screen.blit(self.start_text, self.start_rect)
        screen.blit(self.exit_text, self.exit_rect)


class PlayingState(State):
    """Playing state for the game."""

    def __init__(self, game):
        """Initialize the playing state.

        Args:
            game: Reference to the main game object
        """
        super().__init__(game)
        # This is just a placeholder for now
        # Later will initialize player, enemies, level, etc.
        self.bg_y = 0
        self.bg_speed = 100  # pixels per second
        self.font = pygame.font.Font(None, 24)

    def enter(self):
        """Called when entering the playing state."""
        # This will eventually initialize the level, player, etc.
        pass

    def handle_event(self, event):
        """Handle input events for the playing state.

        Args:
            event: The pygame event to handle
        """
        # This will handle player input, etc.
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                # Will implement pause state later
                pass

    def update(self, dt):
        """Update the playing state.

        Args:
            dt: Time elapsed since last update in seconds
        """
        # Update scrolling background
        self.bg_y = (self.bg_y + self.bg_speed * dt) % self.game.height

        # This will eventually update all game entities
        pass

    def render(self, screen):
        """Render the playing state.

        Args:
            screen: The pygame surface to render to
        """
        # Draw scrolling background - simple placeholder for now
        screen.fill((20, 20, 60))

        # Draw stars to simulate scrolling
        for i in range(50):
            # Stars are just white rectangles for now
            y_pos = (i * 30 + self.bg_y) % self.game.height
            pygame.draw.rect(screen, (255, 255, 255), (i * 25, y_pos, 2, 2))

        # Placeholder text
        debug_text = self.font.render("Playing State - Placeholder", True, (255, 255, 255))
        screen.blit(debug_text, (10, 10))
