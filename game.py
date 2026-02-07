import pygame
import random
import time
import math
from objects.paddle import Paddle
from objects.ball import Ball
from objects.brick import Brick
from objects.powerup import PowerUp
from objects.particles import ParticleSystem
from level_patterns import get_pattern
from save_system import save_game

WIDTH = 800
HEIGHT = 600

BRICK_COLORS = [
    (255, 50, 50),   # Neon Red
    (50, 255, 50),   # Neon Green
    (80, 80, 255),   # Neon Blue
    (255, 255, 50),  # Neon Yellow
    (255, 50, 255),  # Neon Magenta
    (50, 255, 255)   # Neon Cyan
]

class Game:
    def __init__(self, screen, level, sounds):
        self.screen = screen
        self.level = level
        self.sounds = sounds

        # Difficulty Scaling
        self.speed_boost = min(self.level * 0.15, 4.0)
        
        self.paddle = Paddle()
        self.ball = Ball(level)
        # Apply speed boost
        self.ball.base_speed += self.speed_boost
        self.ball.reset_position()

        self.bricks = self.create_bricks()
        self.hurdles = self.create_hurdles()

        self.lives = 3
        try:
            self.heart_img = pygame.image.load("assets/ui/heart.png").convert_alpha()
            self.heart_img = pygame.transform.scale(self.heart_img, (30, 30))
        except:
            self.heart_img = None

        self.powerups = []
        self.multi_balls = [self.ball]
        
        # New systems
        self.particles = ParticleSystem()
        self.shake_amount = 0
        self.last_time = time.time()
        
        # BG Animation variables
        self.scanline_y = 0
        self.bg_offset = [0, 0]

    def create_bricks(self):
        bricks = []
        pattern = get_pattern(self.level)
        
        rows = len(pattern)
        cols = len(pattern[0])
        bw, bh = 70, 25
        padx, pady = 8, 8
        
        # Center the shape
        total_w = cols * (bw + padx) - padx
        total_h = rows * (bh + pady) - pady
        offset_x = (WIDTH - total_w) // 2
        offset_y = 80

        for r in range(rows):
            Color = BRICK_COLORS[r % len(BRICK_COLORS)]
            for c in range(cols):
                if pattern[r][c]:
                    # Toughness increases with level
                    tough_chance = 0.2 + min(self.level * 0.02, 0.6)
                    health = 2 if random.random() < tough_chance else 1
                    if self.level > 20 and random.random() < 0.1: health = 3
                    
                    bricks.append(Brick(
                        offset_x + c*(bw+padx), 
                        offset_y + r*(bh+pady), 
                        bw, bh, Color, health=health
                    ))
        return bricks

    def create_hurdles(self):
        hurdles = []
        # Add hurdles from level 5 onwards
        if self.level >= 5:
            count = min(self.level // 4, 10)
            for i in range(count):
                h = Brick(
                    random.randint(100, WIDTH - 150),
                    random.randint(250, 450),
                    100, 20, (100, 100, 120), health=999 # Indestructible
                )
                h.move_dir = 1 if i % 2 == 0 else -1
                h.move_speed = 2 + (self.level * 0.1)
                hurdles.append(h)
        return hurdles

    def update(self):
        now = time.time()
        dt = now - self.last_time
        self.last_time = now

        # BG Animation
        self.scanline_y = (self.scanline_y + 2) % HEIGHT
        self.bg_offset[0] = math.sin(now * 2) * 2
        self.bg_offset[1] = math.cos(now * 2) * 2

        keys = pygame.key.get_pressed()
        self.paddle.move(keys)
        self.particles.update(dt)

        if self.shake_amount > 0:
            self.shake_amount -= 1

        # Move Hurdles
        for h in self.hurdles:
            h.rect.x += h.move_dir * h.move_speed
            if h.rect.left <= 50 or h.rect.right >= WIDTH - 50:
                h.move_dir *= -1

        for ball in self.multi_balls[:]:
            ball.move()

            # Hurdle Collision
            for h in self.hurdles:
                if ball.rect.colliderect(h.rect):
                    if abs(ball.rect.top - h.rect.bottom) < 10 or abs(ball.rect.bottom - h.rect.top) < 10:
                        ball.speed_y *= -1
                    else:
                        ball.speed_x *= -1
                    self.sounds["paddle"].play()
                    self.shake_amount = 2

            # Paddle Collision
            if ball.rect.colliderect(self.paddle.rect) and ball.speed_y > 0:
                diff = (ball.rect.centerx - self.paddle.rect.centerx) / (self.paddle.rect.width / 2)
                ball.speed_x = diff * ball.base_speed * 1.2
                ball.speed_y = -abs(ball.speed_y)
                self.sounds["paddle"].play()
                self.shake_amount = 3

            # Brick Collision
            for brick in self.bricks[:]:
                if ball.rect.colliderect(brick.rect):
                    if abs(ball.rect.top - brick.rect.bottom) < 10 or abs(ball.rect.bottom - brick.rect.top) < 10:
                        ball.speed_y *= -1
                    else:
                        ball.speed_x *= -1
                    
                    # Brick Damage Logic
                    brick.health -= 1
                    self.shake_amount = 5
                    self.particles.spawn(brick.rect.centerx, brick.rect.centery, brick.color, 10)
                    
                    if brick.health <= 0:
                        self.particles.spawn(brick.rect.centerx, brick.rect.centery, brick.color, 20)
                        self.bricks.remove(brick)
                        self.sounds["hit"].play()
                        if random.random() < 0.2:
                            try:
                                self.powerups.append(PowerUp(brick.rect.centerx, brick.rect.centery))
                            except: pass
                    else:
                        # Dim color to show damage
                        brick.color = [max(0, c - 80) for c in brick.color]
                        self.sounds["paddle"].play() # Different sound for non-break? Or just play hit
                    break

            if ball.rect.top > HEIGHT:
                if len(self.multi_balls) > 1:
                    self.multi_balls.remove(ball)
                else:
                    self.lives -= 1
                    self.sounds["game_over"].play()
                    if self.lives <= 0: return "game_over"
                    ball.reset_position()

        for power in self.powerups[:]:
            power.move()
            if not power.active:
                self.powerups.remove(power)
                continue
            if power.rect.colliderect(self.paddle.rect):
                if power.type == "MULTI":
                    for b in self.multi_balls[:2]:
                        self.multi_balls.append(b.clone())
                elif power.type == "SPEED":
                    for b in self.multi_balls: b.activate_speed_power()
                elif power.type == "BIG": self.paddle.activate_big_paddle()
                elif power.type == "SMALL": self.paddle.activate_small_paddle()
                elif power.type == "SHIELD": self.paddle.activate_shield()
                self.powerups.remove(power)

        if not self.bricks:
            return "next_level"

        return None

    def draw(self):
        draw_offset = (random.randint(-self.shake_amount, self.shake_amount), 
                       random.randint(-self.shake_amount, self.shake_amount))

        self.screen.fill((5, 5, 20)) 
        
        # Dynamic Pulse Background
        pulse = abs(math.sin(time.time() * 2)) * 10
        for i in range(0, WIDTH, 40):
            pygame.draw.line(self.screen, (20, 20, 40 + pulse), (i + draw_offset[0], 0), (i + draw_offset[0], HEIGHT))
        for i in range(0, HEIGHT, 40):
            pygame.draw.line(self.screen, (20, 20, 40 + pulse), (0, i + draw_offset[1]), (WIDTH, i + draw_offset[1]))

        # High-tech Scanline Animation
        scanline_surf = pygame.Surface((WIDTH, 2), pygame.SRCALPHA)
        pygame.draw.rect(scanline_surf, (0, 255, 255, 40), (0, 0, WIDTH, 2))
        self.screen.blit(scanline_surf, (0, self.scanline_y))

        # Vignette Effect
        vignette = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        # Using a simple gradient/radial simulation
        for i in range(0, 100, 10):
            alpha = 150 - (i * 1.5)
            pygame.draw.rect(vignette, (0, 0, 0, alpha), (0, 0, WIDTH, HEIGHT), i)
        self.screen.blit(vignette, (0,0))

        # Draw Game Objects with offset
        for brick in self.bricks:
            brick.draw(self.screen)
        
        for h in self.hurdles:
            h.draw(self.screen)
        
        self.paddle.draw(self.screen)
        
        for ball in self.multi_balls:
            ball.draw(self.screen)
            
        for power in self.powerups:
            power.draw(self.screen)

        self.particles.draw(self.screen)

        # UI
        if self.heart_img:
            for i in range(self.lives):
                self.screen.blit(self.heart_img, (15 + i*35, 15))
        else:
            font = pygame.font.SysFont("Arial", 24)
            lives_text = font.render(f"LIVES: {self.lives}", True, (255, 255, 255))
            self.screen.blit(lives_text, (20, 20))
 