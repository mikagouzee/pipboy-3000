import pygame, json
from .base_screen import BaseScreen, PIPBOY_BG, PIPBOY_FG
from .fonts import load_font
from .colors import Palette
from .glow_text import glow_text, glow_title
from .ui_frame import draw_frame, draw_hline, draw_corner

class QuestsScreen(BaseScreen):
	def __init__(self, screen, manager):
		super().__init__(screen)
		self.manager = manager
		self.font = load_font(20)

		self.load()

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
			if event.key == pygame.K_ESCAPE:
				self.manager.set("data")
			if event.key == pygame.K_RETURN:
				self.quests.append("New Quest")
				self.save()

		if event.type == pygame.MOUSEBUTTONDOWN:
			y = event.pos[1]
			index = (y - 80) // 30
			if 0 <= index < len(self.quests):
				del self.quests[index]
				self.save()

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

