import pygame
import time
import math

class Brick:
    def __init__(self, x, y, width=60, height=20, color=(180, 0, 0), health=1):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = list(color)
        self.health = health
        self.max_health = health

    def draw(self, screen):
        # Special look for Indestructible Hurdles
        if self.health > 100:
            # Draw hurdle with a "Plasma Shield" glow
            pygame.draw.rect(screen, (40, 40, 60), self.rect, border_radius=5)
            # Pulsing blue border
            pulse = abs(math.sin(time.time() * 5)) * 50
            border_color = (100 + pulse, 150 + pulse, 255)
            pygame.draw.rect(screen, border_color, self.rect, 2, border_radius=5)
            # Add scanline over hurdle
            sy = self.rect.y + (int(time.time() * 40) % self.rect.height)
            pygame.draw.line(screen, (150, 200, 255, 100), (self.rect.x, sy), (self.rect.right, sy))
            return

        # Regular Brick drawing
        pygame.draw.rect(screen, self.color, self.rect, border_radius=3)
        
        # Add a light highlight on top for 3D/glassy feel
        highlight_rect = pygame.Rect(self.rect.x + 2, self.rect.y + 2, self.rect.width - 4, self.rect.height // 2)
        pygame.draw.rect(screen, (255, 255, 255, 120), highlight_rect, border_radius=2)
        
        # Outer border
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 1, border_radius=3)
