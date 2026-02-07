import pygame
import random

class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.size = random.randint(2, 5)
        self.vel_x = random.uniform(-3, 3)
        self.vel_y = random.uniform(-3, 3)
        self.lifetime = 1.0  # seconds
        self.alpha = 255

    def update(self, dt):
        self.x += self.vel_x
        self.y += self.vel_y
        self.lifetime -= dt
        self.alpha = max(0, int(255 * self.lifetime))
        self.size *= 0.95

    def is_dead(self):
        return self.lifetime <= 0

    def draw(self, screen):
        # Create a surface for the particle to support alpha
        s = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        pygame.draw.circle(s, (*self.color, self.alpha), (self.size, self.size), self.size)
        screen.blit(s, (self.x - self.size, self.y - self.size))

class ParticleSystem:
    def __init__(self):
        self.particles = []

    def spawn(self, x, y, color, count=10):
        for _ in range(count):
            self.particles.append(Particle(x, y, color))

    def update(self, dt):
        for p in self.particles[:]:
            p.update(dt)
            if p.is_dead():
                self.particles.remove(p)

    def draw(self, screen):
        for p in self.particles:
            p.draw(screen)
