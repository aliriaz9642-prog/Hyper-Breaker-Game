import pygame

class LevelSelect:
    def __init__(self, screen, unlocked_level):
        self.screen = screen
        self.font = pygame.font.SysFont("Outfit", 24)
        self.big_font = pygame.font.SysFont("Outfit", 48, bold=True)
        self.unlocked_level = unlocked_level
        self.buttons = []
        self.create_buttons()
        self.back_rect = pygame.Rect(20, 20, 100, 45)
        self.mouse_pos = (0,0)

    def create_buttons(self):
        self.buttons.clear()
        size = 60
        gap = 12
        cols = 8
        rows = 4
        x_start = (800 - (cols * (size + gap))) // 2
        y_start = 140
        
        level = 1
        for row in range(rows):
            for col in range(cols):
                rect = pygame.Rect(x_start + col * (size + gap), y_start + row * (size + gap), size, size)
                self.buttons.append((level, rect))
                level += 1

    def draw(self):
        self.mouse_pos = pygame.mouse.get_pos()
        self.screen.fill((5, 5, 20))
        
        title = self.big_font.render("MISSION SECTORS", True, (0, 255, 255))
        self.screen.blit(title, (400 - title.get_width()//2, 50))

        for level, rect in self.buttons:
            is_unlocked = level <= self.unlocked_level
            hover = rect.collidepoint(self.mouse_pos) and is_unlocked
            
            color = (0, 255, 255) if is_unlocked else (60, 60, 60)
            bg_color = (20, 40, 60) if is_unlocked else (30, 30, 30)
            
            if hover:
                glow_rect = rect.inflate(8, 8)
                s = pygame.Surface((glow_rect.width, glow_rect.height), pygame.SRCALPHA)
                pygame.draw.rect(s, (*color, 60), (0, 0, glow_rect.width, glow_rect.height), border_radius=10)
                self.screen.blit(s, glow_rect.topleft)

            pygame.draw.rect(self.screen, bg_color, rect, border_radius=10)
            pygame.draw.rect(self.screen, color if is_unlocked else (40, 40, 40), rect, 2, border_radius=10)
            
            label = str(level) if is_unlocked else "LOCKED"
            txt_color = (255, 255, 255) if is_unlocked else (100, 100, 100)
            text = self.font.render(label, True, txt_color)
            text_rect = text.get_rect(center=rect.center)
            self.screen.blit(text, text_rect)

        # Back Button
        back_hover = self.back_rect.collidepoint(self.mouse_pos)
        pygame.draw.rect(self.screen, (20, 20, 40), self.back_rect, border_radius=10)
        pygame.draw.rect(self.screen, (255, 0, 255) if back_hover else (150, 0, 150), self.back_rect, 2, border_radius=10)
        back_txt = self.font.render("EXIT", True, (255, 255, 255))
        self.screen.blit(back_txt, (self.back_rect.centerx - back_txt.get_width()//2, self.back_rect.centery - back_txt.get_height()//2))

    def handle_click(self, pos):
        if self.back_rect.collidepoint(pos):
            return "back"

        for level, rect in self.buttons:
            if rect.collidepoint(pos) and level <= self.unlocked_level:
                return level

        return None
