import pygame
import time

WIDTH = 800

class Paddle:
    def __init__(self):
        self.base_width = 120
        self.height = 15
        self.x = 340
        self.y = 560
        self.speed = 10  # Increased speed for better feel
        self.width = self.base_width
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.color = (255, 0, 255)  # Neon Magenta
        self.target_x = self.x
        self.size_power_end_time = 0
        self.shield_end_time = 0
        self.shield_active = False

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.x < WIDTH - self.rect.width:
            self.rect.x += self.speed

        if self.size_power_end_time and time.time() > self.size_power_end_time:
            self.reset_size()

        if self.shield_end_time and time.time() > self.shield_end_time:
            self.shield_active = False
            self.shield_end_time = 0

    def draw(self, screen):
        # Draw Glow
        glow_rect = self.rect.inflate(10, 10)
        s = pygame.Surface((glow_rect.width, glow_rect.height), pygame.SRCALPHA)
        pygame.draw.rect(s, (*self.color, 80), (0, 0, glow_rect.width, glow_rect.height), border_radius=5)
        screen.blit(s, glow_rect.topleft)

        # Draw Paddle
        pygame.draw.rect(screen, (255, 255, 255), self.rect, border_radius=5)
        pygame.draw.rect(screen, self.color, self.rect, 2, border_radius=5)

        if self.shield_active:
            shield_rect = pygame.Rect(self.rect.x, self.rect.y - 12, self.rect.width, 4)
            pygame.draw.rect(screen, (0, 255, 255), shield_rect, border_radius=2)
            # Add shield glow
            s = pygame.Surface((shield_rect.width, 20), pygame.SRCALPHA)
            pygame.draw.rect(s, (0, 255, 255, 100), (0, 0, shield_rect.width, 20), border_radius=10)
            screen.blit(s, (shield_rect.x, shield_rect.y - 10))

    # =================================================
    # 🔥 POWER FUNCTIONS (OPTIONAL – SAFE)
    # =================================================

    def activate_big_paddle(self, duration=6):
        center = self.rect.centerx
        self.rect.width = 180
        self.rect.centerx = center
        self.size_power_end_time = time.time() + duration

    def activate_small_paddle(self, duration=10):
        center = self.rect.centerx
        self.rect.width = 80
        self.rect.centerx = center
        self.size_power_end_time = time.time() + duration

    def reset_size(self):
        center = self.rect.centerx
        self.rect.width = self.base_width
        self.rect.centerx = center
        self.size_power_end_time = 0

    def activate_shield(self, duration=8):
        self.shield_active = True
        self.shield_end_time = time.time() + duration
