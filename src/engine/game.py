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

    def __init__(self, width=1280, height=720, fps=60):
        """Initialize the game with specified window dimensions and target FPS.

        Args:
            width (int): Window width in pixels
            height (int): Window height in pixels
            fps (int): Target frames per second
        """
        self.width = width
        self.height = height
        self.fps = fps
        self.running = False

        # Ensure save directory exists
        self.save_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data"
        )
        os.makedirs(self.save_dir, exist_ok=True)
        self.save_file = os.path.join(self.save_dir, "save_data.json")

        # Initialize display
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Machines of God")

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

        # Let the current state render
        self.current_state.render(self.screen)

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
        except Exception as e:
            print(f"Error saving game: {e}")

    def _load_game_data(self):
        """Load game progress from file."""
        if not os.path.exists(self.save_file):
            print("No save file found, starting new game")
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
        except Exception as e:
            print(f"Error loading game: {e}")
