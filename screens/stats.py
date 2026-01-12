import pygame
from .base_screen import BaseScreen
from .helpers.glow_text import glow_text, glow_title
from .helpers.fonts import load_font
from .helpers.ui_frame import draw_frame, draw_hline, draw_corner
from .helpers.colors import Palette

class StatsScreen(BaseScreen):
	def __init__(self, screen, manager):
		super().__init__(screen)
		self.manager = manager
		self.font_title = load_font(28)
		self.font_text = load_font(20)

		self.stats = [
			("STRENGTH", "5"),
			("PERCEPTION", "6"),
			("ENDURANCE", "4"),
			("CHARISMA", "7"),
			("INTELLIGENCE", "8"),
			("AGILITY", "5"),
			("LUCK", "3")
		]

	def handle_event(self, event):
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				self.manager.set("menu")

		if event.type == pygame.MOUSEBUTTONDOWN:
			self.manager.set("menu")

	def render(self):
		self.screen.fill(Palette.BG)
		w, h = self.screen.get_size()
		draw_frame(self.screen, (10, 10, w - 20, h - 20))
		draw_hline(self.screen, 20, 60, w - 40)

		# Title
		title = glow_title("STATS", self.font_title)
		self.screen.blit(title, (20, 20))

		# Stats list
		y = 80
		for label, value in self.stats:
			text = glow_text(f"{label}: {value}", self.font_text)
			self.screen.blit(text, (40, y))
			y += 30

