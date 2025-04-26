"""
Shop state for purchasing upgrades.
"""

import pygame

from .base_state import State


class ShopState(State):
    """Shop state for purchasing upgrades."""

    def __init__(self, game):
        """Initialize the shop state.

        Args:
            game: Reference to the main game object
        """
        super().__init__(game)

        # Font setup
        self.title_font = pygame.font.Font(None, 48)
        self.item_font = pygame.font.Font(None, 28)
        self.desc_font = pygame.font.Font(None, 20)

        # Upgrade definitions - name, description, cost, max level
        self.upgrades = {
            "hull": {
                "name": "Hull Armor",
                "desc": "Increase ship health",
                "cost": 50,
                "cost_multiplier": 1.5,
                "max_level": 5,
                "level": 0,
                "values": [50, 75, 100, 125, 150, 200],
            },
            "engine": {
                "name": "Engine Thrust",
                "desc": "Increase vertical movement speed",
                "cost": 30,
                "cost_multiplier": 1.6,
                "max_level": 5,
                "level": 0,
                "values": [250, 300, 350, 400, 450, 500],
            },
            "thruster": {
                "name": "Side Thrusters",
                "desc": "Increase lateral movement speed",
                "cost": 30,
                "cost_multiplier": 1.6,
                "max_level": 5,
                "level": 0,
                "values": [250, 300, 350, 400, 450, 500],
            },
            "primary": {
                "name": "Primary Weapons",
                "desc": "Upgrade main weapons system",
                "cost": 60,
                "cost_multiplier": 1.8,
                "max_level": 5,
                "level": 0,
                "patterns": ["single_slow", "single_medium", "double", "triple", "quad", "five"],
            },
            "shield": {
                "name": "Shield Generator",
                "desc": "Generate protective shields",
                "cost": 100,
                "cost_multiplier": 2.0,
                "max_level": 3,
                "level": 0,
                "values": [0, 50, 75, 100],
                "recharge": [0, 2, 5, 10],  # Shield points per second
            },
            "secondary": {
                "name": "Missile System",
                "desc": "Launch homing missiles",
                "cost": 150,
                "cost_multiplier": 2.0,
                "max_level": 3,
                "level": 0,
                "missiles": [0, 1, 2, 2],
                "cooldown": [0, 3, 3, 2],  # Seconds between missile launches
            },
            "magnet": {
                "name": "Star Magnet",
                "desc": "Attract stars from greater distance",
                "cost": 80,
                "cost_multiplier": 1.8,
                "max_level": 3,
                "level": 0,
                "radius": [0, 50, 100, 150],
            },
        }

        # Selected upgrade (highlighted)
        self.selected_index = 0
        self.upgrade_keys = list(self.upgrades.keys())

        # Stars available for spending
        self.stars = 0

    def enter(self):
        """Called when entering the shop state."""
        # Get current star count from playing state
        if "playing" in self.game.states:
            play_state = self.game.states["playing"]
            self.stars = play_state.total_stars_collected

    def handle_event(self, event):
        """Handle input events for the shop state.

        Args:
            event: The pygame event to handle
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_b:
                # Return to menu
                self.game.change_state("menu")
            elif event.key == pygame.K_RETURN or event.key == pygame.K_n or event.key == pygame.K_c:
                # Continue to next level
                self._continue_to_next_level()
            elif event.key == pygame.K_UP:
                # Navigate up
                self.selected_index = (self.selected_index - 1) % len(self.upgrade_keys)
            elif event.key == pygame.K_DOWN:
                # Navigate down
                self.selected_index = (self.selected_index + 1) % len(self.upgrade_keys)
            elif event.key == pygame.K_SPACE:
                # Purchase upgrade
                self._purchase_upgrade()

    def _continue_to_next_level(self):
        """Progress to the next level after shopping."""
        # Make sure we have the playing state
        if "playing" not in self.game.states:
            self.game.change_state("menu")
            return

        # Get reference to playing state
        play_state = self.game.states["playing"]

        # Increment level
        play_state.current_level += 1

        # Reset level timers and completion flags
        play_state.level_time = 0
        play_state.wave_timer = 0
        play_state.wave_index = 0
        play_state.level_complete = False
        play_state.completion_timer = 0

        # Increase difficulty for next level (more enemies, faster spawns)
        self._scale_difficulty(play_state)

        # Return to playing state with next level
        self.game.change_state("playing")

    def _scale_difficulty(self, play_state):
        """Scale difficulty based on current level."""
        # Increase level duration slightly for higher levels
        play_state.level_duration = 90 + (play_state.current_level - 1) * 15

        # Scale enemy spawn rates and counts
        for wave in play_state.waves:
            for enemy_def in wave["enemies"]:
                # Increase enemy count based on level (careful not to overwhelm)
                base_count = enemy_def["count"]
                enemy_def["count"] = min(base_count + play_state.current_level // 2, base_count * 3)

                # Decrease spawn interval for faster action
                base_interval = enemy_def["interval"]
                enemy_def["interval"] = max(
                    base_interval * 0.8 ** (play_state.current_level - 1), 0.5
                )

    def _purchase_upgrade(self):
        """Attempt to purchase the selected upgrade."""
        key = self.upgrade_keys[self.selected_index]
        upgrade = self.upgrades[key]

        # Check if at max level
        if upgrade["level"] >= upgrade["max_level"]:
            return

        # Calculate cost based on current level
        cost = int(upgrade["cost"] * (upgrade["cost_multiplier"] ** upgrade["level"]))

        # Check if enough stars
        if self.stars >= cost:
            # Purchase
            self.stars -= cost
            upgrade["level"] += 1

            # Update playing state with new upgrade level
            if "playing" in self.game.states:
                play_state = self.game.states["playing"]
                play_state.total_stars_collected = self.stars

                # Apply upgrade effects to player
                if hasattr(play_state, "player") and play_state.player:
                    player = play_state.player

                    # Set the appropriate upgrade value
                    if key == "hull":
                        player.max_health = upgrade["values"][upgrade["level"]]
                        player.health = min(player.health, player.max_health)
                    elif key == "engine":
                        player.vert_speed = upgrade["values"][upgrade["level"]]
                    elif key == "thruster":
                        player.lat_speed = upgrade["values"][upgrade["level"]]
                    elif key == "primary":
                        player.primary_level = upgrade["level"]
                        player.primary_pattern = upgrade["patterns"][upgrade["level"]]
                    elif key == "shield":
                        player.max_shield = upgrade["values"][upgrade["level"]]
                        player.shield_recharge_rate = upgrade["recharge"][upgrade["level"]]
                    elif key == "secondary":
                        player.secondary_level = upgrade["level"]
                        player.missile_count = upgrade["missiles"][upgrade["level"]]
                        player.missile_cooldown = upgrade["cooldown"][upgrade["level"]]
                    elif key == "magnet":
                        player.magnet_radius = upgrade["radius"][upgrade["level"]]

                    # Update player stats based on all upgrades
                    player.update_stats()

    def update(self, dt):
        """Update the shop state.

        Args:
            dt: Time elapsed since last update in seconds
        """
        pass

    def render(self, screen):
        """Render the shop state.

        Args:
            screen: The pygame surface to render to
        """
        # Draw background
        screen.fill((20, 20, 50))

        # Draw shop title
        title_text = self.title_font.render("UPGRADE SHOP", True, (255, 220, 50))
        title_rect = title_text.get_rect(center=(self.game.width // 2, 50))
        screen.blit(title_text, title_rect)

        # Draw available stars
        stars_text = self.item_font.render(f"Available Stars: {self.stars}", True, (255, 255, 255))
        stars_rect = stars_text.get_rect(topright=(self.game.width - 50, 30))
        screen.blit(stars_text, stars_rect)

        # Draw instructions
        inst_text = self.desc_font.render(
            "Use UP/DOWN to select, SPACE to purchase, ENTER to continue, ESC to exit",
            True,
            (180, 180, 180),
        )
        inst_rect = inst_text.get_rect(center=(self.game.width // 2, self.game.height - 30))
        screen.blit(inst_text, inst_rect)

        # Show current/next level info
        level_info = "Press ENTER to continue to"
        if "playing" in self.game.states:
            play_state = self.game.states["playing"]
            level_info += f" Level {play_state.current_level + 1}"
        else:
            level_info += " next level"

        level_text = self.item_font.render(level_info, True, (100, 255, 100))
        level_rect = level_text.get_rect(center=(self.game.width // 2, self.game.height - 60))
        screen.blit(level_text, level_rect)

        # Draw upgrade items
        y_start = 150
        item_height = 80

        for i, key in enumerate(self.upgrade_keys):
            upgrade = self.upgrades[key]

            # Highlight selected item
            if i == self.selected_index:
                pygame.draw.rect(
                    screen,
                    (40, 40, 80),
                    pygame.Rect(
                        50, y_start + (i * item_height), self.game.width - 100, item_height
                    ),
                )
                pygame.draw.rect(
                    screen,
                    (100, 100, 200),
                    pygame.Rect(
                        50, y_start + (i * item_height), self.game.width - 100, item_height
                    ),
                    2,
                )

            # Upgrade name
            name_text = self.item_font.render(
                f"{upgrade['name']} (Level {upgrade['level']}/{upgrade['max_level']})",
                True,
                (255, 255, 255),
            )
            screen.blit(name_text, (70, y_start + 10 + (i * item_height)))

            # Upgrade description
            desc_text = self.desc_font.render(upgrade["desc"], True, (200, 200, 200))
            screen.blit(desc_text, (70, y_start + 40 + (i * item_height)))

            # Calculate cost based on current level
            cost = int(upgrade["cost"] * (upgrade["cost_multiplier"] ** upgrade["level"]))

            # Show cost or maxed out
            if upgrade["level"] >= upgrade["max_level"]:
                cost_text = self.item_font.render("MAXED OUT", True, (100, 255, 100))
            else:
                cost_text = self.item_font.render(
                    f"Cost: {cost} stars",
                    True,
                    (255, 220, 50) if self.stars >= cost else (150, 150, 150),
                )

            cost_rect = cost_text.get_rect(
                right=self.game.width - 70, centery=y_start + 25 + (i * item_height)
            )
            screen.blit(cost_text, cost_rect) 