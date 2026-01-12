import pygame
from .base_screen import BaseScreen
from .helpers.fonts import load_font
from .helpers.glow_text import glow_text, glow_title
from .helpers.colors import Palette
from .helpers.ui_frame import draw_frame, draw_hline, draw_corner

from .helpers.touch import TouchArea

DATA_CATEGORIES = ["MAP", "MISC", "QUESTS", "RADIO"]

class DataMenu(BaseScreen):
	def __init__(self, screen, manager):
		super().__init__(screen)
		self.manager = manager
		self.font = load_font(26)
		self.selected = 0

		self.buttons = []
		y = 120

		for label in DATA_CATEGORIES:
			rect = pygame.Rect(0, 0, 260, 40)
			rect.center = (screen.get_width() // 2, y)

			self.buttons.append(
				TouchArea(rect, lambda l=label: self._select(l), padding=20)
			)

			y += 50

	def _select(self, label):
		self.selected = DATA_CATEGORIES.index(label)
		self.open_selected()

	def handle_event(self, event):
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_UP:
				self.selected = (self.selected - 1) % len(DATA_CATEGORIES)
			elif event.key == pygame.K_DOWN:
				self.selected = (self.selected + 1) % len(DATA_CATEGORIES)
			elif event.key == pygame.K_BACKSPACE:
				self.manager.set("menu")
			elif event.key == pygame.K_RETURN:
				self.open_selected()

		for btn in self.buttons:
			btn.handle_event(event)


	def open_selected(self):
		name = DATA_CATEGORIES[self.selected].lower()
		self.manager.set(f"data_{name}")

	def render(self):
		self.screen.fill(Palette.BG)
		w, h = self.screen.get_size()

		draw_frame(self.screen, (10, 10, w - 20, h - 20))
		draw_hline(self.screen, 20, 60, w - 40)

		title = glow_title("DATA", self.font)
		self.screen.blit(title, (20, 20))

		for i, label in enumerate(DATA_CATEGORIES):
			color = Palette.FG if i == self.selected else (0, 150, 60)
			text = glow_text(label, self.font)
			rect = text.get_rect(center=(w // 2, 120 + i * 50))
			self.screen.blit(text, rect)

