import pygame
from ..helpers.fonts import load_font
from ..helpers.glow_text import glow_text
from ..helpers.colors import Palette

SUBCATEGORIES = {
    "STAT": ["STATUS", "SPECIAL", "SKILLS", "PERKS"],
    "INV":  ["AID", "AMMO", "WEAPONS", "APPAREL", "MISC"],
    "DATA": ["QUESTS", "LOGS", "NOTES"],
    "MAP":  ["LOCAL", "WORLD"],
    "RADIO":["CHANNELS", "SIGNALS"]
}

class TopBar:
    def __init__(self, screen, categories, get_selected):
        self.screen = screen
        self.categories = categories
        self.get_selected = get_selected
        self.font = load_font(22)

    def render(self):
        w, _ = self.screen.get_size()
        x = 18
        y = 12
        selected = self.get_selected()

        for cat in self.categories:
            is_sel = (cat == selected)
            text_surf = glow_text(cat, self.font) if is_sel else glow_text(cat, self.font)
            rect = text_surf.get_rect(topleft=(x, y))
            color = Palette.FG if is_sel else (60, 140, 60)
            # draw text (glow_text already returns a surface with glow)
            self.screen.blit(text_surf, rect)
            # box selected tab
            if is_sel:
                pygame.draw.rect(self.screen, color, rect.inflate(12, 10), 2)
            x += rect.width + 28

        # underline across top area
        pygame.draw.line(self.screen, Palette.FG, (10, 56), (w - 10, 56), 2)

class SubBar:
    def __init__(self, screen, get_main_selected, get_sub_selected, set_sub_selected):
        self.screen = screen
        self.get_main_selected = get_main_selected
        self.get_sub_selected = get_sub_selected
        self.set_sub_selected = set_sub_selected
        self.font = load_font(18)

    def items_for_main(self, main):
        return SUBCATEGORIES.get(main, [])

    def render(self):
        main = self.get_main_selected()
        items = self.items_for_main(main)
        sel = self.get_sub_selected()

        x = 18
        y = 64
        for it in items:
            is_sel = (it == sel)
            surf = glow_text(it, self.font) if is_sel else glow_text(it, self.font)
            rect = surf.get_rect(topleft=(x, y))
            # faded for non-selected
            if not is_sel:
                faded = pygame.Surface(surf.get_size(), pygame.SRCALPHA)
                faded.fill((0, 0, 0, 120))
                surf.blit(faded, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)
            self.screen.blit(surf, rect)
            # subtle box for selected subtab
            if is_sel:
                pygame.draw.rect(self.screen, Palette.FG, rect.inflate(8, 8), 1)
            x += rect.width + 18

