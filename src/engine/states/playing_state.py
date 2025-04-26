"""
Playing state for the main gameplay.
"""

import random

import pygame

from engine.visual import ParallaxBackground
from entities.collectible import HealthPack, ShieldPack, Star
from entities.enemy import (
    BasicEnemy,
    DartEnemy,
    HeavyBomber,
    ShieldBearerEnemy,
    ShooterEnemy,
    ZigzagEnemy,
)
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
        self.wave_timer = 0
        self.wave_index = 0

        # Level completion
        self.level_complete = False
        self.completion_timer = 0
        self.completion_delay = 3.0  # Time to show completion message

        # Wave definitions for level 1
        self.waves = [
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

        # Enemy spawn timing for current wave
        self.enemy_spawn_timers = {}

        # Game progression data
        self.total_stars_collected = 0

    def enter(self):
        """Called when entering the playing state."""
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
        self.wave_timer = 0
        self.wave_index = 0
        self.level_complete = False
        self.completion_timer = 0
        self.enemy_spawn_timers = {}

        # Restore player attributes if we had any
        if player_attributes:
            for attr, value in player_attributes.items():
                setattr(self.player, attr, value)
        # Else ensure player has appropriate starting stats if new game
        elif self.player.health <= 0:
            self.player.health = self.player.max_health
            self.player.lives = 3
            self.player.score = 0

    def handle_event(self, event):
        """Handle input events for the playing state.

        Args:
            event: The pygame event to handle
        """
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

        # Handle level timing and completion
        self._update_level_timing(dt)
        if self.level_complete:
            return  # Skip other updates if level is complete

        # Update game entities
        self._update_player_and_weapons(dt)
        self._update_enemies(dt)
        self._update_collectibles(dt)

        # Update background
        self.background.update(dt)

        # Check collisions
        self._check_collisions()

        # Spawn any necessary enemies
        self._process_wave_spawns(dt)

    def _update_level_timing(self, dt):
        """Update level timing and wave progression.

        Args:
            dt: Time elapsed since last update in seconds
        """
        # Update level timer
        self.level_time += dt

        # Check for level completion
        if self.level_time >= self.level_duration:
            if not self.level_complete:
                self.level_complete = True
                print(f"Level {self.current_level} complete!")

        # Handle level completion delay
        if self.level_complete:
            self.completion_timer += dt
            if self.completion_timer >= self.completion_delay:
                # Save current game state for persistence
                self._save_game_state()
                # Go to shop after completing level
                self.game.change_state("shop")
                return

        # Update wave timing
        self.wave_timer += dt

        # Check if we need to switch to next wave
        current_wave = self.waves[self.wave_index]
        if self.wave_timer >= current_wave["duration"] and self.wave_index < len(self.waves) - 1:
            self.wave_timer = 0
            self.wave_index += 1
            self.enemy_spawn_timers = {}  # Reset timers for new wave
            print(f"Starting wave {self.wave_index + 1}")

        # Handle enemy spawning based on current wave
        self._process_wave_spawns(dt)

    def _save_game_state(self):
        """Save the current game state for level progression."""
        # Ensure we have a reference to game to save state
        if hasattr(self.game, "_save_game_data"):
            self.game._save_game_data()

        # Mark game as having saved data
        self.game.has_saved_game = True

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
                # Add new projectiles to all_sprites
                for proj in self.player_projectiles:
                    if proj not in self.all_sprites:
                        self.all_sprites.add(proj)

        # Update projectiles and missiles
        self.player_projectiles.update(dt)
        self.player_missiles.update(dt)
        self.enemy_projectiles.update(dt)

    def _update_enemies(self, dt):
        """Update enemies and their shooting.

        Args:
            dt: Time elapsed since last update in seconds
        """
        # Update enemies and handle enemy shooting
        for enemy in self.enemies:
            enemy.update(dt)
            # Let shooter enemies shoot
            if hasattr(enemy, "can_shoot") and enemy.can_shoot:
                if enemy.shoot(self.game_time, self.enemy_projectiles):
                    # Add new projectiles to all_sprites
                    for proj in self.enemy_projectiles:
                        if proj not in self.all_sprites:
                            self.all_sprites.add(proj)

    def _update_collectibles(self, dt):
        """Update collectibles and magnet effect.

        Args:
            dt: Time elapsed since last update in seconds
        """
        # Update collectibles
        self.collectibles.update(dt)

        # Apply magnet effect if player has magnet upgrade
        if self.player.magnet_radius > 0:
            self._apply_magnet_effect()

    def _process_wave_spawns(self, dt):
        """Process enemy spawning for the current wave.

        Args:
            dt: Time elapsed since last update in seconds
        """
        current_wave = self.waves[self.wave_index]
        for enemy_def in current_wave["enemies"]:
            enemy_type = enemy_def["type"]

            # Initialize timer if not exists
            if enemy_type not in self.enemy_spawn_timers:
                self.enemy_spawn_timers[enemy_type] = 0

            # Update timer
            self.enemy_spawn_timers[enemy_type] += dt

            # Check if it's time to spawn
            if self.enemy_spawn_timers[enemy_type] >= enemy_def["interval"]:
                self.enemy_spawn_timers[enemy_type] = 0

                # Spawn enemies based on count
                for _ in range(enemy_def["count"]):
                    self._spawn_enemy(enemy_type)

    def _spawn_enemy(self, enemy_type="basic"):
        """Spawn a new enemy at a random position.

        Args:
            enemy_type (str): Type of enemy to spawn
        """
        x = random.randint(50, self.game.width - 50)

        if enemy_type == "basic":
            enemy = BasicEnemy(x, -50)
        elif enemy_type == "zigzag":
            enemy = ZigzagEnemy(x, -50)
        elif enemy_type == "shooter":
            enemy = ShooterEnemy(x, -50)
        elif enemy_type == "heavy":
            enemy = HeavyBomber(x, -50)
        elif enemy_type == "dart":
            enemy = DartEnemy(x, -50)
        elif enemy_type == "shield":
            enemy = ShieldBearerEnemy(x, -50)
        else:
            enemy = BasicEnemy(x, -50)

        self.enemies.add(enemy)
        self.all_sprites.add(enemy)

    def _apply_magnet_effect(self):
        """Pull collectibles toward the player if they're within magnet radius."""
        if not self.player.magnet_radius or not self.collectibles:
            return

        player_pos = pygame.math.Vector2(self.player.rect.centerx, self.player.rect.centery)

        for collectible in self.collectibles:
            collectible_pos = pygame.math.Vector2(
                collectible.rect.centerx, collectible.rect.centery
            )
            distance = player_pos.distance_to(collectible_pos)

            # If within radius, apply attraction force
            if distance < self.player.magnet_radius:
                # Calculate direction to player
                direction = player_pos - collectible_pos

                if direction.length() > 0:
                    direction.normalize_ip()

                    # Apply stronger force when closer
                    force = (self.player.magnet_radius - distance) / self.player.magnet_radius

                    # Update collectible position directly
                    collectible.rect.x += (
                        direction.x * force * 300 * 0.016
                    )  # Hardcoded dt for smooth effect
                    collectible.rect.y += direction.y * force * 300 * 0.016

    def _check_collisions(self):
        """Check for collisions between game objects."""
        # Player projectiles hitting enemies
        hits = pygame.sprite.groupcollide(self.enemies, self.player_projectiles, False, True)
        for enemy, projectiles in hits.items():
            # Force enemy death after one hit for immediate feedback
            enemy.health = 0
            self.player.score += enemy.value

            # Spawn collectibles with probability
            self._spawn_collectibles(enemy.rect.centerx, enemy.rect.centery)

            # Create explosion effect
            explosion = pygame.Surface((60, 60), pygame.SRCALPHA)
            pygame.draw.circle(explosion, (255, 200, 50, 200), (30, 30), 30)
            pygame.draw.circle(explosion, (255, 150, 50, 180), (30, 30), 25)
            pygame.draw.circle(explosion, (255, 100, 50, 150), (30, 30), 20)
            pygame.draw.circle(explosion, (255, 50, 50, 100), (30, 30), 15)
            # Kill the enemy
            enemy.kill()

        # Player missiles hitting enemies
        hits = pygame.sprite.groupcollide(self.enemies, self.player_missiles, False, True)
        for enemy, missiles in hits.items():
            # Force enemy death after one missile hit
            enemy.health = 0
            self.player.score += enemy.value * 2  # Bonus score for missile kills

            # Higher chance of collectibles from missile kills
            self._spawn_collectibles(enemy.rect.centerx, enemy.rect.centery, bonus_chance=True)

            # Create bigger explosion effect
            explosion = pygame.Surface((80, 80), pygame.SRCALPHA)
            pygame.draw.circle(explosion, (255, 200, 50, 200), (40, 40), 40)
            pygame.draw.circle(explosion, (255, 150, 50, 180), (40, 40), 35)
            pygame.draw.circle(explosion, (255, 100, 50, 150), (40, 40), 30)
            pygame.draw.circle(explosion, (255, 50, 50, 100), (40, 40), 25)
            # Kill the enemy
            enemy.kill()

        # Enemies hitting player
        if pygame.sprite.spritecollideany(self.player, self.enemies):
            # Player hit by enemy
            self.player.take_damage(10)
            # Remove the enemy that hit the player
            for enemy in pygame.sprite.spritecollide(self.player, self.enemies, True):
                pass

        # Enemy projectiles hitting player
        hits = pygame.sprite.spritecollide(self.player, self.enemy_projectiles, True)
        for _ in hits:
            self.player.take_damage(5)

        # Player collecting items
        hits = pygame.sprite.spritecollide(self.player, self.collectibles, False)
        for collectible in hits:
            if isinstance(collectible, Star):
                self.total_stars_collected += collectible.value
                self.player.score += collectible.value
            elif isinstance(collectible, HealthPack):
                self.player.health = min(
                    self.player.max_health, self.player.health + collectible.value
                )
            elif isinstance(collectible, ShieldPack):
                self.player.shield = min(
                    self.player.max_shield, self.player.shield + collectible.value
                )

            # Remove the collectible
            collectible.collect()

        # Check if player is dead
        if self.player.lives <= 0:
            # Game over - return to menu
            self.game.change_state("menu")

    def _spawn_collectibles(self, x, y, bonus_chance=False):
        """Spawn collectibles at the specified position.

        Args:
            x (int): X position
            y (int): Y position
            bonus_chance (bool): If True, increases drop chances
        """
        # Base drop chances
        star_chance = 0.4
        health_chance = 0.05
        shield_chance = 0.02

        # Apply bonus if specified
        if bonus_chance:
            star_chance = 0.6
            health_chance = 0.1
            shield_chance = 0.05

        # Star drop
        if random.random() < star_chance:
            star = Star(x, y, value=random.randint(5, 15))
            self.collectibles.add(star)
            self.all_sprites.add(star)

        # Health pack drop
        if random.random() < health_chance:
            health = HealthPack(x, y)
            self.collectibles.add(health)
            self.all_sprites.add(health)

        # Shield pack drop
        if random.random() < shield_chance:
            shield = ShieldPack(x, y)
            self.collectibles.add(shield)
            self.all_sprites.add(shield)

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

        # Draw UI elements
        self._draw_ui(screen)

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
        wave_text = f"Level: {self.current_level}  Wave: {self.wave_index + 1}/{len(self.waves)}"
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