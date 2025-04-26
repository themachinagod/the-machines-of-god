"""
Game class for Machines of God.
"""

import json
import os

import pygame
from pygame.locals import K_ESCAPE, KEYDOWN, QUIT

from engine.state import MenuState, PlayingState, ShopState


class Game:
    """Main game class that manages the game loop and state transitions."""

    def __init__(self, width=980, height=1280, fps=60):
        """Initialize the game with specified window dimensions and target FPS.

        Args:
            width (int): Window width in pixels
            height (int): Window height in pixels
            fps (int): Target frames per second
        """
        # These will be the virtual dimensions (actual gameplay area)
        self.virtual_width = width
        self.virtual_height = height

        # Get actual screen dimensions
        display_info = pygame.display.Info()
        self.screen_width = display_info.current_w
        self.screen_height = display_info.current_h

        # For consistency in references, maintain width/height for the virtual screen
        self.width = self.virtual_width
        self.height = self.virtual_height

        self.fps = fps
        self.running = False
        self.fullscreen = True  # Default to fullscreen mode

        # Ensure save directory exists
        self.save_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data"
        )
        os.makedirs(self.save_dir, exist_ok=True)
        self.save_file = os.path.join(self.save_dir, "save_data.json")

        # Flag to track if there's a saved game - set this BEFORE creating states
        self.has_saved_game = os.path.exists(self.save_file)

        # Initialize display
        flags = pygame.FULLSCREEN if self.fullscreen else 0
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), flags)
        pygame.display.set_caption("Machines of God")

        # Create virtual screen for consistent gameplay area
        self.virtual_screen = pygame.Surface((self.virtual_width, self.virtual_height))

        # Calculate scaling and positioning
        self._update_screen_layout()

        # Set up the clock for timing
        self.clock = pygame.time.Clock()

        # Set up game states
        self.states = {
            "menu": MenuState(self),
            "playing": PlayingState(self),
            "shop": ShopState(self),
        }

        # Set current state
        self.current_state_name = "menu"
        self.current_state = self.states[self.current_state_name]

        # Load saved data
        self._load_game_data()

    def _update_screen_layout(self):
        """Calculate scaling and positioning for the virtual screen."""
        # Calculate the aspect ratio of virtual screen and actual screen
        virtual_ratio = self.virtual_width / self.virtual_height
        screen_ratio = self.screen_width / self.screen_height

        if screen_ratio > virtual_ratio:
            # Screen is wider than virtual, scale by height
            self.scale_height = self.screen_height
            self.scale_width = int(self.scale_height * virtual_ratio)
            self.scale_x = (self.screen_width - self.scale_width) // 2
            self.scale_y = 0
        else:
            # Screen is taller than virtual, scale by width
            self.scale_width = self.screen_width
            self.scale_height = int(self.scale_width / virtual_ratio)
            self.scale_x = 0
            self.scale_y = (self.screen_height - self.scale_height) // 2

        # Calculate the scaling factor for mouse input
        self.scale_factor_x = self.virtual_width / self.scale_width
        self.scale_factor_y = self.virtual_height / self.scale_height

    def run(self):
        """Run the main game loop."""
        self.running = True

        while self.running:
            # Handle input events
            self._handle_events()

            # Update game state
            self._update()

            # Render game
            self._render()

            # Cap the frame rate
            self.clock.tick(self.fps)

        # Save game data when quitting
        self._save_game_data()

    def _handle_events(self):
        """Process input events."""
        for event in pygame.event.get():
            # Check for quit events
            if event.type == QUIT or (
                event.type == KEYDOWN
                and event.key == K_ESCAPE
                and self.current_state_name == "menu"
            ):
                self.running = False

            # Translate mouse position events to virtual coordinates
            if event.type in (pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP):
                # Translate physical coordinates to virtual coordinates
                if hasattr(event, "pos"):
                    physical_x, physical_y = event.pos

                    # Convert to virtual coordinate space if mouse is within game area
                    if (
                        self.scale_x <= physical_x < self.scale_x + self.scale_width
                        and self.scale_y <= physical_y < self.scale_y + self.scale_height
                    ):
                        virtual_x = int((physical_x - self.scale_x) * self.scale_factor_x)
                        virtual_y = int((physical_y - self.scale_y) * self.scale_factor_y)
                        event.pos = (virtual_x, virtual_y)

            # Let the current state handle the event
            self.current_state.handle_event(event)

    def _update(self):
        """Update game state."""
        # Update delta time
        dt = self.clock.get_time() / 1000.0  # Convert to seconds

        # Update the current state
        self.current_state.update(dt)

    def _render(self):
        """Render the game."""
        # Clear the screen
        self.screen.fill((0, 0, 0))

        # Clear the virtual screen
        self.virtual_screen.fill((0, 0, 0))

        # Let the current state render to the virtual screen
        self.current_state.render(self.virtual_screen)

        # Scale and blit the virtual screen onto the actual screen with letterboxing
        scaled_surface = pygame.transform.smoothscale(
            self.virtual_screen, (self.scale_width, self.scale_height)
        )
        self.screen.blit(scaled_surface, (self.scale_x, self.scale_y))

        # Draw letterbox borders if needed
        if self.scale_x > 0:
            # Draw vertical borders
            pygame.draw.rect(self.screen, (20, 20, 40), (0, 0, self.scale_x, self.screen_height))
            pygame.draw.rect(
                self.screen,
                (20, 20, 40),
                (self.scale_x + self.scale_width, 0, self.scale_x, self.screen_height),
            )
        if self.scale_y > 0:
            # Draw horizontal borders
            pygame.draw.rect(self.screen, (20, 20, 40), (0, 0, self.screen_width, self.scale_y))
            pygame.draw.rect(
                self.screen,
                (20, 20, 40),
                (0, self.scale_y + self.scale_height, self.screen_width, self.scale_y),
            )

        # Flip the display
        pygame.display.flip()

    def change_state(self, state_name):
        """Change the current game state.

        Args:
            state_name (str): Name of the state to change to
        """
        if state_name in self.states:
            # Exit the current state
            self.current_state.exit()

            # Change state
            self.current_state_name = state_name
            self.current_state = self.states[state_name]

            # Enter the new state
            self.current_state.enter()
        else:
            print(f"Error: State '{state_name}' does not exist.")

    def _save_game_data(self):
        """Save game progress to file."""
        save_data = {
            "stars": self.states["playing"].total_stars_collected,
            "upgrades": self.states["shop"].upgrades,
        }

        try:
            with open(self.save_file, "w") as f:
                json.dump(save_data, f)
            print("Game saved successfully!")
            self.has_saved_game = True
        except Exception as e:
            print(f"Error saving game: {e}")

    def _load_game_data(self):
        """Load game progress from file."""
        if not os.path.exists(self.save_file):
            print("No save file found, starting new game")
            self.has_saved_game = False
            return

        try:
            with open(self.save_file, "r") as f:
                save_data = json.load(f)

            # Restore data
            if "stars" in save_data:
                self.states["playing"].total_stars_collected = save_data["stars"]

            if "upgrades" in save_data:
                self.states["shop"].upgrades = save_data["upgrades"]

            print("Game loaded successfully!")
            self.has_saved_game = True
        except Exception as e:
            print(f"Error loading game: {e}")
            self.has_saved_game = False

    def start_new_game(self):
        """Start a new game by resetting save data."""
        # Reset the playing state
        self.states["playing"].total_stars_collected = 0

        # Reset all upgrades
        for key in self.states["shop"].upgrades:
            self.states["shop"].upgrades[key]["level"] = 0

        # Reset player stats
        self.states["playing"].player.health = self.states["playing"].player.max_health
        self.states["playing"].player.lives = 3
        self.states["playing"].player.score = 0

        # Apply upgrade resets to player
        play_state = self.states["playing"]
        shop_state = self.states["shop"]

        # Reset player stats based on starting upgrade levels
        play_state.player.max_health = shop_state.upgrades["hull"]["values"][0]
        play_state.player.health = play_state.player.max_health

        play_state.player.vert_speed = shop_state.upgrades["engine"]["values"][0]
        play_state.player.lat_speed = shop_state.upgrades["thruster"]["values"][0]

        play_state.player.primary_pattern = shop_state.upgrades["primary"]["patterns"][0]
        play_state.player.primary_cooldown = 0.5

        play_state.player.max_shield = shop_state.upgrades["shield"]["values"][0]
        play_state.player.shield = play_state.player.max_shield
        play_state.player.shield_recharge_rate = shop_state.upgrades["shield"]["recharge"][0]

        play_state.player.secondary_level = shop_state.upgrades["secondary"]["level"]
        play_state.player.missile_count = shop_state.upgrades["secondary"]["missiles"][0]
        play_state.player.missile_cooldown = shop_state.upgrades["secondary"]["cooldown"][0]

        play_state.player.magnet_radius = shop_state.upgrades["magnet"]["radius"][0]

        # Delete save file
        if os.path.exists(self.save_file):
            try:
                os.remove(self.save_file)
                print("Save file deleted for new game")
                self.has_saved_game = False
            except Exception as e:
                print(f"Error deleting save file: {e}")

        # Change to playing state to start the game
        self.change_state("playing")
