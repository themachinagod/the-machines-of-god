#!/usr/bin/env python3
"""
Machines of God - A vertical scrolling shoot 'em up game inspired by Sky Force
"""

import sys

import pygame

from engine.game import Game


def main():
    """Main entry point for the game."""
    # Initialize pygame
    pygame.init()

    # Create and run the game
    game = Game()
    game.run()

    # Clean up
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
