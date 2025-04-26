"""
Collision management for the game.
"""

import pygame

from entities.collectible import HealthPack, ShieldPack, Star


class CollisionManager:
    """Handles collision detection and resolution between game objects."""

    def __init__(self, sprite_groups, collectible_manager):
        """Initialize the collision manager.

        Args:
            sprite_groups (dict): Dictionary of sprite groups
            collectible_manager: Manager for collectible items spawning
        """
        self.sprite_groups = sprite_groups
        self.collectible_manager = collectible_manager

        # Track game state
        self.total_stars_collected = 0
        
        # Statistics references - these will be set from the playing state
        self.stats = None

    def set_stats_reference(self, stats):
        """Set a reference to the stats dictionary for tracking.
        
        Args:
            stats (dict): Reference to the stats dictionary
        """
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
        self._check_projectile_enemy_collisions(player)

        # Player missiles hitting enemies
        self._check_missile_enemy_collisions(player)

        # Enemies hitting player
        if self._check_enemy_player_collisions(player):
            player_killed = True

        # Enemy projectiles hitting player
        if self._check_enemy_projectile_player_collisions(player):
            player_killed = True

        # Player collecting items
        self._check_player_collectible_collisions(player)

        return player_killed

    def _check_projectile_enemy_collisions(self, player):
        """Check for player projectiles hitting enemies.

        Args:
            player: The player object to award score to
        """
        hits = pygame.sprite.groupcollide(
            self.sprite_groups["enemies"], self.sprite_groups["player_projectiles"], False, True
        )

        for enemy, projectiles in hits.items():
            # Track shots hit
            if self.stats:
                self.stats["shots_hit"] += len(projectiles)
            
            # Force enemy death after one hit for immediate feedback
            enemy.health = 0
            player.score += enemy.value
            
            # Track enemies killed
            if self.stats:
                self.stats["enemies_killed"] += 1

            # Spawn collectibles with probability
            self.collectible_manager.spawn_collectibles(enemy.rect.centerx, enemy.rect.centery)

            # Create explosion effect (done by rendering system)

            # Kill the enemy
            enemy.kill()

    def _check_missile_enemy_collisions(self, player):
        """Check for player missiles hitting enemies.

        Args:
            player: The player object to award score to
        """
        hits = pygame.sprite.groupcollide(
            self.sprite_groups["enemies"], self.sprite_groups["player_missiles"], False, True
        )

        for enemy, missiles in hits.items():
            # Force enemy death after one missile hit
            enemy.health = 0
            player.score += enemy.value * 2  # Bonus score for missile kills
            
            # Track enemies killed
            if self.stats:
                self.stats["enemies_killed"] += 1

            # Higher chance of collectibles from missile kills
            self.collectible_manager.spawn_collectibles(
                enemy.rect.centerx, enemy.rect.centery, bonus_chance=True
            )

            # Create bigger explosion effect (done by rendering system)

            # Kill the enemy
            enemy.kill()

    def _check_enemy_player_collisions(self, player):
        """Check for enemies hitting the player.

        Args:
            player: The player object

        Returns:
            bool: True if player was killed, False otherwise
        """
        if pygame.sprite.spritecollideany(player, self.sprite_groups["enemies"]):
            # Player hit by enemy
            player.take_damage(10)
            # Remove the enemy that hit the player
            for enemy in pygame.sprite.spritecollide(player, self.sprite_groups["enemies"], True):
                pass

            # Check if player is dead
            if player.lives <= 0:
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

        for _ in hits:
            player.take_damage(5)

        # Check if player is dead
        if player.lives <= 0:
            return True

        return False

    def _check_player_collectible_collisions(self, player):
        """Check for player collecting items.

        Args:
            player: The player object
        """
        hits = pygame.sprite.spritecollide(player, self.sprite_groups["collectibles"], False)

        for collectible in hits:
            if isinstance(collectible, Star):
                self.total_stars_collected += collectible.value
                player.score += collectible.value
                
                # Track stars collected
                if self.stats:
                    self.stats["stars_collected"] += 1
                    
            elif isinstance(collectible, HealthPack):
                player.health = min(player.max_health, player.health + collectible.value)
            elif isinstance(collectible, ShieldPack):
                player.shield = min(player.max_shield, player.shield + collectible.value)

            # Remove the collectible
            collectible.collect()

    def reset(self):
        """Reset the collision manager for a new game."""
        pass  # No persistent state to reset
