import pygame
from .base_screen import BaseScreen
from .helpers.ui_frame import draw_frame, draw_hline, draw_corner
from .helpers.colors import Palette

from .helpers.touch import TouchArea

class MapScreen(BaseScreen):
	def __init__(self, screen, manager):
		super().__init__(screen)
		self.manager = manager

		# Load map image
		self.map_img = pygame.image.load("assets/map.png").convert()

		full_rect = pygame.Rect(0, 0, screen.get_width(), screen.get_height())
		self.back_button = TouchArea(full_rect, self.go_back, padding=0)

	def go_back(self):
		self.manager.set("data")

	def handle_event(self, event):
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_BACKSPACE:
				self.go_back()

		self.back_button.handle_event(event)

	def render(self):
		self.screen.fill(Palette.BG)
		w, h = self.screen.get_size()
		draw_frame(self.screen, (10, 10, w - 20, h - 20))
		draw_hline(self.screen, 20, 60, w - 40)
		scaled = pygame.transform.smoothscale(self.map_img, self.screen.get_size())
		self.screen.blit(scaled, (0,0))
