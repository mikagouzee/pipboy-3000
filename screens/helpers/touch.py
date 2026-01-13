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
        self.pulse = 0.0 #0 = no pulse, 1 = full brightness

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
            self.pulse = 1.0
            self.callback()

    def update(self, dt):
        if self.pulse > 0:
                self.pulse -= dt * 2
                if self.pulse < 0:
                        self.pulse = 0


    def draw_pulse(self, surface):
        if self.pulse > 0:
                overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
                alpha = int(self.pulse * 100)
                overlay.fill((80, 255, 80, alpha))
                surface.blit(overlay, (0,0))
                print("Pulse:", self.pulse)
