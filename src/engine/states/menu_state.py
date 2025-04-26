"""
Menu state for the game.
"""

import pygame

from .base_state import State


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

        # Menu options will be updated in enter()
        self.menu_options = []
        self.selected_option = 0
        self.update_menu_options()

    def update_menu_options(self):
        """Update menu options based on game state."""
        self.menu_options = []

        # Show Resume Game only if there's a saved game
        if self.game.has_saved_game:
            self.menu_options.append({"text": "Resume Game", "key": pygame.K_r, "action": "resume"})

        # Always show New Game and Shop
        self.menu_options.append({"text": "New Game", "key": pygame.K_n, "action": "new_game"})
        self.menu_options.append({"text": "Shop", "key": pygame.K_s, "action": "shop"})
        self.menu_options.append({"text": "Exit", "key": pygame.K_ESCAPE, "action": "exit"})

        # Ensure selected option is valid
        if self.selected_option >= len(self.menu_options):
            self.selected_option = 0

    def enter(self):
        """Called when entering this state."""
        # Update menu options when entering the state
        self.update_menu_options()

    def handle_event(self, event):
        """Handle input events for the menu state.

        Args:
            event: The pygame event to handle
        """
        if event.type == pygame.KEYDOWN:
            # Handle menu navigation
            if event.key == pygame.K_UP:
                self.selected_option = (self.selected_option - 1) % len(self.menu_options)
            elif event.key == pygame.K_DOWN:
                self.selected_option = (self.selected_option + 1) % len(self.menu_options)
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                self.execute_selected_action()
            else:
                # Check for hotkeys
                for i, option in enumerate(self.menu_options):
                    if event.key == option["key"]:
                        self.selected_option = i
                        self.execute_selected_action()
                        break

    def execute_selected_action(self):
        """Execute the currently selected menu action."""
        action = self.menu_options[self.selected_option]["action"]

        if action == "resume":
            # Resume saved game
            self.game._load_game_data()  # Reload data to ensure it's fresh
            self.game.change_state("playing")
        elif action == "new_game":
            # Start new game
            self.game.start_new_game()
        elif action == "shop":
            self.game.change_state("shop")
        elif action == "exit":
            self.game.running = False

    def render(self, screen):
        """Render the menu state.

        Args:
            screen: The pygame surface to render to
        """
        # Draw background (could be a starfield or something)
        screen.fill((0, 0, 40))

        # Draw title
        screen.blit(self.title_text, self.title_rect)

        # Draw menu options
        for i, option in enumerate(self.menu_options):
            # Highlight selected option
            color = (255, 255, 100) if i == self.selected_option else (200, 200, 200)
            text = self.font_small.render(option["text"], True, color)
            rect = text.get_rect(center=(self.game.width // 2, self.game.height // 2 + i * 50))
            screen.blit(text, rect) 