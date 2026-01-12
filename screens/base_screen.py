import pygame
from .helpers.colors import Palette
PIPBOY_BG = (5, 20, 10)	   # dark green-ish
PIPBOY_FG = (0, 255, 100)	 # bright green

class BaseScreen:
	def __init__(self, screen):
		self.screen = screen

	def handle_event(self, event):
		"""Override in subclass if needed."""
		pass

	def update(self, dt):
		"""Override in subclass."""
		pass

	def render(self):
		"""Override in subclass."""
		self.screen.fill(Palette.BG)

