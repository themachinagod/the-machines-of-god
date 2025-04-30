"""
Collision management for the game.
"""

import pygame

from entities.collectible import HealthPack, ShieldPack, Star
from utils.logger import get_logger


class CollisionManager:
    """Handles collision detection and resolution between game objects."""

    def __init__(self, sprite_groups, collectible_manager):
        """Initialize the collision manager.

        Args:
            sprite_groups (dict): Dictionary of sprite groups
            collectible_manager: Manager for collectible items spawning
        """
        # Initialize logger
        self.logger = get_logger()
        self.logger.info("Initializing CollisionManager")

        self.sprite_groups = sprite_groups
        self.collectible_manager = collectible_manager
        self.logger.debug("Sprite groups registered: %s", list(sprite_groups.keys()))

        # Track game state
        self.total_stars_collected = 0

        # Statistics references - these will be set from the playing state
        self.stats = None

        self.logger.info("CollisionManager initialized successfully")

    def set_stats_reference(self, stats):
        """Set a reference to the stats dictionary for tracking.

        Args:
            stats (dict): Reference to the stats dictionary
        """
        self.logger.debug("Setting stats reference: %s", stats)
        self.stats = stats

    def check_collisions(self, player):
        """Check and handle all collisions in the game.

        Args:
            player: The player object

        Returns:
            bool: True if the player was killed, False otherwise
        """
        player_killed = False

        # Player projectiles hitting enemies
        projectile_hits = self._check_projectile_enemy_collisions(player)
        if projectile_hits > 0:
            self.logger.debug("Player projectiles hit %d enemies", projectile_hits)

        # Player missiles hitting enemies
        missile_hits = self._check_missile_enemy_collisions(player)
        if missile_hits > 0:
            self.logger.debug("Player missiles hit %d enemies", missile_hits)

        # Enemies hitting player
        if self._check_enemy_player_collisions(player):
            self.logger.info("Player killed by enemy collision")
            player_killed = True

        # Enemy projectiles hitting player
        if self._check_enemy_projectile_player_collisions(player):
            self.logger.info("Player killed by enemy projectile")
            player_killed = True

        # Player collecting items
        collectibles = self._check_player_collectible_collisions(player)
        if collectibles > 0:
            self.logger.debug("Player collected %d items", collectibles)

        return player_killed

    def _check_projectile_enemy_collisions(self, player):
        """Check for player projectiles hitting enemies.

        Args:
            player: The player object to award score to

        Returns:
            int: Number of enemies hit
        """
        hits = pygame.sprite.groupcollide(
            self.sprite_groups["enemies"], self.sprite_groups["player_projectiles"], False, True
        )

        hit_count = len(hits)

        for enemy, projectiles in hits.items():
            # Track shots hit
            if self.stats:
                self.stats["shots_hit"] += len(projectiles)
                self.logger.debug("Stats updated: shots_hit +%d", len(projectiles))

            # Force enemy death after one hit for immediate feedback
            enemy.health = 0
            player.score += enemy.value
            self.logger.debug("Enemy destroyed by projectile, player score +%d", enemy.value)

            # Track enemies killed
            if self.stats:
                self.stats["enemies_killed"] += 1
                self.logger.debug("Stats updated: enemies_killed +1")

            # Spawn collectibles with probability
            self.collectible_manager.spawn_collectibles(enemy.rect.centerx, enemy.rect.centery)
            self.logger.debug(
                "Attempting to spawn collectibles at (%d, %d)",
                enemy.rect.centerx,
                enemy.rect.centery,
            )

            # Create explosion effect (done by rendering system)

            # Kill the enemy
            enemy.kill()

        return hit_count

    def _check_missile_enemy_collisions(self, player):
        """Check for player missiles hitting enemies.

        Args:
            player: The player object to award score to

        Returns:
            int: Number of enemies hit
        """
        hits = pygame.sprite.groupcollide(
            self.sprite_groups["enemies"], self.sprite_groups["player_missiles"], False, True
        )

        hit_count = len(hits)

        for enemy, missiles in hits.items():
            # Force enemy death after one missile hit
            enemy.health = 0
            score_increase = enemy.value * 2
            player.score += score_increase  # Bonus score for missile kills
            self.logger.debug("Enemy destroyed by missile, player score +%d", score_increase)

            # Track enemies killed
            if self.stats:
                self.stats["enemies_killed"] += 1
                self.logger.debug("Stats updated: enemies_killed +1")

            # Higher chance of collectibles from missile kills
            self.collectible_manager.spawn_collectibles(
                enemy.rect.centerx, enemy.rect.centery, bonus_chance=True
            )
            self.logger.debug(
                "Attempting to spawn bonus collectibles at (%d, %d)",
                enemy.rect.centerx,
                enemy.rect.centery,
            )

            # Create bigger explosion effect (done by rendering system)

            # Kill the enemy
            enemy.kill()

        return hit_count

    def _check_enemy_player_collisions(self, player):
        """Check for enemies hitting the player.

        Args:
            player: The player object

        Returns:
            bool: True if player was killed, False otherwise
        """
        collisions = pygame.sprite.spritecollide(player, self.sprite_groups["enemies"], False)

        if collisions:
            self.logger.info("Player collided with %d enemies", len(collisions))
            # Player hit by enemy
            player.take_damage(10)
            self.logger.debug("Player took 10 damage, health now: %d", player.health)

            # Remove the enemy that hit the player
            for enemy in pygame.sprite.spritecollide(player, self.sprite_groups["enemies"], True):
                self.logger.debug("Enemy removed after collision with player")

            # Check if player is dead
            if player.lives <= 0:
                self.logger.info("Player lost all lives after enemy collision")
                return True

        return False

    def _check_enemy_projectile_player_collisions(self, player):
        """Check for enemy projectiles hitting the player.

        Args:
            player: The player object

        Returns:
            bool: True if player was killed, False otherwise
        """
        hits = pygame.sprite.spritecollide(player, self.sprite_groups["enemy_projectiles"], True)

        if hits:
            damage = len(hits) * 5
            self.logger.info("Player hit by %d enemy projectiles for %d damage", len(hits), damage)

            for _ in hits:
                player.take_damage(5)

            # Check if player is dead
            if player.lives <= 0:
                self.logger.info("Player lost all lives after projectile hit")
                return True

        return False

    def _check_player_collectible_collisions(self, player):
        """Check for player collecting items.

        Args:
            player: The player object

        Returns:
            int: Number of collectibles collected
        """
        hits = pygame.sprite.spritecollide(player, self.sprite_groups["collectibles"], False)

        for collectible in hits:
            if isinstance(collectible, Star):
                self.total_stars_collected += collectible.value
                player.score += collectible.value
                self.logger.debug(
                    "Player collected Star worth %d points, total stars: %d",
                    collectible.value,
                    self.total_stars_collected,
                )

                # Track stars collected
                if self.stats:
                    self.stats["stars_collected"] += 1
                    self.logger.debug("Stats updated: stars_collected +1")

            elif isinstance(collectible, HealthPack):
                old_health = player.health
                player.health = min(player.max_health, player.health + collectible.value)
                health_gained = player.health - old_health
                self.logger.debug(
                    "Player collected HealthPack, restored %d health. Health now: %d/%d",
                    health_gained,
                    player.health,
                    player.max_health,
                )

            elif isinstance(collectible, ShieldPack):
                old_shield = player.shield
                player.shield = min(player.max_shield, player.shield + collectible.value)
                shield_gained = player.shield - old_shield
                self.logger.debug(
                    "Player collected ShieldPack, restored %d shield. Shield now: %d/%d",
                    shield_gained,
                    player.shield,
                    player.max_shield,
                )

            # Remove the collectible
            collectible.collect()

        return len(hits)

    def reset(self):
        """Reset the collision manager for a new game."""
        self.logger.info("Resetting CollisionManager")
        # No persistent state to reset
        pass
