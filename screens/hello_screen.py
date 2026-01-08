import pygame
from .base_screen import BaseScreen, PIPBOY_BG, PIPBOY_FG

class HelloScreen(BaseScreen):
	def __init__(self, screen):
		super().__init__(screen)
		self.font = pygame.font.SysFont("consolas", 24)
		self.text = self.font.render("HELLO, PIP-BOY", True, PIPBOY_FG)

	def render(self):
		self.screen.fill(PIPBOY_BG)
		rect = self.text.get_rect(center=self.screen.get_rect().center)
		self.screen.blit(self.text, rect)

