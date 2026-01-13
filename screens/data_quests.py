import pygame, json
from .base_screen import BaseScreen
from .helpers.fonts import load_font
from .helpers.colors import Palette
from .helpers.glow_text import glow_text, glow_title
from .helpers.ui_frame import draw_frame, draw_hline, draw_corner
from .helpers.touch import TouchArea

class QuestsScreen(BaseScreen):
	def __init__(self, screen, manager):
		super().__init__(screen)
		self.manager = manager
		self.font = load_font(20)
		
		back_rect = pygame.Rect(10,10,120,50)
		self.back_button = TouchArea(back_rect, self.go_back, padding=10)

		self.load()

	def go_back(self):
		self.manager.set("data")

	def load(self):
		try:
			with open("data/quests.json") as f:
				self.quests = json.load(f)
		except:
			self.quests = []

	def save(self):
		with open("data/quests.json", "w") as f:
			json.dump(self.quests, f)

	def handle_event(self, event):
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_BACKSPACE:
				self.go_back()
			if event.key == pygame.K_RETURN:
				self.quests.append("New Quest")
				self.save()

		if event.type == pygame.MOUSEBUTTONDOWN:
			y = event.pos[1]
			index = (y - 80) // 30
			if 0 <= index < len(self.quests):
				del self.quests[index]
				self.save()

		self.back_button.handle_event(event)

	def render(self):
		self.screen.fill(Palette.BG)
		y = 40
		w, h = self.screen.get_size()
		draw_frame(self.screen, (10, 10, w - 20, h - 20))
		draw_hline(self.screen, 20, 60, w - 40)

		title = glow_title("QUESTS (tap to remove, ENTER to add)", self.font)
		self.screen.blit(title, (20, y))
		y += 40

		for q in self.quests:
			text = glow_text(q, self.font)
			self.screen.blit(text, (40, y))
			y += 30

