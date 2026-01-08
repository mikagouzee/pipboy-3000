import pygame
from .base_screen import BaseScreen, PIPBOY_BG
from .ui_frame import draw_frame, draw_hline, draw_corner

class MapScreen(BaseScreen):
	def __init__(self, screen, manager):
		super().__init__(screen)
		self.manager = manager

		# Load map image
		self.map_img = pygame.image.load("assets/map.png").convert()

	def handle_event(self, event):
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				self.manager.set("data")
		if event.type == pygame.MOUSEBUTTONDOWN:
			self.manager.set("data")

	def render(self):
		self.screen.fill(PIPBOY_BG)
		w, h = self.screen.get_size()
		draw_frame(self.screen, (10, 10, w - 20, h - 20))
		draw_hline(self.screen, 20, 60, w - 40)

		self.screen.blit(self.map_img, (0, 0))
