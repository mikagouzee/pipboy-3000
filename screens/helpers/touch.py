import pygame
import time

class TouchArea:
    def __init__(self, rect, callback, padding=12, debounce_ms=150):
        """
        rect: pygame.Rect defining the visual button area
        callback: function to call when tapped
        padding: extra hitbox around the rect (in pixels)
        debounce_ms: minimum time between taps
        """
        self.rect = rect
        self.callback = callback
        self.padding = padding
        self.debounce_ms = debounce_ms
        self._last_tap = 0

    def _expanded_rect(self):
        return self.rect.inflate(self.padding * 2, self.padding * 2)

    def handle_event(self, event):
        if event.type != pygame.MOUSEBUTTONDOWN:
            return

        x, y = event.pos
        expanded = self._expanded_rect()

        if expanded.collidepoint(x, y):
            now = time.time() * 1000  # ms
            if now - self._last_tap < self.debounce_ms:
                return  # ignore double taps

            self._last_tap = now
            self.callback()

