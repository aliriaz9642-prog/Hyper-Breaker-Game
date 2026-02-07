import pygame
import time
import random

WIDTH = 800
HEIGHT = 600

class Ball:
    def __init__(self, level):
        self.level = level
        self.radius = 10  # Slightly larger for better visibility
        self.x = 400
        self.y = 300
        self.base_speed = 5 + level * 0.2
        angle = random.uniform(0.4, 0.8) * (-1 if random.random() > 0.5 else 1)
        self.speed_x = self.base_speed * angle
        self.speed_y = -self.base_speed
        self.rect = pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)
        self.color = (0, 255, 255)  # Cyan/Neon Blue
        self.trail = []
        self.max_trail_length = 10
        self.speed_multiplier = 1
        self.speed_power_end_time = 0

    def reset_position(self):
        self.x = 400
        self.y = 300
        self.rect.center = (self.x, self.y)
        self.speed_x = self.base_speed * random.uniform(-0.5, 0.5)
        self.speed_y = -self.base_speed
        self.trail = []
        self.speed_multiplier = 1
        self.speed_power_end_time = 0

    def move(self):
        if self.speed_power_end_time and time.time() > self.speed_power_end_time:
            self.speed_multiplier = 1
            self.speed_power_end_time = 0

        # Save trail
        self.trail.insert(0, self.rect.center)
        if len(self.trail) > self.max_trail_length:
            self.trail.pop()

        self.x += self.speed_x * self.speed_multiplier
        self.y += self.speed_y * self.speed_multiplier
        self.rect.center = (int(self.x), int(self.y))

        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.speed_x *= -1
            self.x = max(self.radius, min(WIDTH - self.radius, self.x))

        if self.rect.top <= 0:
            self.speed_y *= -1
            self.y = self.radius

    def draw(self, screen):
        # Draw trail
        for i, pos in enumerate(self.trail):
            alpha = int(255 * (1 - i / self.max_trail_length))
            radius = int(self.radius * (1 - i / self.max_trail_length))
            if radius < 1: radius = 1
            s = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(s, (*self.color, alpha // 2), (radius, radius), radius)
            screen.blit(s, (pos[0] - radius, pos[1] - radius))

        # Draw main ball with a glow
        glow_radius = self.radius + 4
        s = pygame.Surface((glow_radius * 2, glow_radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(s, (*self.color, 100), (glow_radius, glow_radius), glow_radius)
        screen.blit(s, (self.rect.centerx - glow_radius, self.rect.centery - glow_radius))
        
        pygame.draw.circle(screen, (255, 255, 255), self.rect.center, self.radius) # Core is white
        pygame.draw.circle(screen, self.color, self.rect.center, self.radius, 2)   # Outer ring is color

    def activate_speed_power(self, duration=8):
        self.speed_multiplier = 1.6
        self.speed_power_end_time = time.time() + duration

    def clone(self):
        new_ball = Ball(self.level)
        new_ball.x, new_ball.y = self.x, self.y
        new_ball.rect.center = self.rect.center
        new_ball.speed_x = random.choice([-1, 1]) * abs(self.speed_x)
        new_ball.speed_y = -abs(self.speed_y)
        return new_ball
