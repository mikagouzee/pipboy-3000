import pygame
from .colors import PipboyPalette

def draw_frame(surface, rect, thickness=2):
    """
    Draw a rectangular Pip-Boy frame.
    rect = (x, y, w, h)
    """
    x, y, w, h = rect
    color = PipboyPalette.FG

    pygame.draw.rect(surface, color, pygame.Rect(x, y, w, h), thickness)

def draw_hline(surface, x, y, length, thickness=2):
    """
    Draw a horizontal separator line.
    """
    color = PipboyPalette.FG
    pygame.draw.line(surface, color, (x, y), (x + length, y), thickness)

def draw_vline(surface, x, y, length, thickness=2):
    """
    Draw a vertical separator line.
    """
    color = PipboyPalette.FG
    pygame.draw.line(surface, color, (x, y), (x, y + length), thickness)

def draw_corner(surface, x, y, size=10, thickness=2):
    """
    Draw a small L-shaped corner accent.
    """
    color = PipboyPalette.FG
    pygame.draw.line(surface, color, (x, y), (x + size, y), thickness)
    pygame.draw.line(surface, color, (x, y), (x, y + size), thickness)

