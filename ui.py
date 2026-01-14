# pypboy/ui.py
import pygame
import datetime
import config
from game.core import Entity, EntityGroup


class Header(Entity):
    """
    Simple header that displays a headline, title and a clock.
    Compatible with legacy usage: header.headline, header.title
    """
    def __init__(self, headline="", title=""):
        self.headline = headline
        self.title = title
        super(Header, self).__init__((config.WIDTH, config.HEIGHT))
        self.rect.topleft = (4, 0)
        self._date = None

    def update(self, *args, **kwargs):
        super(Header, self).update(*args, **kwargs)

    def render(self, *args, **kwargs):
        new_date = datetime.datetime.now().strftime("%d.%m.%y.%H:%M:%S")
        if new_date != self._date:
            # redraw header only when date changes
            self.image.fill((0, 0, 0))
            # decorative lines
            pygame.draw.line(self.image, (95, 255, 177), (5, 15), (5, 35), 2)
            pygame.draw.line(self.image, (95, 255, 177), (5, 15), (config.WIDTH - 154, 15), 2)
            pygame.draw.line(self.image, (95, 255, 177), (config.WIDTH - 154, 15), (config.WIDTH - 154, 35), 2)
            pygame.draw.line(self.image, (95, 255, 177), (config.WIDTH - 148, 15), (config.WIDTH - 13, 15), 2)
            pygame.draw.line(self.image, (95, 255, 177), (config.WIDTH - 13, 15), (config.WIDTH - 13, 35), 2)

            # headline
            try:
                text = config.FONTS[14].render("  %s  " % self.headline, True, (105, 251, 187), (0, 0, 0))
                self.image.blit(text, (26, 8))
            except Exception:
                pass

            # title (right side)
            try:
                text = config.FONTS[14].render(self.title, True, (95, 255, 177), (0, 0, 0))
                self.image.blit(text, ((config.WIDTH - 154) - text.get_width() - 10, 19))
            except Exception:
                pass

            # date/time
            try:
                text = config.FONTS[14].render(new_date, True, (95, 255, 177), (0, 0, 0))
                self.image.blit(text, ((config.WIDTH - 141), 19))
            except Exception:
                pass

            self._date = new_date
        super(Header, self).update(*args, **kwargs)


class Footer(Entity):
    """
    Footer that displays a horizontal menu. Use footer.menu = [labels...]
    and footer.select(label) to highlight.
    """
    def __init__(self):
        super(Footer, self).__init__((config.WIDTH, config.HEIGHT))
        self.menu = []
        self.selected = None
        self.rect.topleft = (4, config.HEIGHT - 40)

    def update(self, *args, **kwargs):
        super(Footer, self).update(*args, **kwargs)

    def select(self, module_label):
        self.selected = module_label
        self.image.fill((0, 0, 0))
        pygame.draw.line(self.image, (95, 255, 177), (5, 2), (5, 20), 2)
        pygame.draw.line(self.image, (95, 255, 177), (5, 20), (config.WIDTH - 13, 20), 2)
        pygame.draw.line(self.image, (95, 255, 177), (config.WIDTH - 13, 2), (config.WIDTH - 13, 20), 2)

        offset = 20
        for m in self.menu:
            padding = 1
            text_width = 0
            # ensure a minimum width for each menu item
            while text_width < 54:
                spaces = " ".join([" " for _ in range(padding)])
                text = config.FONTS[12].render("%s%s%s" % (spaces, m, spaces), True, (105, 251, 187), (0, 0, 0))
                text_width = text.get_size()[0]
                padding += 1
            if m == self.selected:
                pygame.draw.rect(self.image, (95, 255, 177), (offset - 2, 6, (text_width + 3), 26), 2)
            self.image.blit(text, (offset, 12))
            offset = offset + 120 + (text_width - 100)


class Menu(Entity):
    """
    Simple vertical menu used by SubModules. Items is a list of labels.
    callbacks is a list of callables aligned with items.
    """
    def __init__(self, width, items=None, callbacks=None, selected=0):
        items = items or []
        callbacks = callbacks or []
        super(Menu, self).__init__((width, config.HEIGHT - 80))
        self.items = items
        self.callbacks = callbacks
        self.selected = 0
        self.select(selected)

        if getattr(config, "SOUND_ENABLED", False):
            try:
                self.dial_move_sfx = pygame.mixer.Sound('sounds/dial_move.ogg')
            except Exception:
                self.dial_move_sfx = None

    def select(self, item_index):
        # item_index can be index or label
        if isinstance(item_index, int):
            self.selected = item_index
        else:
            try:
                self.selected = self.items.index(item_index)
            except Exception:
                self.selected = 0
        self.redraw()
        if len(self.callbacks) > self.selected and self.callbacks[self.selected]:
            try:
                self.callbacks[self.selected]()
            except Exception:
                pass

    def handle_action(self, action):
        if action == "dial_up":
            if self.selected > 0:
                if getattr(self, "dial_move_sfx", None):
                    try:
                        self.dial_move_sfx.play()
                    except Exception:
                        pass
                self.select(self.selected - 1)
        elif action == "dial_down":
            if self.selected < len(self.items) - 1:
                if getattr(self, "dial_move_sfx", None):
                    try:
                        self.dial_move_sfx.play()
                    except Exception:
                        pass
                self.select(self.selected + 1)

    def redraw(self):
        self.image.fill((0, 0, 0))
        offset = 5
        for i in range(len(self.items)):
            try:
                text = config.FONTS[14].render(" %s " % self.items[i], True, (105, 251, 187), (0, 0, 0))
            except Exception:
                text = pygame.font.Font(None, 14).render(" %s " % self.items[i], True, (105, 251, 187), (0, 0, 0))
            if i == self.selected:
                selected_rect = (5, offset - 2, text.get_size()[0] + 6, text.get_size()[1] + 3)
                pygame.draw.rect(self.image, (95, 255, 177), selected_rect, 2)
            self.image.blit(text, (10, offset))
            offset += text.get_size()[1] + 6


class Scanlines(Entity):
    """
    Animated scanlines entity. gap and colours allow flexible patterns.
    render(interval) advances the animation.
    """
    def __init__(self, width, height, gap, speed, colours, full_push=False):
        super(Scanlines, self).__init__((width, height))
        self.width = width
        self.height = height
        self.move = gap * len(colours)
        self.gap = gap
        self.colours = colours
        self.rect.top = 0
        self.top = 0.0
        self.speed = speed
        self.full_push = full_push

        # prefill image with repeating colour bands
        colour = 0
        area = pygame.Rect(0, 0, self.width, self.gap)
        y = 0
        while y <= self.height - self.gap:
            try:
                self.image.fill(self.colours[colour], area)
            except Exception:
                # fallback: draw a semi-transparent band
                pygame.draw.rect(self.image, (0, 0, 0, 20), area)
            area.move_ip(0, self.gap)
            y += self.gap
            colour += 1
            if colour >= len(self.colours):
                colour = 0

    def render(self, interval, *args, **kwargs):
        self.top += self.speed * interval
        self.rect.top = int(self.top)
        self.dirty = 1
        if self.full_push:
            if self.top >= self.height:
                self.top = 0
        else:
            if (self.top * self.speed) >= self.move:
                self.top = 0
        super(Scanlines, self).update()


class Overlay(Entity):
    """
    Overlay that blits a semi-transparent image over the screen.
    """
    def __init__(self, path='images/overlay.png', opacity=128):
        try:
            img = pygame.image.load(path).convert_alpha()
        except Exception:
            img = pygame.Surface((config.WIDTH, config.HEIGHT), pygame.SRCALPHA)
            img.fill((0, 0, 0, 0))
        self.image = img.copy()
        super(Overlay, self).__init__((config.WIDTH, config.HEIGHT))
        self.blit_alpha(self, self.image, (0, 0), opacity)

    def blit_alpha(self, target, source, location, opacity):
        x, y = location
        temp = pygame.Surface((source.get_width(), source.get_height())).convert()
        try:
            temp.blit(target.image if hasattr(target, "image") else target, (-x, -y))
        except Exception:
            temp.blit(target, (-x, -y))
        temp.blit(source, (0, 0))
        temp.set_alpha(opacity)
        try:
            target.image.blit(temp, location)
        except Exception:
            target.blit(temp, location)


class Border(Entity):
    def __init__(self, path='images/border.png'):
        try:
            img = pygame.image.load(path).convert_alpha()
            self.image = img
            self.rect = self.image.get_rect()
        except Exception:
            super(Border, self).__init__()
            self.image.fill((0, 0, 0))
            self.rect = self.image.get_rect()

