"""
Logging utility for the game.
Handles logging to console and file with different log levels.
Creates a new log file for each game run with a timestamp in the filename.
Implements a singleton pattern so the logger can be accessed from anywhere.
"""

import logging
import os
from datetime import datetime
from pathlib import Path

# Global logger instance
_logger = None


def get_logger():
    """
    Get the singleton logger instance.
    If the logger hasn't been set up yet, it will be initialized.

    Returns:
        logging.Logger: The configured logger instance
    """
    global _logger
    if _logger is None:
        _logger = setup_logger()
    return _logger


def setup_logger(name="game"):
    """
    Set up and configure the logger.

    Args:
        name (str): Name of the logger. Defaults to 'game'.

    Returns:
        logging.Logger: Configured logger instance
    """
    # Create logger
    logger = logging.getLogger(name)

    # Only setup handlers if they don't exist to avoid duplicate logs
    if not logger.handlers:
        logger.setLevel(logging.DEBUG)

        # Create logs directory if it doesn't exist
        log_dir = Path(__file__).parents[2] / "logs"
        os.makedirs(log_dir, exist_ok=True)

        # Create a timestamp for the log filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_filename = f"{log_dir / f'game_{timestamp}.log'}"

        # Create file handler
        file_handler = logging.FileHandler(log_filename)
        file_handler.setLevel(logging.DEBUG)

        # Create console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        # Create formatter and add it to the handlers
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # Add handlers to logger
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger
