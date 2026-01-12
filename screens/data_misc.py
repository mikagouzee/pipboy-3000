import pygame, random, json
from .base_screen import BaseScreen
from .helpers.fonts import load_font
from .helpers.glow_text import glow_text, glow_title
from .helpers.colors import Palette
from .helpers.ui_frame import draw_frame, draw_hline, draw_corner
from .helpers.touch import TouchArea

class MiscScreen(BaseScreen):
	def __init__(self, screen, manager):
		super().__init__(screen)
		self.manager = manager
		self.font = load_font(20)
		with open("data/trivia.json") as f:
			self.trivia = json.load(f)

		self.current = random.choice(self.trivia)

		w, h = screen.get_size()

		back_rect = pygame.Rect(10, 10, 120, 50)
		self.back_button = TouchArea(back_rect, self.go_back, padding=10)

		full_rect = pygame.Rect(0, 0,  w, h)
		self.trivia_button = TouchArea(full_rect, self.new_trivia, padding=0)

	def go_back(self):
		self.manager.set("data")

	def new_trivia(self):
		self.current = random.choice(self.trivia)

	def handle_event(self, event):
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_BACKSPACE:
				self.go_back()
			if event.key == pygame.K_RETURN:
				self.new_trivia()

		self.back_button.handle_event(event)
		self.trivia_button.handle_event(event)

	def render(self):
		self.screen.fill(Palette.BG)
		lines = self.wrap_text(self.current, 40)
		w, h = self.screen.get_size()
		y = 40

		backtext = glow_text("< BACK", self.font)
		self.screen.blit(backtext, (20,20))

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

