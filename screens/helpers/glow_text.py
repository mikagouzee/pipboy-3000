import pygame
from .colors import Palette

def glow_text(text, font):
	return render_glow_text(text, font, Palette.FG, Palette.TEXT, 1)

def glow_title(text, font):
	return render_glow_text(text, font, Palette.FG, Palette.TITLE)

def render_glow_text(text, font, color, glow_color, glow_size=2):
	"""
	Render text with a glow effect.
	- glow_size: how thick the glow halo is
	"""
	# Render base text
	base = font.render(text, True, color)

	# Create glow surface slightly larger
	w, h = base.get_size()
	glow_surface = pygame.Surface((w + glow_size * 2, h + glow_size * 2), pygame.SRCALPHA)

	# Draw glow by rendering the text multiple times offset around the center
	for dx in range(-glow_size, glow_size + 1):
		for dy in range(-glow_size, glow_size + 1):
			if dx*dx + dy*dy <= glow_size * glow_size:
				glow_surface.blit(font.render(text, True, glow_color), (dx + glow_size, dy + glow_size))

	# Draw main text on top
	glow_surface.blit(base, (glow_size, glow_size))

	return glow_surface

