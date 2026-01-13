import pygame
import math
import time

from ..helpers.colors import Palette
from ..helpers.fonts import load_font
from ..helpers.glow_text import glow_text

from ..helpers.crt import create_scanlines
from ..helpers.noise import create_noise_surface
from ..helpers.touch import TouchArea


SUBCATEGORIES = {
	"STAT": ["STATUS", "SPECIAL", "SKILLS", "PERKS"],
	"INV":  ["AID", "AMMO", "WEAPONS", "APPAREL", "MISC"],
	"DATA": ["QUESTS", "LOGS", "NOTES"],
	"MAP":  ["LOCAL", "WORLD"],
	"RADIO":["CHANNELS", "SIGNALS"]
}

class UIManager:
	def __init__(self, screen, get_main_selected, get_sub_selected, set_sub_selected, scanline_params=None, noise_params=None):
		self.screen = screen
		self.get_main_selected = get_main_selected
		self.get_sub_selected = get_sub_selected
		self.set_sub_selected = set_sub_selected

		self.font_top = load_font(22)
		self.font_sub = load_font(18)

		self.flicker_time = 0.0
		self.flicker_speed = 0.8
		self.flicker_max_alpha = 14

		w, h = screen.get_size()
		sl_params = scanline_params or {"width": w, "height": h, "gap": 3, "speed": 1, "colours": [(0,13,3,50)]}
		noise_params = noise_params or {"width": w, "height": h, "intensity":100}

		self.topbar_touch = []

		try:
				self.scanlines = create_scanlines(sl_params["width"], sl_params["height"])
		except Exception:
				self.scanlines = pygame.Surface((w,h), pygame.SRCALPHA)

		try:
				self.noise = create_noise_surface(noise_params["width"], noise_params["height"], intensity=noise_params["intensity"])
		except Exception:
				self.noise = pygame.Surface((w, h), pygame.SRCALPHA)


	def set_main(self, cat):
		self.set_main_selected(cat)
		self.set_sub_selected(None)

	# Top bar is global and fixed
	def render_topbar(self):
		w, _ = self.screen.get_size()
		categories = ["STAT", "INV", "DATA", "MAP", "RADIO"]
		x = 18
		y = 12
		main = self.get_main_selected() or "STAT"
		selected = self.get_main_selected()

		for cat in categories:
			surf = glow_text(cat, self.font_top)
			rect = surf.get_rect(topleft=(x, y))
			color = Palette.FG if cat == selected else (60, 140, 60)
			self.screen.blit(surf, rect)
			if cat == selected:
				pygame.draw.rect(self.screen, color, rect.inflate(12, 10), 2)
			self.topbar_touch.append(TouchArea(rect.inflate(10,10), lambda c=cat:self.set_main(c)))
			x += rect.width + 28
		pygame.draw.line(self.screen, Palette.FG, (10, 56), (w - 10, 56), 2)

	# Subbar derived from main selection
	def render_subbar(self):
		main = self.get_main_selected() or "STAT"
		items = SUBCATEGORIES.get(main, [])
		sel = self.get_sub_selected()
		x = 18
		y = 64
		for it in items:
			is_sel = (it == sel)
			surf = glow_text(it, self.font_sub)
			rect = surf.get_rect(topleft=(x, y))
			if not is_sel:
				faded = pygame.Surface(surf.get_size(), pygame.SRCALPHA)
				faded.fill((0, 0, 0, 120))
				surf.blit(faded, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)
			self.screen.blit(surf, rect)
			if is_sel:
				pygame.draw.rect(self.screen, Palette.FG, rect.inflate(8, 8), 1)
			x += rect.width + 18

	# CRT flicker overlay applied last
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
				self.screen.blit(self.scanlines, (0,0))
		if self.noise:
				self.screen.blit(self.noise, (0,0))

	# Public render called from main loop after screen render
	def render(self, dt):
		self.render_topbar()
		self.render_subbar()
		self.render_flicker(dt)
		self.render_scanlines_and_noise()

	# Optional: handle global keys for top/sub switching
	def handle_event(self, event):
		if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_TAB:
						main = self.get_main_selected() or "STAT"
						items = SUBCATEGORIES.get(main, [])
						if items:
								cur = self.get_sub_selected()
								try:
										idx = items.index(cur)
										idx = (idx+1) % len(items)
								except ValueError:
										idx = 0
								self.set_sub_selected(items[idx])
