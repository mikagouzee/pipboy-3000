import pygame
from .base_screen import BaseScreen
from .helpers.fonts import load_font
from .helpers.colors import Palette
from .helpers.glow_text import glow_text, glow_title
from .helpers.ui_frame import draw_frame, draw_hline, draw_corner


class RadioScreen(BaseScreen):
	def __init__(self, screen, manager):
		super().__init__(screen)
		self.manager = manager
		self.font = load_font(24)

		pygame.mixer.init()
		pygame.mixer.music.load("assets/radio.mp3")

	def handle_event(self, event):
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				self.manager.set("data")
			if event.key == pygame.K_RETURN:
				if pygame.mixer.music.get_busy():
					pygame.mixer.music.stop()
				else:
					pygame.mixer.music.play()

		if event.type == pygame.MOUSEBUTTONDOWN:
			if pygame.mixer.music.get_busy():
				pygame.mixer.music.stop()
			else:
				pygame.mixer.music.play()

	def render(self):
		self.screen.fill(Palette.BG)
		w, h = self.screen.get_size()
		draw_frame(self.screen, (10, 10, w - 20, h - 20))
		draw_hline(self.screen, 20, 60, w - 40)

		text = "PLAYING" if pygame.mixer.music.get_busy() else "STOPPED"
		label = glow_text(f"RADIO: {text}", self.font)
		self.screen.blit(label, (20, 40))

