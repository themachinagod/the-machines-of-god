"""
Playing state for the main gameplay.
"""

import pygame

from engine.managers.collectible_manager import CollectibleManager
from engine.managers.collision_manager import CollisionManager
from engine.managers.enemy_manager import EnemyManager
from engine.managers.level_manager import LevelManager
from engine.managers.ui_manager import UIManager
from engine.visual import ParallaxBackground
from entities.player import Player

from .base_state import State


class PlayingState(State):
    """Playing state for the game."""

    def __init__(self, game):
        """Initialize the playing state.

        Args:
            game: Reference to the main game object
        """
        super().__init__(game)

        # Initialize font for UI
        self.font = pygame.font.Font(None, 24)

        # Initialize sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.player_projectiles = pygame.sprite.Group()
        self.player_missiles = pygame.sprite.Group()
        self.enemy_projectiles = pygame.sprite.Group()
        self.collectibles = pygame.sprite.Group()

        # Create sprite groups dictionary for easier manager access
        self.sprite_groups = {
            "all": self.all_sprites,
            "enemies": self.enemies,
            "player_projectiles": self.player_projectiles,
            "player_missiles": self.player_missiles,
            "enemy_projectiles": self.enemy_projectiles,
            "collectibles": self.collectibles,
        }

        # Create player
        self.player = Player(game.width // 2, game.height - 100)
        self.all_sprites.add(self.player)

        # Background scrolling
        self.bg_y = 0
        self.scroll_speed = 1.0

        # Initialize parallax background
        self.background = ParallaxBackground(game.width, game.height)

        # Game timing
        self.game_time = 0

        # Level structure
        self.current_level = 1
        self.level_time = 0
        self.level_duration = 90  # Level lasts 90 seconds

        # Level completion
        self.level_complete = False
        self.completion_timer = 0
        self.completion_delay = 3.0  # Time to show completion message

        # Initialize wave definitions for level 1
        self.base_waves = [
            # Wave 1: Basic enemies, easy pattern
            {
                "duration": 15,  # Seconds this wave lasts
                "enemies": [{"type": "basic", "count": 1, "interval": 2.0}],
            },
            # Wave 2: More basic enemies
            {"duration": 15, "enemies": [{"type": "basic", "count": 2, "interval": 1.5}]},
            # Wave 3: Basic + Zigzag enemies
            {
                "duration": 15,
                "enemies": [
                    {"type": "basic", "count": 1, "interval": 3.0},
                    {"type": "zigzag", "count": 1, "interval": 3.0},
                ],
            },
            # Wave 4: Zigzag enemies + Shooter + Dart
            {
                "duration": 15,
                "enemies": [
                    {"type": "zigzag", "count": 1, "interval": 3.0},
                    {"type": "shooter", "count": 1, "interval": 5.0},
                    {"type": "dart", "count": 2, "interval": 4.0},
                ],
            },
            # Wave 5: Shield bearers + basic enemies
            {
                "duration": 20,
                "enemies": [
                    {"type": "basic", "count": 2, "interval": 3.0},
                    {"type": "shield", "count": 2, "interval": 5.0},
                ],
            },
            # Wave 6: Mini-boss wave with mixed enemies
            {
                "duration": 30,
                "enemies": [
                    {"type": "basic", "count": 1, "interval": 4.0},
                    {"type": "shooter", "count": 1, "interval": 6.0},
                    {"type": "zigzag", "count": 1, "interval": 4.0},
                    {"type": "dart", "count": 1, "interval": 3.0},
                    {"type": "shield", "count": 1, "interval": 7.0},
                    {"type": "heavy", "count": 1, "interval": 10.0},
                ],
            },
        ]

        # Game progression data
        self.total_stars_collected = 0
        
        # Statistics tracking
        self.stats = {
            "enemies_killed": 0,
            "enemies_escaped": 0,
            "stars_collected": 0,
            "stars_missed": 0,
            "shots_fired": 0,
            "shots_hit": 0,
            "accuracy": 0,
            "collection_rate": 0,
            "kill_rate": 0,
        }
        
        # Level scoring
        self.base_score = 0
        self.level_score = 0
        self.bonus_score = 0
        self.bonus_multiplier = 1.0
        self.showing_level_summary = False
        self.summary_timer = 0
        self.summary_duration = 5.0  # Show summary for 5 seconds

        # Initialize managers
        self._init_managers()

    def _init_managers(self):
        """Initialize all game manager components."""
        # Create collectible manager
        self.collectible_manager = CollectibleManager(
            self.game.width, self.game.height, self.all_sprites, self.collectibles
        )

        # Create collision manager
        self.collision_manager = CollisionManager(self.sprite_groups, self.collectible_manager)
        
        # Set the stats reference in collision manager
        self.collision_manager.set_stats_reference(self.stats)

        # Create enemy manager
        self.enemy_manager = EnemyManager(
            self.game.width,
            self.game.height,
            self.all_sprites,
            self.enemies,
            self.enemy_projectiles,
        )

        # Create level manager
        self.level_manager = LevelManager(self.game)

        # Create UI manager
        self.ui_manager = UIManager(self.game.width, self.game.height)

        # Set up the level
        self._setup_level()

    def _setup_level(self):
        """Set up the level based on current level number."""
        # Get difficulty-scaled waves
        scaled_waves = self.level_manager.scale_difficulty(self.base_waves)

        # Initialize enemy manager with scaled waves
        self.enemy_manager.set_waves(scaled_waves)

    def enter(self):
        """Called when entering the playing state."""
        # Debug - Print player weapon info
        if hasattr(self, "player") and self.player:
            print(f"DEBUG - Entering PlayingState - Level: {self.current_level}")
            print(f"DEBUG - Player primary_pattern: {self.player.primary_pattern}")
            print(f"DEBUG - Player primary_level: {self.player.primary_level}")
            print(f"DEBUG - Player primary_cooldown: {self.player.primary_cooldown}")

        # Store player attributes if they exist and we're continuing a game
        player_attributes = {}
        if hasattr(self, "player") and self.player:
            # Save important player attributes
            player_attributes = {
                "max_health": self.player.max_health,
                "health": self.player.health,
                "max_shield": self.player.max_shield,
                "shield": self.player.shield,
                "shield_recharge_rate": self.player.shield_recharge_rate,
                "vert_speed": self.player.vert_speed,
                "lat_speed": self.player.lat_speed,
                "primary_level": self.player.primary_level,
                "primary_pattern": self.player.primary_pattern,
                "secondary_level": self.player.secondary_level,
                "missile_count": self.player.missile_count,
                "missile_cooldown": self.player.missile_cooldown,
                "magnet_radius": self.player.magnet_radius,
                "score": self.player.score,
                "lives": self.player.lives,
            }

        # Reset player position if needed
        self.player.rect.centerx = self.game.width // 2
        self.player.rect.bottom = self.game.height - 50

        # Clear all sprites except player
        for sprite in self.all_sprites:
            if sprite != self.player:
                sprite.kill()

        # Reset game entities
        self.enemies.empty()
        self.player_projectiles.empty()
        self.player_missiles.empty()
        self.enemy_projectiles.empty()
        self.collectibles.empty()

        # Reset level data for current level
        self.level_time = 0
        self.level_complete = False
        self.completion_timer = 0
        
        # Keep persistent stats across levels, but reset for new game
        if not player_attributes and (self.player.health <= 0 or self.current_level == 1):
            # Reset stats for new game
            self.stats = {
                "enemies_killed": 0,
                "enemies_escaped": 0,
                "stars_collected": 0, 
                "stars_missed": 0,
                "shots_fired": 0,
                "shots_hit": 0,
                "accuracy": 0,
                "collection_rate": 0,
                "kill_rate": 0,
            }

        # Restore player attributes if we had any
        if player_attributes:
            for attr, value in player_attributes.items():
                setattr(self.player, attr, value)
        # Else ensure player has appropriate starting stats if new game
        elif self.player.health <= 0:
            self.player.health = self.player.max_health
            self.player.lives = 3
            self.player.score = 0

        # Setup level
        self._setup_level()

    def handle_event(self, event):
        """Handle input events for the playing state.

        Args:
            event: The pygame event to handle
        """
        # If showing level summary, any key proceeds to shop
        if self.showing_level_summary and event.type == pygame.KEYDOWN:
            self.showing_level_summary = False
            self.summary_timer = 0
            # Save current game state for persistence
            self.level_manager._save_game_state()
            # Go to shop after showing summary
            self.game.change_state("shop")
            return
            
        # Handle pause
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                # Will implement pause state later
                pass
            # Fire when space is pressed
            elif event.key == pygame.K_SPACE:
                self.player.shoot(self.game_time, self.player_projectiles)
                # Add new projectiles to all_sprites
                for proj in self.player_projectiles:
                    if proj not in self.all_sprites:
                        self.all_sprites.add(proj)
            # Fire missile with M key if available
            elif event.key == pygame.K_m:
                # Find the closest enemy for targeting
                target = self._find_closest_enemy()
                if self.player.fire_missile(self.game_time, self.player_missiles, target):
                    # Add new missiles to all_sprites
                    for missile in self.player_missiles:
                        if missile not in self.all_sprites:
                            self.all_sprites.add(missile)

    def _find_closest_enemy(self):
        """Find the closest enemy to the player for missile targeting.

        Returns:
            pygame.sprite.Sprite: The closest enemy, or None if no enemies
        """
        if not self.enemies:
            return None

        closest = None
        min_distance = float("inf")

        player_pos = pygame.math.Vector2(self.player.rect.centerx, self.player.rect.centery)

        for enemy in self.enemies:
            enemy_pos = pygame.math.Vector2(enemy.rect.centerx, enemy.rect.centery)
            distance = player_pos.distance_to(enemy_pos)

            if distance < min_distance:
                min_distance = distance
                closest = enemy

        return closest

    def update(self, dt):
        """Update the playing state.

        Args:
            dt: Time elapsed since last update in seconds
        """
        # Update game time
        self.game_time += dt
        
        # If showing level summary, handle the timer and transition
        if self.showing_level_summary:
            self.summary_timer += dt
            if self.summary_timer >= self.summary_duration:
                self.showing_level_summary = False
                self.summary_timer = 0
                # Save current game state for persistence
                self.level_manager._save_game_state()
                # Go to shop after showing summary
                self.game.change_state("shop")
            return  # Skip other updates while showing summary

        # Handle level timing and completion
        level_changed = self.level_manager.update(dt)
        
        # If level is complete, calculate final score and show summary
        if level_changed and self.level_manager.is_level_complete():
            self._calculate_level_score()
            self.showing_level_summary = True
            return  # Skip other updates if level is complete

        # Update wave timing
        self.enemy_manager.update_wave_timer(dt)

        # Update player and weapons
        self._update_player_and_weapons(dt)

        # Update enemies through enemy manager
        self.enemy_manager.update(dt, self.game_time)

        # Update collectibles through collectible manager
        self.collectible_manager.update(dt)
        
        # Track stars that went off-screen
        for collectible in list(self.collectibles):
            if collectible.rect.top > self.game.height:
                if isinstance(collectible, Star):
                    self.stats["stars_missed"] += 1
                collectible.kill()

        # Track enemies that escaped
        for enemy in list(self.enemies):
            if enemy.rect.top > self.game.height:
                self.stats["enemies_escaped"] += 1
                
        # Update collection rate and kill rate statistics
        total_stars = self.stats["stars_collected"] + self.stats["stars_missed"]
        if total_stars > 0:
            self.stats["collection_rate"] = (self.stats["stars_collected"] / total_stars) * 100
            
        total_enemies = self.stats["enemies_killed"] + self.stats["enemies_escaped"]
        if total_enemies > 0:
            self.stats["kill_rate"] = (self.stats["enemies_killed"] / total_enemies) * 100
            
        if self.stats["shots_fired"] > 0:
            self.stats["accuracy"] = (self.stats["shots_hit"] / self.stats["shots_fired"]) * 100

        # Store base score from game events, but don't apply multiplier yet
        self.base_score = self.player.score

        # Update background
        self.background.update(dt)

        # Check collisions using collision manager
        player_killed = self.collision_manager.check_collisions(self.player)

        # Update total stars collected
        self.total_stars_collected = self.collision_manager.total_stars_collected

        # Check if player was killed
        if player_killed:
            # Game over - return to menu
            self.game.change_state("menu")

    def _update_player_and_weapons(self, dt):
        """Update player and weapon systems.

        Args:
            dt: Time elapsed since last update in seconds
        """
        # Update scrolling background
        self.bg_y = (self.bg_y + self.scroll_speed * dt) % self.game.height

        # Get pressed keys
        keys = pygame.key.get_pressed()

        # Update player
        self.player.update(dt, keys)

        # Continuous fire if space is held
        if keys[pygame.K_SPACE]:
            if self.player.shoot(self.game_time, self.player_projectiles):
                # Track shots fired
                self.stats["shots_fired"] += 1
                
                # Add new projectiles to all_sprites
                for proj in self.player_projectiles:
                    if proj not in self.all_sprites:
                        self.all_sprites.add(proj)

        # Update projectiles and missiles
        self.player_projectiles.update(dt)
        self.player_missiles.update(dt)
        self.enemy_projectiles.update(dt)

    def render(self, screen):
        """Render the playing state.

        Args:
            screen: The pygame surface to render to
        """
        # Fill the screen with black
        screen.fill((0, 0, 40))  # Very dark blue background

        # Draw parallax background
        self.background.render(screen)

        # Draw all sprites
        self.all_sprites.draw(screen)

        # Draw UI elements using UI manager
        self.ui_manager.render(
            screen, self.player, self.level_manager, self.enemy_manager, self.total_stars_collected
        )
        
        # If showing level summary, draw it
        if self.showing_level_summary:
            self._draw_level_summary(screen)

    def _draw_level_summary(self, screen):
        """Draw the level completion summary screen.
        
        Args:
            screen: The pygame surface to render to
        """
        # Semi-transparent overlay
        overlay = pygame.Surface((self.game.width, self.game.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))  # RGBA, semi-transparent black
        screen.blit(overlay, (0, 0))
        
        # Title
        summary_font = pygame.font.Font(None, 48)
        title_text = summary_font.render(f"LEVEL {self.current_level} COMPLETE!", True, (255, 220, 50))
        title_rect = title_text.get_rect(center=(self.game.width // 2, 100))
        screen.blit(title_text, title_rect)
        
        # Stats box
        stat_font = pygame.font.Font(None, 28)
        stat_y = 180
        stat_spacing = 35
        
        # Performance stats
        stats_to_show = [
            f"Enemies Defeated: {self.stats['enemies_killed']}",
            f"Enemies Escaped: {self.stats['enemies_escaped']}",
            f"Kill Rate: {self.stats['kill_rate']:.1f}%",
            f"Stars Collected: {self.stats['stars_collected']}",
            f"Collection Rate: {self.stats['collection_rate']:.1f}%",
            f"Shots Fired: {self.stats['shots_fired']}",
            f"Accuracy: {self.stats['accuracy']:.1f}%",
        ]
        
        # Draw stats
        for i, stat in enumerate(stats_to_show):
            text = stat_font.render(stat, True, (220, 220, 220))
            rect = text.get_rect(center=(self.game.width // 2, stat_y + i * stat_spacing))
            screen.blit(text, rect)
        
        # Score summary
        score_y = stat_y + len(stats_to_show) * stat_spacing + 30
        
        score_items = [
            ("Base Score:", self.base_score, (255, 255, 255)),
            (f"Performance Bonus ({self.bonus_multiplier:.2f}x):", self.bonus_score, (100, 255, 100)),
            ("TOTAL SCORE:", self.level_score, (255, 220, 50)),
        ]
        
        for i, (label, value, color) in enumerate(score_items):
            text = stat_font.render(f"{label} {value}", True, color)
            rect = text.get_rect(center=(self.game.width // 2, score_y + i * stat_spacing))
            screen.blit(text, rect)
        
        # Continue prompt
        continue_y = score_y + len(score_items) * stat_spacing + 40
        continue_text = stat_font.render("Press any key to continue to the shop...", True, (180, 180, 180))
        continue_rect = continue_text.get_rect(center=(self.game.width // 2, continue_y))
        
        # Blink the prompt
        if (self.game_time * 2) % 2 < 1:  # Blink every half second
            screen.blit(continue_text, continue_rect)

    def _draw_ui(self, screen):
        """Draw user interface elements."""
        # Draw HUD
        health_text = f"Health: {int(self.player.health)}/{self.player.max_health}"
        shield_text = (
            f"Shield: {int(self.player.shield)}/{self.player.max_shield}"
            if self.player.max_shield > 0
            else ""
        )
        lives_text = f"Lives: {self.player.lives}"
        score_text = f"Score: {self.player.score}"
        stars_text = f"Stars: {self.total_stars_collected}"
        missiles_text = (
            f"Missiles: {self.player.missile_count}" if self.player.missile_count > 0 else ""
        )

        # First row of HUD
        hud_text = self.font.render(
            f"{health_text}  {shield_text}  {lives_text}  {score_text}", True, (255, 255, 255)
        )
        screen.blit(hud_text, (10, 10))

        # Second row for additional info
        current_wave = self.enemy_manager.get_current_wave_index() + 1  # 1-based for display
        total_waves = self.enemy_manager.get_total_waves()
        wave_text = f"Level: {self.current_level}  Wave: {current_wave}/{total_waves}"
        hud_text2 = self.font.render(
            f"{stars_text}  {missiles_text}  {wave_text}",
            True,
            (255, 255, 255),
        )
        screen.blit(hud_text2, (10, 35))

        # Draw level completion message
        if self.level_complete:
            complete_font = pygame.font.Font(None, 72)
            complete_text = complete_font.render(
                f"Level {self.current_level} Complete!", True, (255, 220, 50)
            )
            text_rect = complete_text.get_rect(center=(self.game.width // 2, self.game.height // 2))

            # Draw shadow effect
            shadow_text = complete_font.render(
                f"Level {self.current_level} Complete!", True, (0, 0, 0)
            )
            shadow_rect = shadow_text.get_rect(
                center=(self.game.width // 2 + 3, self.game.height // 2 + 3)
            )
            screen.blit(shadow_text, shadow_rect)
            screen.blit(complete_text, text_rect)

        # Draw shield indicator if player has shield
        if self.player.shield > 0:
            # Calculate shield percentage
            shield_pct = self.player.shield / self.player.max_shield

            # Draw shield arc with appropriate fill level
            pygame.draw.arc(
                screen,
                (50, 150, 255, 180),
                self.player.rect.inflate(20, 20),
                0,
                6.28 * shield_pct,  # Partial circle based on shield percentage
                3,
            )

        # Draw stats in bottom left corner during gameplay
        stats_text = f"Kills: {self.stats['enemies_killed']} " \
                    f"Escaped: {self.stats['enemies_escaped']} " \
                    f"K/D: {self.stats['kill_rate']:.1f}% " \
                    f"Stars: {self.stats['stars_collected']}/{self.stats['stars_collected'] + self.stats['stars_missed']} " \
                    f"Acc: {self.stats['accuracy']:.1f}%"
        
        stats_render = self.font.render(stats_text, True, (200, 200, 200))
        screen.blit(stats_render, (10, self.game.height - 30))

    def _calculate_level_score(self):
        """Calculate final level score with performance bonuses."""
        # Calculate score based on performance metrics
        performance_bonus = (
            (self.stats["kill_rate"] * 0.5) +
            (self.stats["collection_rate"] * 0.3) + 
            (self.stats["accuracy"] * 0.2)
        )
        
        # Calculate bonus multiplier (up to 2x)
        self.bonus_multiplier = 1.0 + (performance_bonus / 100)
        
        # Calculate bonus score
        self.bonus_score = int(self.base_score * (self.bonus_multiplier - 1.0))
        
        # Apply bonus to player score
        self.level_score = self.base_score + self.bonus_score
        self.player.score = self.level_score
