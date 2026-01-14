# screens/helpers/ui_manager.py
import pygame
import math
import time

from .colors import Palette
from .fonts import load_font
from .glow_text import glow_text
from .touch import TouchArea
from .crt import create_scanlines
from .noise import create_noise_surface

SUBCATEGORIES_FALLBACK = {
    "STAT": ["STATUS", "SPECIAL", "SKILLS", "PERKS"],
    "INV":  ["AID", "AMMO", "WEAPONS", "APPAREL", "MISC"],
    "DATA": ["QUESTS", "LOGS", "NOTES"],
    "MAP":  ["LOCAL", "WORLD"],
    "RADIO":["CHANNELS", "SIGNALS"]
}

class UIManager:
    """
    UIManager draws topbar, subbar, CRT effects and wires TouchAreas to ModuleManager.
    It expects a ModuleManager instance (module_manager) that exposes:
      - get_modules() -> list of labels
      - get_active_label() -> current label
      - get_active_module() -> module instance (legacy BaseModule)
      - set_active(label)
    """
    def __init__(self, screen, module_manager, get_sub_selected=None, set_sub_selected=None,
                 scanline_params=None, noise_params=None):
        self.screen = screen
        self.module_manager = module_manager
        self.get_sub_selected = get_sub_selected or (lambda: None)
        self.set_sub_selected = set_sub_selected or (lambda v: None)

        self.font_top = load_font(22)
        self.font_sub = load_font(18)

        self.topbar_touch = []
        self.subbar_touch = []

        # flicker state
        self.flicker_time = 0.0
        self.flicker_speed = 0.8
        self.flicker_max_alpha = 14

        # create scanlines/noise
        w, h = screen.get_size()
        try:
            self.scanlines = create_scanlines(w, h)
        except Exception:
            self.scanlines = pygame.Surface((w, h), pygame.SRCALPHA)
        try:
            self.noise = create_noise_surface(w, h, intensity=100)
        except Exception:
            self.noise = pygame.Surface((w, h), pygame.SRCALPHA)

    # Topbar: create touch areas and draw
    def render_topbar(self):
        self.topbar_touch.clear()
        categories = self.module_manager.get_modules()
        if not categories:
            categories = ["STAT", "INV", "DATA", "MAP", "RADIO"]
        x = 18
        y = 12
        selected = self.module_manager.get_active_label()
        for cat in categories:
            label = cat.upper()
            surf = glow_text(label, self.font_top)
            rect = surf.get_rect(topleft=(x, y))
            color = Palette.FG if label == selected else (60, 140, 60)
            self.screen.blit(surf, rect)
            if label == selected:
                pygame.draw.rect(self.screen, color, rect.inflate(12, 10), 2)
            # create touch area; capture cat in default arg
            ta_rect = rect.inflate(10, 10)
            self.topbar_touch.append(TouchArea(ta_rect, lambda c=label: self._on_topbar_tap(c)))
            x += rect.width + 28
        pygame.draw.line(self.screen, Palette.FG, (10, 56), (self.screen.get_width() - 10, 56), 2)

    def _on_topbar_tap(self, label):
        # set active module via module_manager
        try:
            self.module_manager.set_active(label)
            # reset sub selection if module exposes footer
            active = self.module_manager.get_active_module()
            if active and hasattr(active, "footer"):
                # set default sub to footer.selected if present
                try:
                    default = active.footer.selected
                    self.set_sub_selected(default)
                except Exception:
                    self.set_sub_selected(None)
        except Exception:
            pass

    # Subbar: query active module for sublabels (legacy BaseModule.footer.menu)
    def render_subbar(self):
        self.subbar_touch.clear()
        active = self.module_manager.get_active_module()
        if active and hasattr(active, "footer") and getattr(active.footer, "menu", None):
            items = active.footer.menu
        else:
            # fallback to static mapping
            active_label = self.module_manager.get_active_label() or "STAT"
            items = SUBCATEGORIES_FALLBACK.get(active_label, [])
        sel = self.get_sub_selected()
        x = 18
        y = 64
        for it in items:
            surf = glow_text(it, self.font_sub)
            rect = surf.get_rect(topleft=(x, y))
            if it != sel:
                faded = pygame.Surface(surf.get_size(), pygame.SRCALPHA)
                faded.fill((0, 0, 0, 120))
                surf.blit(faded, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)
            self.screen.blit(surf, rect)
            if it == sel:
                pygame.draw.rect(self.screen, Palette.FG, rect.inflate(8, 8), 1)
            # create touch area that activates the submodule on the active module
            ta_rect = rect.inflate(8, 8)
            self.subbar_touch.append(TouchArea(ta_rect, lambda s=it: self._on_subbar_tap(s)))
            x += rect.width + 18

    def _on_subbar_tap(self, sublabel):
        # set sub selection and ask active module to switch submodule
        self.set_sub_selected(sublabel)
        active = self.module_manager.get_active_module()
        if active:
            # legacy BaseModule.switch_submodule expects index; find index in footer.menu
            try:
                if hasattr(active, "footer") and getattr(active.footer, "menu", None):
                    idx = active.footer.menu.index(sublabel)
                    active.switch_submodule(idx)
                else:
                    # fallback: try to call activate by name if present
                    if hasattr(active, "activate"):
                        active.activate(sublabel)
            except Exception:
                pass

    def render_flicker(self, dt):
        self.flicker_time += dt * self.flicker_speed
        strength = (math.sin(self.flicker_time) + 1) * 0.5
        alpha = int(strength * self.flicker_max_alpha)
        if alpha <= 0:
            return
        flicker = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        flicker.fill((80, 255, 80, alpha))
        self.screen.blit(flicker, (0, 0))

    def render_scanlines_and_noise(self):
        if self.scanlines:
            self.screen.blit(self.scanlines, (0, 0))
        if self.noise:
            self.screen.blit(self.noise, (0, 0))

    def render(self, dt):
        # draw top/sub bars and CRT effects
        self.render_topbar()
        self.render_subbar()
        self.render_flicker(dt)
        self.render_scanlines_and_noise()
        # update pulses for touch areas
        for ta in self.topbar_touch + self.subbar_touch:
            try:
                ta.update(dt)
            except Exception:
                pass

    def handle_event(self, event):
        # route events to touch areas first
        for ta in self.topbar_touch + self.subbar_touch:
            try:
                ta.handle_event(event)
            except Exception:
                pass

