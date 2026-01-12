import pygame, random, json
from .base_screen import BaseScreen
from .helpers.fonts import load_font
from .helpers.glow_text import glow_text, glow_title
from .helpers.colors import Palette
from .helpers.ui_frame import draw_frame, draw_hline, draw_corner

class MiscScreen(BaseScreen):
	def __init__(self, screen, manager):
		super().__init__(screen)
		self.manager = manager
		self.font = load_font(20)
		with open("data/trivia.json") as f:
			self.trivia = json.load(f)

		self.current = random.choice(self.trivia)

	def handle_event(self, event):
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				self.manager.set("data")
			if event.key == pygame.K_RETURN:
				self.current = random.choice(self.trivia)

		if event.type == pygame.MOUSEBUTTONDOWN:
			self.current = random.choice(self.trivia)

	def render(self):
		self.screen.fill(Palette.BG)
		lines = self.wrap_text(self.current, 40)
		w, h = self.screen.get_size()
		y = 40

		draw_frame(self.screen, (10, 10, w - 20, h - 20))
		draw_hline(self.screen, 20, 60, w - 40)

		for line in lines:
			text = glow_text(line, self.font)
			self.screen.blit(text, (20, y))
			y += 30

	def wrap_text(self, text, width):
		words = text.split()
		lines = []
		line = ""
		for w in words:
			if len(line) + len(w) + 1 > width:
				lines.append(line)
				line = w
			else:
				line += " " + w if line else w
		if line:
			lines.append(line)
		return lines

