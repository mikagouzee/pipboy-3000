import pygame
from .base_screen import BaseScreen
from .helpers.fonts import load_font
from .helpers.colors import Palette
from .helpers.glow_text import glow_text, glow_title
from .helpers.ui_frame import draw_frame, draw_hline, draw_corner

from .helpers.touch import TouchArea

class ListScreen(BaseScreen):
	def __init__(self, screen, manager, title, items):
		super().__init__(screen)
		self.manager = manager
		self.title = title
		self.items = items

		self.font_title = load_font(28)
		self.font_text = load_font(20)

		full_rect = pygame.Rect(0, 0, screen.get_width(), screen.get_height())
		self.back_button = TouchArea(full_rect, lambda: self.manager.set("items"), padding=0)


	def handle_event(self, event):
		self.back_button.handle_event(event)

	def render(self):
		self.screen.fill(Palette.BG)
		w, h = self.screen.get_size()
		draw_frame(self.screen, (10, 10, w - 20, h - 20))
		draw_hline(self.screen, 20, 60, w - 40)

		# Title
		title = glow_title(self.title, self.font_title)
		self.screen.blit(title, (20, 20))

		# Items
		y = 80
		for item in self.items:
			text = glow_text(item, self.font_text)
			self.screen.blit(text, (40, y))
			y += 30

