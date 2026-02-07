import pygame
import os
from menu import MainMenu
from level_select import LevelSelect
from save_system import load_game, save_game
from game import Game

# ============================
# CONSTANTS
# ============================
WIDTH = 800
HEIGHT = 600

# ============================
# INIT
# ============================
pygame.init()
pygame.mixer.init()

# ============================
# SCREEN
# ============================
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Advanced Brick Breaker")
clock = pygame.time.Clock()

font_big = pygame.font.SysFont("arial", 48, bold=True)
font_small = pygame.font.SysFont("arial", 28)

# ============================
# ASSET PATHS (Safe cross-platform)
# ============================
assets_dir = os.path.join(os.getcwd(), "assets")
menu_bg_path = os.path.join(assets_dir, "images", "menu_bg.png")
bg_path = os.path.join(assets_dir, "images", "background.png")
bg_music_path = os.path.join(assets_dir, "sounds", "bg_music.wav")
hit_sound_path = os.path.join(assets_dir, "sounds", "hit.wav")
paddle_sound_path = os.path.join(assets_dir, "sounds", "paddle.wav")
game_over_sound_path = os.path.join(assets_dir, "sounds", "game_over.wav")

# ============================
# SAFE ASSET LOADING
# ============================
def safe_load_image(path, size=None):
    try:
        img = pygame.image.load(path).convert()
        if size: img = pygame.transform.scale(img, size)
        return img
    except:
        return None

def safe_load_sound(path):
    try:
        return pygame.mixer.Sound(path)
    except:
        class DummySound:
            def play(self): pass
        return DummySound()

menu_bg = safe_load_image(menu_bg_path, (WIDTH, HEIGHT))
bg = safe_load_image(bg_path, (WIDTH, HEIGHT))

try:
    if os.path.exists(bg_music_path):
        pygame.mixer.music.load(bg_music_path)
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play(-1)
except:
    print("Music load failed, skipping...")

sounds = {
    "hit": safe_load_sound(hit_sound_path),
    "paddle": safe_load_sound(paddle_sound_path),
    "game_over": safe_load_sound(game_over_sound_path)
}

# ============================
# GAME STATES
# ============================
MENU = "menu"
LEVELS = "levels"
PLAYING = "playing"
GAME_OVER = "game_over"

state = MENU

# ============================
# LOAD SAVE
# ============================
save_data = load_game()
current_level = save_data["current_level"]

# ============================
# OBJECTS
# ============================
menu = MainMenu(screen)
level_screen = LevelSelect(screen, current_level)
game = None  # Initialize only when Play clicked

# ============================
# GAME LOOP
# ============================
running = True
while running:
    clock.tick(60)

    # ----------------------------
    # EVENTS
    # ----------------------------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:

            # ===== MENU =====
            if state == MENU:
                action = menu.handle_click(event.pos)
                if action == "play":
                    game = Game(screen, current_level, sounds)
                    state = PLAYING
                elif action == "levels":
                    state = LEVELS

            # ===== LEVEL SELECT =====
            elif state == LEVELS:
                result = level_screen.handle_click(event.pos)
                if result == "back":
                    state = MENU
                elif isinstance(result, int):
                    current_level = result
                    game = Game(screen, current_level, sounds)
                    state = PLAYING

            # ===== GAME OVER =====
            elif state == GAME_OVER:
                state = MENU

    # ----------------------------
    # DRAW + UPDATE
    # ----------------------------
    if state == MENU:
        menu.draw(menu_bg)

    elif state == LEVELS:
        if bg: screen.blit(bg, (0, 0))
        else: screen.fill((5, 5, 20))
        level_screen.draw()

    elif state == PLAYING:
        # We don't blit "bg" here because Game.draw handles its own futuristic background
        result = game.update()
        game.draw()

        if result == "next_level":
            current_level += 1
            save_game(current_level)
            level_screen.unlocked_level = current_level
            game = Game(screen, current_level, sounds)

        elif result == "game_over":
            state = GAME_OVER

    elif state == GAME_OVER:
        # Futuristic Game Over
        screen.fill((10, 0, 0))
        # Draw some scanlines or grid
        for i in range(0, HEIGHT, 4):
            pygame.draw.line(screen, (20, 0, 0), (0, i), (WIDTH, i))
            
        text = font_big.render("MISSION FAILED", True, (255, 50, 50))
        hint = font_small.render("SYSTEM REBOOT REQUIRED - CLICK TO CONTINUE", True, (150, 150, 150))
        
        # Add a glow to the text
        glow = font_big.render("MISSION FAILED", True, (150, 0, 0))
        screen.blit(glow, (WIDTH//2 - text.get_width()//2 + 2, 242))
        
        screen.blit(text, (WIDTH//2 - text.get_width()//2, 240))
        screen.blit(hint, (WIDTH//2 - hint.get_width()//2, 320))

    # ----------------------------
    # UPDATE DISPLAY
    # ----------------------------
    pygame.display.update()

pygame.quit()
