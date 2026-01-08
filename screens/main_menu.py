import pygame
from .base_screen import BaseScreen
from .glow_text import glow_text, glow_title
from .fonts import load_font
from .colors import Palette
from .ui_frame import draw_frame, draw_hline, draw_corner

MENU_ITEMS = ["STATS", "ITEMS", "DATA"]

class MainMenu(BaseScreen):
	def __init__(self, screen, manager):
		super().__init__(screen)
		self.manager = manager
		self.font = load_font(28)
		self.selected = 0

	def handle_event(self, event):
		# Keyboard navigation
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_UP:
				self.selected = (self.selected - 1) % len(MENU_ITEMS)
			elif event.key == pygame.K_DOWN:
				self.selected = (self.selected + 1) % len(MENU_ITEMS)
			elif event.key == pygame.K_RETURN:
				choice = MENU_ITEMS[self.selected].lower()
				self.manager.set(choice)

		# Touch / mouse navigation
		if event.type == pygame.MOUSEBUTTONDOWN:
			x, y = event.pos
			w, h = self.screen.get_size()

			for i, label in enumerate(MENU_ITEMS):
				item_y = 120 + i * 60
				if abs(y - item_y) < 30:
					self.selected = i
					choice = MENU_ITEMS[i].lower()
					self.manager.set(choice)

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


		for i, label in enumerate(MENU_ITEMS):
			color = Palette.FG if i == self.selected else (0, 150, 60)
			text = glow_text(label, self.font)
			rect = text.get_rect(center=(w // 2, 120 + i * 60))
			self.screen.blit(text, rect)

