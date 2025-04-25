"""
Configuration utilities for Machines of God game.
"""

import json
import os


class Config:
    """Handles game configuration."""

    def __init__(self, config_file="data/config.json"):
        """Initialize the configuration manager.

        Args:
            config_file (str): Path to the configuration file
        """
        self.config_file = config_file
        self.config = self._load_config()

    def _load_config(self):
        """Load configuration from file.

        Returns:
            dict: Configuration data
        """
        default_config = {
            "video": {
                "width": 1280,
                "height": 720,
                "fullscreen": False,
                "vsync": True,
                "fps_limit": 60,
            },
            "audio": {"music_volume": 0.7, "sfx_volume": 1.0, "mute": False},
            "controls": {
                "keyboard": {
                    "move_up": "w",
                    "move_down": "s",
                    "move_left": "a",
                    "move_right": "d",
                    "shoot": "space",
                    "special1": "z",
                    "special2": "x",
                    "pause": "p",
                },
                "gamepad": {"enabled": True},
            },
            "gameplay": {"difficulty": "normal", "player_lives": 3, "starting_level": 1},
            "display": {"show_fps": True, "show_hitboxes": False},
        }

        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r") as f:
                    config = json.load(f)

                # Merge with default config to ensure all values exist
                return self._merge_configs(default_config, config)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Error loading config file: {e}")
                print("Using default configuration.")
                return default_config
        else:
            print(f"Config file not found: {self.config_file}")
            print("Creating default configuration.")
            self._save_config(default_config)
            return default_config

    def _merge_configs(self, default, custom):
        """Merge a custom config with the default config.

        Args:
            default (dict): Default configuration
            custom (dict): Custom configuration

        Returns:
            dict: Merged configuration
        """
        result = default.copy()

        for key, value in custom.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._merge_configs(result[key], value)
            else:
                result[key] = value

        return result

    def _save_config(self, config=None):
        """Save configuration to file.

        Args:
            config (dict, optional): Configuration to save. Defaults to current config.

        Returns:
            bool: True if successful, False otherwise
        """
        if config is None:
            config = self.config

        try:
            # Make sure the directory exists
            os.makedirs(os.path.dirname(self.config_file), exist_ok=True)

            with open(self.config_file, "w") as f:
                json.dump(config, f, indent=4)
            return True
        except IOError as e:
            print(f"Error saving config file: {e}")
            return False

    def get(self, section, key=None, default=None):
        """Get a configuration value.

        Args:
            section (str): Configuration section
            key (str, optional): Configuration key. If None, return the entire section.
            default: Default value if section or key not found

        Returns:
            The configuration value or default
        """
        if section not in self.config:
            return default

        if key is None:
            return self.config[section]

        if key not in self.config[section]:
            return default

        return self.config[section][key]

    def set(self, section, key, value):
        """Set a configuration value.

        Args:
            section (str): Configuration section
            key (str): Configuration key
            value: New value

        Returns:
            bool: True if successful, False otherwise
        """
        if section not in self.config:
            self.config[section] = {}

        self.config[section][key] = value
        return self._save_config()

    def save(self):
        """Save the current configuration to file.

        Returns:
            bool: True if successful, False otherwise
        """
        return self._save_config()


# Create a singleton instance
config = Config()
