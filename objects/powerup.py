import pygame
import random

POWER_TYPES = ["MULTI", "SPEED", "BIG", "SMALL", "SHIELD"]

POWER_IMAGES = {
    "MULTI": "assets/powers/multiball.png",
    "SPEED": "assets/powers/speed.png",
    "BIG": "assets/powers/paddle_big.png",
    "SMALL": "assets/powers/paddle_small.png",
    "SHIELD": "assets/powers/shield.png",
}

POWER_COLORS = {
    "MULTI": (255, 255, 0),    # Yellow
    "SPEED": (255, 50, 50),    # Red
    "BIG": (0, 255, 0),        # Green
    "SMALL": (200, 200, 200),  # Grey
    "SHIELD": (0, 255, 255)    # Cyan
}

class PowerUp:
    def __init__(self, x, y):
        self.type = random.choice(POWER_TYPES)
        self.color = POWER_COLORS.get(self.type, (255, 255, 255))
        try:
            self.image = pygame.image.load(POWER_IMAGES[self.type]).convert_alpha()
            self.rect = self.image.get_rect()
        except:
            self.image = None
            self.rect = pygame.Rect(0, 0, 24, 24)
            
        self.rect.center = (x, y)
        self.speed = 4
        self.active = True
        self.angle = 0

    def move(self):
        self.rect.y += self.speed
        self.angle += 5
        if self.rect.top > 600:
            self.active = False

    def draw(self, screen):
        # Draw Glow
        glow_size = self.rect.width + 15
        s = pygame.Surface((glow_size, glow_size), pygame.SRCALPHA)
        pygame.draw.circle(s, (*self.color, 80), (glow_size//2, glow_size//2), glow_size//2)
        screen.blit(s, (self.rect.centerx - glow_size//2, self.rect.centery - glow_size//2))

        if self.image:
            rotated = pygame.transform.rotate(self.image, self.angle)
            new_rect = rotated.get_rect(center=self.rect.center)
            screen.blit(rotated, new_rect)
        else:
            # Fallback futuristic diamond
            points = [
                (self.rect.centerx, self.rect.top),
                (self.rect.right, self.rect.centery),
                (self.rect.centerx, self.rect.bottom),
                (self.rect.left, self.rect.centery)
            ]
            pygame.draw.polygon(screen, (255, 255, 255), points)
            pygame.draw.polygon(screen, self.color, points, 2)
            
            font = pygame.font.SysFont("Arial", 14, bold=True)
            txt = font.render(self.type[0], True, self.color)
            screen.blit(txt, (self.rect.centerx - txt.get_width()//2, self.rect.centery - txt.get_height()//2))
