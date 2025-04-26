"""
UI management for the game.
"""

import pygame


class UIManager:
    """Manages UI rendering and interaction."""

    def __init__(self, game_width, game_height):
        """Initialize the UI manager.

        Args:
            game_width (int): Width of the game screen
            game_height (int): Height of the game screen
        """
        self.width = game_width
        self.height = game_height

        # Initialize fonts
        self.font = pygame.font.Font(None, 24)
        self.large_font = pygame.font.Font(None, 72)

    def render(self, screen, player, level_manager, enemy_manager, total_stars):
        """Render all UI elements.

        Args:
            screen (pygame.Surface): The surface to render on
            player: The player object with health/shield info
            level_manager: The level manager with level info
            enemy_manager: The enemy manager with wave info
            total_stars (int): Total stars collected
        """
        # Draw HUD
        self._draw_hud(screen, player, level_manager, enemy_manager, total_stars)

        # Draw level completion message if applicable
        if level_manager.is_level_complete():
            self._draw_level_complete_message(screen, level_manager.current_level)

        # Draw shield indicator if player has shield
        if player.shield > 0:
            self._draw_shield_indicator(screen, player)

    def _draw_hud(self, screen, player, level_manager, enemy_manager, total_stars):
        """Draw the heads-up display (HUD).

        Args:
            screen (pygame.Surface): The surface to render on
            player: The player object with health/shield info
            level_manager: The level manager with level info
            enemy_manager: The enemy manager with wave info
            total_stars (int): Total stars collected
        """
        # Draw HUD
        health_text = f"Health: {int(player.health)}/{player.max_health}"

        shield_text = (
            f"Shield: {int(player.shield)}/{player.max_shield}" if player.max_shield > 0 else ""
        )

        lives_text = f"Lives: {player.lives}"
        score_text = f"Score: {player.score}"
        stars_text = f"Stars: {total_stars}"

        missiles_text = f"Missiles: {player.missile_count}" if player.missile_count > 0 else ""

        # First row of HUD
        hud_text = self.font.render(
            f"{health_text}  {shield_text}  {lives_text}  {score_text}", True, (255, 255, 255)
        )
        screen.blit(hud_text, (10, 10))

        # Second row for additional info
        wave_text = (
            f"Level: {level_manager.current_level}  "
            f"Wave: {enemy_manager.get_current_wave_index() + 1}/{enemy_manager.get_total_waves()}"
        )

        hud_text2 = self.font.render(
            f"{stars_text}  {missiles_text}  {wave_text}",
            True,
            (255, 255, 255),
        )
        screen.blit(hud_text2, (10, 35))

    def _draw_level_complete_message(self, screen, level_number):
        """Draw the level completion message.

        Args:
            screen (pygame.Surface): The surface to render on
            level_number (int): Current level number
        """
        complete_text = self.large_font.render(
            f"Level {level_number} Complete!", True, (255, 220, 50)
        )
        text_rect = complete_text.get_rect(center=(self.width // 2, self.height // 2))

        # Draw shadow effect
        shadow_text = self.large_font.render(f"Level {level_number} Complete!", True, (0, 0, 0))
        shadow_rect = shadow_text.get_rect(center=(self.width // 2 + 3, self.height // 2 + 3))
        screen.blit(shadow_text, shadow_rect)
        screen.blit(complete_text, text_rect)

    def _draw_shield_indicator(self, screen, player):
        """Draw the shield indicator around the player.

        Args:
            screen (pygame.Surface): The surface to render on
            player: The player object with shield info
        """
        # Calculate shield percentage
        shield_pct = player.shield / player.max_shield

        # Draw shield arc with appropriate fill level
        pygame.draw.arc(
            screen,
            (50, 150, 255, 180),
            player.rect.inflate(20, 20),
            0,
            6.28 * shield_pct,  # Partial circle based on shield percentage
            3,
        )
