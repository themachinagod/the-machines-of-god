#!/usr/bin/env python3
"""
Machines of God - A vertical scrolling shoot 'em up game inspired by Sky Force
"""

import sys

import pygame

from engine.game import Game
from utils.logger import get_logger

# Get the logger singleton
logger = get_logger()


def main():
    """Main entry point for the game."""
    logger.info("Starting Machines of God")

    # Initialize pygame
    logger.debug("Initializing pygame")
    pygame.init()

    # Create and run the game
    logger.debug("Creating game instance")
    game = Game()

    logger.info("Starting game loop")
    game.run()

    # Clean up
    logger.debug("Cleaning up and exiting")
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
