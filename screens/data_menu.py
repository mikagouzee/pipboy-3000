import pygame
from .base_screen import BaseScreen, PIPBOY_BG, PIPBOY_FG
from .fonts import load_font
from .glow_text import glow_text, glow_title
from .colors import Palette
from .ui_frame import draw_frame, draw_hline, draw_corner

DATA_CATEGORIES = ["MAP", "MISC", "QUESTS", "RADIO"]

class DataMenu(BaseScreen):
	def __init__(self, screen, manager):
		super().__init__(screen)
		self.manager = manager
		self.font = load_font(26)
		self.selected = 0

	def handle_event(self, event):
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_UP:
				self.selected = (self.selected - 1) % len(DATA_CATEGORIES)
			elif event.key == pygame.K_DOWN:
				self.selected = (self.selected + 1) % len(DATA_CATEGORIES)
			elif event.key == pygame.K_ESCAPE:
				self.manager.set("menu")
			elif event.key == pygame.K_RETURN:
				self.open_selected()

		if event.type == pygame.MOUSEBUTTONDOWN:
			x, y = event.pos
			for i, label in enumerate(DATA_CATEGORIES):
				item_y = 120 + i * 50
				if abs(y - item_y) < 25:
					self.selected = i
					self.open_selected()

	def open_selected(self):
		name = DATA_CATEGORIES[self.selected].lower()
		self.manager.set(f"data_{name}")

	def render(self):
		self.screen.fill(PipboyPalette.BG)
		w, h = self.screen.get_size()

		draw_frame(self.screen, (10, 10, w - 20, h - 20))
		draw_hline(self.screen, 20, 60, w - 40)

		title = glow_title("DATA", self.font)
		self.screen.blit(title, (20, 20))

		for i, label in enumerate(DATA_CATEGORIES):
			color = PIPBOY_FG if i == self.selected else (0, 150, 60)
			text = glow_text(label, self.font)
			rect = text.get_rect(center=(w // 2, 120 + i * 50))
			self.screen.blit(text, rect)

