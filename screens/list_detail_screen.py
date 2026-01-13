import pygame
from .base_screen import BaseScreen
from ..helpers.colors import Palette
from ..helpers.fonts import load_font
from ..helpers.glow_text import glow_text
from ..helpers.touch import TouchArea

class ListDetailScreen(BaseScreen):
    def __init__(self, screen, manager, title, items, subkey=None, on_select=None):
        super().__init__(screen)
        self.manager = manager
        self.title = title
        self.items = items  # list of dicts: {id,label,image,lines}
        self.selected_index = 0
        self.on_select = on_select
        self.font_title = load_font(26)
        self.font_item = load_font(18)
        self.font_detail = load_font(16)
        self.touch_areas = []
        self._rebuild_touch_areas()

    def _rebuild_touch_areas(self):
        self.touch_areas.clear()
        w, h = self.screen.get_size()
        x = 20
        y = 100
        for i, it in enumerate(self.items):
            rect = pygame.Rect(x, y, w//2 - 40, 28)
            self.touch_areas.append(TouchArea(rect, lambda idx=i: self._tap_index(idx), padding=6))
            y += 30

    def _tap_index(self, idx):
        self.selected_index = idx
        if self.on_select:
            self.on_select(self.items[idx])

    def handle_event(self, event):
        for ta in self.touch_areas:
            ta.handle_event(event)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_index = max(0, self.selected_index - 1)
            elif event.key == pygame.K_DOWN:
                self.selected_index = min(len(self.items) - 1, self.selected_index + 1)
            elif event.key == pygame.K_RETURN:
                if self.on_select:
                    self.on_select(self.items[self.selected_index])

    def update(self, dt):
        for ta in self.touch_areas:
            ta.update(dt)

    def render(self):
        self.screen.fill(Palette.BG)
        w, h = self.screen.get_size()
        # title
        title_s = glow_text(self.title, self.font_title)
        self.screen.blit(title_s, (20, 20))
        # left list
        x = 20
        y = 100
        for i, it in enumerate(self.items):
            is_sel = (i == self.selected_index)
            surf = glow_text(it["label"], self.font_item)
            rect = surf.get_rect(topleft=(x, y))
            if not is_sel:
                faded = pygame.Surface(surf.get_size(), pygame.SRCALPHA)
                faded.fill((0, 0, 0, 120))
                surf.blit(faded, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)
            self.screen.blit(surf, rect)
            if is_sel:
                pygame.draw.rect(self.screen, Palette.FG, rect.inflate(6, 6), 1)
            y += 30
        # right panel
        right_x = w // 2 + 10
        right_y = 100
        sel = self.items[self.selected_index]
        if sel.get("image"):
            try:
                img = pygame.image.load(sel["image"]).convert_alpha()
                img = pygame.transform.smoothscale(img, (w//2 - 40, h//3))
                self.screen.blit(img, (right_x, right_y))
                right_y += img.get_height() + 8
            except Exception:
                pass
        for line in sel.get("lines", []):
            txt = glow_text(line, self.font_detail)
            self.screen.blit(txt, (right_x, right_y))
            right_y += 22

