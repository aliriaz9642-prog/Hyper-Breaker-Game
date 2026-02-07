import pygame

class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.font_title = pygame.font.SysFont("Outfit", 64, bold=True)
        self.font_btn = pygame.font.SysFont("Outfit", 32)

        self.play_rect = pygame.Rect(300, 300, 200, 55)
        self.level_rect = pygame.Rect(300, 380, 200, 55)
        self.mouse_pos = (0,0)

    def draw(self, bg=None):
        self.mouse_pos = pygame.mouse.get_pos()
        
        if bg:
            self.screen.blit(bg, (0, 0))
        else:
            self.screen.fill((5, 5, 20))

        # Title Glow
        title_text = "HYPER BREAKER"
        title = self.font_title.render(title_text, True, (0, 255, 255))
        self.screen.blit(title, (400 - title.get_width()//2, 120))
        
        # Draw Buttons
        self.draw_button(self.play_rect, "START MISSION", (0, 255, 255))
        self.draw_button(self.level_rect, "SELECT SECTOR", (255, 0, 255))

    def draw_button(self, rect, text, color):
        is_hover = rect.collidepoint(self.mouse_pos)
        current_color = color if is_hover else (100, 100, 100)
        
        # Button Glow if hover
        if is_hover:
            glow_rect = rect.inflate(10, 10)
            s = pygame.Surface((glow_rect.width, glow_rect.height), pygame.SRCALPHA)
            pygame.draw.rect(s, (*color, 60), (0, 0, glow_rect.width, glow_rect.height), border_radius=15)
            self.screen.blit(s, glow_rect.topleft)

        pygame.draw.rect(self.screen, (20, 20, 40), rect, border_radius=12)
        pygame.draw.rect(self.screen, current_color, rect, 2, border_radius=12)
        
        btn_txt = self.font_btn.render(text, True, (255, 255, 255) if is_hover else (180, 180, 180))
        self.screen.blit(btn_txt, (rect.centerx - btn_txt.get_width()//2, rect.centery - btn_txt.get_height()//2))

    def handle_click(self, pos):
        if self.play_rect.collidepoint(pos):
            return "play"
        if self.level_rect.collidepoint(pos):
            return "levels"
        return None
