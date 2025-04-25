"""
Enemy classes for Machines of God game.
"""

import math
import random

import pygame


class Enemy(pygame.sprite.Sprite):
    """Base class for all enemies."""

    def __init__(self, x, y, difficulty=1.0):
        """Initialize an enemy sprite.

        Args:
            x (int): Initial x position
            y (int): Initial y position
            difficulty (float): Difficulty multiplier
        """
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill((255, 0, 0))  # Transparent background
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

        # Randomize enemy stats for variety
        self.variance = random.uniform(0.8, 1.2)
        self.difficulty = difficulty

        # Base stats
        self.base_health = 20
        self.base_speed = 60
        self.movement_type = "linear"  # Default movement type

        # Applied stats (affected by difficulty and variance)
        self.health = int(self.base_health * self.difficulty * self.variance)
        self.speed = self.base_speed * self.difficulty * self.variance
        self.value = int(10 * self.difficulty * self.variance)  # Base point value

        # Movement properties
        self.velocity = pygame.math.Vector2(0, self.speed)
        self.amplitude = random.randint(20, 100)  # For zigzag movement
        self.frequency = random.uniform(1.0, 3.0)  # For zigzag movement
        self.timer = random.random() * math.pi * 2  # Randomize starting phase

    def update(self, dt):
        """Update the enemy's position and state.

        Args:
            dt (float): Time elapsed since last update in seconds
        """
        # Update movement based on pattern
        if self.movement_type == "linear":
            self._linear_movement(dt)
        elif self.movement_type == "zigzag":
            self._zigzag_movement(dt)
        elif self.movement_type == "circular":
            self._circular_movement(dt)

        # Check if enemy is off-screen
        screen_height = pygame.display.get_surface().get_size()[1]
        if self.rect.top > screen_height:
            self.kill()

    def _linear_movement(self, dt):
        """Basic downward movement.

        Args:
            dt (float): Time elapsed since last update in seconds
        """
        self.rect.y += self.speed * dt

    def _zigzag_movement(self, dt):
        """Zigzag movement pattern.

        Args:
            dt (float): Time elapsed since last update in seconds
        """
        self.timer += dt
        # Oscillate horizontal direction using sine wave
        self.velocity.x = math.sin(self.timer * self.frequency) * self.amplitude
        self.velocity.y = self.speed

        # Normalize and apply speed
        if self.velocity.length() > 0:
            self.velocity.normalize_ip()

        # Update position
        self.rect.x += self.velocity.x * dt
        self.rect.y += self.velocity.y * dt

    def _circular_movement(self, dt):
        """Circular movement pattern.

        Args:
            dt (float): Time elapsed since last update in seconds
        """
        self.timer += dt
        # Create circular motion using sin and cos
        self.velocity.x = math.sin(self.timer * 2) * 0.7
        self.velocity.y = 0.5 + math.cos(self.timer * 2) * 0.3

        # Normalize and apply speed
        if self.velocity.length() > 0:
            self.velocity.normalize_ip()

        # Update position
        self.rect.x += self.velocity.x * self.speed * dt
        self.rect.y += self.velocity.y * self.speed * dt

    def take_damage(self, amount):
        """Reduce enemy health by the specified amount.

        Args:
            amount (int): Amount of damage to take

        Returns:
            bool: True if the enemy is destroyed, False otherwise
        """
        self.health -= amount
        if self.health <= 0:
            self.kill()
            return True
        return False

    def shoot(self, current_time, projectile_group):
        """Method to be overridden by enemy subclasses that can shoot.

        Args:
            current_time (float): Current game time in seconds
            projectile_group (pygame.sprite.Group): Group to add projectiles to
        """
        pass


class BasicEnemy(Enemy):
    """Basic enemy with simple behavior."""

    def __init__(self, x, y, difficulty=1.0):
        """Initialize a basic enemy.

        Args:
            x (int): Initial x position
            y (int): Initial y position
            difficulty (float): Difficulty multiplier
        """
        super().__init__(x, y, difficulty)

        # Draw a simple enemy shape
        pygame.draw.circle(self.image, (200, 50, 50), (20, 20), 18)
        pygame.draw.circle(self.image, (150, 0, 0), (20, 20), 12)

        # Set transparent color
        self.image.set_colorkey((255, 0, 0))


class ZigzagEnemy(Enemy):
    """Enemy that moves in a zigzag pattern."""

    def __init__(self, x, y, difficulty=1.0):
        """Initialize a zigzag enemy.

        Args:
            x (int): Initial x position
            y (int): Initial y position
            difficulty (float): Difficulty multiplier
        """
        super().__init__(x, y, difficulty)
        self.movement_type = "zigzag"

        # Draw a simple enemy shape
        pygame.draw.polygon(self.image, (200, 150, 50), [(0, 20), (20, 0), (40, 20), (20, 40)])

        # Set transparent color
        self.image.set_colorkey((255, 0, 0))


class EnemyProjectile(pygame.sprite.Sprite):
    """Projectile fired by enemies."""

    def __init__(self, x, y, speed=200, damage=5):
        """Initialize a projectile.

        Args:
            x (int): X position
            y (int): Y position
            speed (int): Speed in pixels per second
                (positive for downward movement)
            damage (int): Damage amount
        """
        super().__init__()
        self.image = pygame.Surface((6, 15), pygame.SRCALPHA)

        # Create a visible enemy projectile
        pygame.draw.line(self.image, (255, 100, 100), (3, 0), (3, 15), 3)
        pygame.draw.circle(self.image, (255, 200, 200), (3, 3), 3)

        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.top = y
        self.velocity = pygame.math.Vector2(0, speed)
        self.damage = damage

    def update(self, dt):
        """Update projectile position.

        Args:
            dt (float): Time elapsed since last update
        """
        self.rect.y += self.velocity.y * dt

        # Remove if off screen
        screen_height = pygame.display.get_surface().get_size()[1]
        if self.rect.top > screen_height:
            self.kill()


class ShooterEnemy(Enemy):
    """Enemy that shoots projectiles."""

    def __init__(self, x, y, difficulty=1.0):
        """Initialize a shooter enemy.

        Args:
            x (int): Initial x position
            y (int): Initial y position
            difficulty (float): Difficulty multiplier
        """
        super().__init__(x, y, difficulty)

        # Draw a simple enemy shape
        pygame.draw.circle(self.image, (50, 50, 200), (20, 20), 18)
        pygame.draw.rect(self.image, (0, 0, 150), pygame.Rect(10, 25, 20, 15))

        # Set transparent color
        self.image.set_colorkey((255, 0, 0))

        # Shooting properties
        self.can_shoot = True
        self.fire_rate = 1.5  # seconds between shots
        self.last_shot_time = random.random() * 1.5  # Randomize first shot

    def shoot(self, current_time, projectile_group):
        """Create a projectile if enough time has passed since the last shot.

        Args:
            current_time (float): Current game time in seconds
            projectile_group (pygame.sprite.Group): Group to add projectiles to

        Returns:
            bool: True if a projectile was created, False otherwise
        """
        if current_time - self.last_shot_time >= self.fire_rate:
            self.last_shot_time = current_time

            # Create a proper projectile
            bullet = EnemyProjectile(self.rect.centerx, self.rect.bottom)
            projectile_group.add(bullet)
            return True

        return False


class HeavyBomber(Enemy):
    """Heavy enemy that is slow but takes multiple hits to destroy."""

    def __init__(self, x, y, difficulty=1.0):
        """Initialize a heavy bomber enemy.

        Args:
            x (int): Initial x position
            y (int): Initial y position
            difficulty (float): Difficulty multiplier
        """
        super().__init__(x, y, difficulty)

        # Override base stats
        self.base_health = 80
        self.base_speed = 30

        # Recalculate with higher difficulty scaling
        self.health = int(self.base_health * self.difficulty * self.variance)
        self.speed = self.base_speed * self.difficulty * self.variance
        self.value = int(40 * self.difficulty * self.variance)  # Worth more points

        # Update velocity with new speed
        self.velocity = pygame.math.Vector2(0, self.speed)

        # Draw a larger, heavy-looking enemy
        self.image = pygame.Surface((60, 60))
        self.image.fill((255, 0, 0))
        pygame.draw.rect(self.image, (180, 100, 180), pygame.Rect(5, 5, 50, 50))
        pygame.draw.rect(self.image, (150, 80, 150), pygame.Rect(15, 15, 30, 30))
        pygame.draw.circle(self.image, (100, 50, 100), (30, 30), 10)

        # Update rect for larger size
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

        # Set transparent color
        self.image.set_colorkey((255, 0, 0))

    def _linear_movement(self, dt):
        """Slower downward movement.

        Args:
            dt (float): Time elapsed since last update in seconds
        """
        # Move with slight side-to-side rocking
        self.timer += dt
        self.rect.x += math.sin(self.timer) * 0.5
        self.rect.y += self.speed * dt


class DartEnemy(Enemy):
    """Fast enemy that makes quick dashes across the screen."""

    def __init__(self, x, y, difficulty=1.0):
        """Initialize a dart enemy.

        Args:
            x (int): Initial x position
            y (int): Initial y position
            difficulty (float): Difficulty multiplier
        """
        super().__init__(x, y, difficulty)

        # Override base stats for dart enemy
        self.base_health = 15
        self.base_speed = 120  # Very fast

        # Recalculate with higher speed variance
        self.variance = random.uniform(0.9, 1.3)  # More variance in speed
        self.health = int(self.base_health * self.difficulty * self.variance)
        self.speed = self.base_speed * self.difficulty * self.variance
        self.value = int(5 * self.difficulty * self.variance)  # Low point value

        # Dash properties
        self.dash_ready = True
        self.dash_cooldown = random.uniform(1.0, 3.0)  # Random dash interval
        self.dash_timer = 0
        self.dash_duration = 0.3  # How long the dash lasts
        self.is_dashing = False
        self.dash_speed_multiplier = 3.0  # Speed boost during dash
        self.dash_direction = pygame.math.Vector2(random.uniform(-0.5, 0.5), 1).normalize()

        # Normal movement is still downward
        self.velocity = pygame.math.Vector2(0, self.speed)

        # Draw a sleek, aerodynamic enemy
        self.image = pygame.Surface((30, 45))
        self.image.fill((255, 0, 0))  # Transparent color

        # Draw dart body
        pygame.draw.polygon(
            self.image, (50, 180, 255), [(15, 0), (0, 25), (15, 45), (30, 25)]  # Light blue color
        )
        # Draw a streak in the middle
        pygame.draw.line(self.image, (100, 220, 255), (15, 0), (15, 45), 3)
        # Add engine glow
        pygame.draw.circle(self.image, (200, 230, 255), (15, 35), 7)

        # Update rect for new size
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

        # Set transparent color
        self.image.set_colorkey((255, 0, 0))

    def update(self, dt):
        """Update the enemy's position and state.

        Args:
            dt (float): Time elapsed since last update in seconds
        """
        # Update dash cooldown
        if not self.is_dashing:
            if not self.dash_ready:
                self.dash_timer += dt
                if self.dash_timer >= self.dash_cooldown:
                    self.dash_ready = True
                    self.dash_timer = 0
                    # Calculate new dash direction (mostly downward but with some angle)
                    self.dash_direction = pygame.math.Vector2(
                        random.uniform(-0.5, 0.5), 1  # Some side motion  # Mostly downward
                    ).normalize()

            # Check if we should start dashing
            elif random.random() < 0.1 * dt:  # Small chance to dash each frame
                self.is_dashing = True
                self.dash_ready = False
                self.dash_timer = 0
        else:
            # Update dash duration
            self.dash_timer += dt
            if self.dash_timer >= self.dash_duration:
                self.is_dashing = False
                self.dash_timer = 0

        # Move based on current state
        if self.is_dashing:
            # Fast movement in dash direction
            dash_velocity = self.dash_direction * self.speed * self.dash_speed_multiplier
            self.rect.x += dash_velocity.x * dt
            self.rect.y += dash_velocity.y * dt

            # Keep within screen bounds horizontally
            screen_width = pygame.display.get_surface().get_size()[0]
            if self.rect.left < 0:
                self.rect.left = 0
                self.dash_direction.x = abs(self.dash_direction.x)  # Bounce
            elif self.rect.right > screen_width:
                self.rect.right = screen_width
                self.dash_direction.x = -abs(self.dash_direction.x)  # Bounce
        else:
            # Normal downward movement
            self.rect.y += self.speed * dt

        # Check if enemy is off-screen
        screen_height = pygame.display.get_surface().get_size()[1]
        if self.rect.top > screen_height:
            self.kill()


class ShieldBearerEnemy(Enemy):
    """Enemy with a front-facing shield that blocks attacks from one direction."""

    def __init__(self, x, y, difficulty=1.0):
        """Initialize a shield bearer enemy.

        Args:
            x (int): Initial x position
            y (int): Initial y position
            difficulty (float): Difficulty multiplier
        """
        super().__init__(x, y, difficulty)

        # Override base stats
        self.base_health = 40
        self.base_speed = 40  # Slow moving

        # Recalculate stats with difficulty and variance
        self.health = int(self.base_health * self.difficulty * self.variance)
        self.speed = self.base_speed * self.difficulty * self.variance
        self.value = int(20 * self.difficulty * self.variance)  # Medium point value

        # Shield properties
        self.shield_active = True
        self.shield_direction = pygame.math.Vector2(0, 1)  # Facing downward
        self.shield_angle = 180  # Degrees (facing downward)
        self.shield_arc = 120  # Degrees of protection arc
        self.shield_rotation_speed = 0.5  # Radians per second
        self.change_direction_timer = random.uniform(2.0, 5.0)  # Time until shield rotates
        self.timer = 0

        # Movement properties
        self.velocity = pygame.math.Vector2(0, self.speed)

        # Create the enemy image
        self.image = pygame.Surface((50, 50))
        self.image.fill((255, 0, 0))  # Transparent color

        # Draw the enemy body
        pygame.draw.circle(self.image, (150, 120, 40), (25, 25), 15)  # Bronze body

        # Draw the shield (will be updated in render)
        self.shield_image = pygame.Surface((50, 50), pygame.SRCALPHA)
        self._update_shield_position()

        # Update rect
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

        # Set transparent color
        self.image.set_colorkey((255, 0, 0))

    def _update_shield_position(self):
        """Update the shield position and appearance based on current direction."""
        # Clear the shield surface
        self.shield_image.fill((0, 0, 0, 0))

        # Calculate shield arc points
        center = (25, 25)
        radius = 22
        start_angle = math.radians(self.shield_angle - self.shield_arc / 2)
        end_angle = math.radians(self.shield_angle + self.shield_arc / 2)

        # Draw shield arc
        points = [center]
        for angle in range(int(math.degrees(start_angle)), int(math.degrees(end_angle)) + 1, 5):
            rad = math.radians(angle)
            x = center[0] + radius * math.cos(rad)
            y = center[1] + radius * math.sin(rad)
            points.append((x, y))
        points.append(center)

        # Draw the shield
        if len(points) > 2:
            pygame.draw.polygon(self.shield_image, (80, 180, 200, 180), points)  # Blue shield
            pygame.draw.polygon(self.shield_image, (120, 220, 255, 180), points, 2)  # Shield border

    def update(self, dt):
        """Update the enemy's position and state.

        Args:
            dt (float): Time elapsed since last update in seconds
        """
        # Update timer
        self.timer += dt

        # Check if it's time to change shield direction
        if self.timer >= self.change_direction_timer:
            self.timer = 0
            self.change_direction_timer = random.uniform(3.0, 6.0)

            # Randomly change shield direction
            new_angle = random.choice([0, 45, 90, 135, 180, 225, 270, 315])
            self.shield_angle = new_angle
            angle_rad = math.radians(new_angle)
            self.shield_direction.x = math.cos(angle_rad)
            self.shield_direction.y = math.sin(angle_rad)

            # Update shield appearance
            self._update_shield_position()

        # Move downward with slight side motion
        drift = math.sin(self.timer * 0.5) * 20 * dt
        self.rect.x += drift
        self.rect.y += self.speed * dt

        # Check if enemy is off-screen
        screen_height = pygame.display.get_surface().get_size()[1]
        if self.rect.top > screen_height:
            self.kill()

    def take_damage(self, amount):
        """Reduce enemy health by the specified amount, taking shield into account.

        Args:
            amount (int): Amount of damage to take

        Returns:
            bool: True if the enemy is destroyed, False otherwise
        """
        # Check if hit is on the shielded side
        if self.shield_active:
            # Get the attack direction (assumed to be from above by default)
            attack_vector = pygame.math.Vector2(0, -1)

            # Calculate angle between attack and shield direction
            angle = math.degrees(attack_vector.angle_to(self.shield_direction))

            # Check if attack is within the shielded arc
            if abs(angle) <= self.shield_arc / 2:
                # Attack blocked, reduce damage significantly
                amount = max(1, amount // 5)

        # Apply damage
        self.health -= amount
        if self.health <= 0:
            self.kill()
            return True
        return False

    def render(self, screen):
        """Custom rendering to show the shield.

        Args:
            screen (pygame.Surface): Surface to render to
        """
        screen.blit(self.image, self.rect)
        screen.blit(self.shield_image, self.rect)
