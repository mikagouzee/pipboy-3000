import pygame
from .base_screen import BaseScreen
from .helpers.glow_text import glow_text, glow_title
from .helpers.fonts import load_font
from .helpers.colors import Palette
from .helpers.ui_frame import draw_frame, draw_hline, draw_corner
from .helpers.touch import TouchArea   # <-- NEW

MENU_ITEMS = ["STATS", "ITEMS", "DATA"]

class MainMenu(BaseScreen):
    def __init__(self, screen, manager):
        super().__init__(screen)
        self.manager = manager
        self.font = load_font(28)
        self.selected = 0

        # --- NEW: create touch areas for each menu item ---
        self.buttons = []
        y = 120

        for label in MENU_ITEMS:
            # A rectangle centered horizontally, matching your text layout
            rect = pygame.Rect(0, 0, 240, 40)
            rect.center = (screen.get_width() // 2, y)

            # Create a touch area with padding and callback
            self.buttons.append(
                TouchArea(rect, lambda l=label: self._select(l), padding=20)
            )

            y += 60

    # --- NEW: callback for touch areas ---
    def _select(self, label):
        self.selected = MENU_ITEMS.index(label)
        self.manager.set(label.lower())

    def handle_event(self, event):
        # Keyboard navigation (unchanged)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected = (self.selected - 1) % len(MENU_ITEMS)
            elif event.key == pygame.K_DOWN:
                self.selected = (self.selected + 1) % len(MENU_ITEMS)
            elif event.key == pygame.K_RETURN:
                choice = MENU_ITEMS[self.selected].lower()
                self.manager.set(choice)

        # Touch handling now delegated to TouchArea objects
        for btn in self.buttons:
            btn.handle_event(event)

    def render(self):
        self.screen.fill(Palette.BG)
        w, h = self.screen.get_size()

        # Outer frame
        draw_frame(self.screen, (10, 10, w - 20, h - 20), thickness=2)

        # Title underline
        draw_hline(self.screen, 20, 60, w - 40, thickness=2)

        # Decorative corners
        draw_corner(self.screen, 10, 10)
        draw_corner(self.screen, w - 20, 10)
        draw_corner(self.screen, 10, h - 20)
        draw_corner(self.screen, w - 20, h - 20)

        # Draw menu items
        for i, label in enumerate(MENU_ITEMS):
            color = Palette.FG if i == self.selected else (0, 150, 60)
            text = glow_text(label, self.font)
            rect = text.get_rect(center=(w // 2, 120 + i * 60))
            self.screen.blit(text, rect)

