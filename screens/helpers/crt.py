import pygame

def create_scanlines(width, height, line_height=2, gap_height=2, opacity=40):
	"""
	Create a transparent surface with horizontal scanlines.
	- line_height: thickness of dark line
	- gap_height: space between lines
	- opacity: 0–255
	"""
	surface = pygame.Surface((width, height), pygame.SRCALPHA)

	y = 0
	while y < height:
		pygame.draw.rect(
			surface,
			(0, 0, 0, opacity),  # semi-transparent black
			pygame.Rect(0, y, width, line_height)
		)
		y += line_height + gap_height

	return surface

